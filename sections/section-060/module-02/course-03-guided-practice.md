---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Guided Practice: A Schedule And A Mutex

In this session you create a CronWorkflow that fires every minute, read the Workflow that it creates and then pause it. After that you start two workflows that share a mutex and read the status of the one that waits. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-060-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-060-02" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Create a schedule

Save this as `cron-minute.yaml`. It fires every minute, forbids overlap and keeps one finished run:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: minute-scan
  namespace: starfleet
spec:
  schedules:
  - "* * * * *"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 60
  successfulJobsHistoryLimit: 1
  failedJobsHistoryLimit: 1
  workflowSpec:
    serviceAccountName: workflow-runner
    entrypoint: main
    activeDeadlineSeconds: 60
    templates:
    - name: main
      container:
        image: docker.io/library/python:3.13-alpine
        command: [python, -c]
        args: ["print('scan')"]
```

Apply it:

```sh
kubectl apply -f cron-minute.yaml
```

Then check the result. The first run appears at the next full minute, so wait up to two minutes:

```sh
kubectl -n starfleet get cronworkflow minute-scan
kubectl -n starfleet get workflow -l workflows.argoproj.io/cron-workflow=minute-scan
kubectl -n starfleet get cronworkflow minute-scan -o jsonpath='{.status.lastScheduledTime}{"\n"}'
```

Pause the schedule so that no more runs are created, and confirm the field:

```sh
kubectl -n starfleet patch cronworkflow minute-scan --type merge -p '{"spec":{"suspend":true}}'
kubectl -n starfleet get cronworkflow minute-scan -o jsonpath='{.spec.suspend}{"\n"}'
```

## Make two workflows share a mutex

Save this as `workflow-locked.yaml`. It holds the mutex `pipeline-lock` for about 40 seconds:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: locked-
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: hold
  activeDeadlineSeconds: 180
  synchronization:
    mutexes:
    - name: pipeline-lock
  templates:
  - name: hold
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["import time; time.sleep(40)"]
```

Create two of them with `generateName`, which needs `kubectl create` instead of `apply`:

```sh
kubectl create -f workflow-locked.yaml
kubectl create -f workflow-locked.yaml
```

Then check the result right away. One workflow is `Running` and the other waits without a pod:

```sh
kubectl -n starfleet get workflow -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.phase}{"\n"}{end}'
kubectl -n starfleet get workflow -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.synchronization}{"\n"}{end}'
```

Read the synchronization status of both. The first holds the lock, and the second shows that it waits for it. Wait about a minute and list again to see the second one start after the first has finished.

## Clean up the examples

```sh
kubectl -n starfleet delete cronworkflow minute-scan
kubectl -n starfleet delete workflow --all
```

The last command deletes all workflows in the namespace of this private playground. Use it only in the playground.

## Reason about what you saw

The schedule created ordinary Workflows, and the history limit kept the number of finished ones small. The mutex made the second workflow wait without using a pod. It started after the first one released the lock.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change, and delete all workflows only in a private playground. A schedule that fires every minute keeps creating runs until it is suspended or deleted. A first run can take up to a full minute to appear.
