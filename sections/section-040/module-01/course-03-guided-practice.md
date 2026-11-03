---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Guided Practice: Arguments, Deadlines And Cleanup

In this session you run two workflows in the module playground. The first uses an argument and cleanup settings. The second exceeds its deadline, so you can read how a timeout appears in the status. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-040-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-040-01" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Run a workflow with an argument and a cleanup policy

Save this as `workflow-arguments.yaml`. The workflow-level parameter `ship` is read with the tag `{{workflow.parameters.ship}}`, and the `ttlStrategy` field deletes the object one hour after it ends:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: arguments-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: main
  activeDeadlineSeconds: 120
  ttlStrategy:
    secondsAfterCompletion: 3600
  arguments:
    parameters:
    - name: ship
      value: voyager
  templates:
  - name: main
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('ship is {{workflow.parameters.ship}}')"]
```

Apply it:

```sh
kubectl apply -f workflow-arguments.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/arguments-one --timeout=180s
kubectl -n starfleet get workflow arguments-one -o jsonpath='{.spec.ttlStrategy}{"\n"}{.status.finishedAt}{"\n"}'
kubectl -n starfleet logs -l workflows.argoproj.io/workflow=arguments-one -c main
```

The log line shows the value that the controller put in place of the tag. The `ttlStrategy` field is still on the object, and the controller removes the object after the stated time.

## Exceed a deadline on purpose

Save this as `workflow-deadline.yaml`. The container sleeps for much longer than the template deadline of 20 seconds:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: deadline-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: slow
  templates:
  - name: slow
    activeDeadlineSeconds: 20
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["import time; time.sleep(120)"]
```

Apply it:

```sh
kubectl apply -f workflow-deadline.yaml
```

Then check the result. The wait command ends when the phase is `Failed`, which is the expected end state here:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Failed workflow/deadline-one --timeout=180s
kubectl -n starfleet get workflow deadline-one -o jsonpath='{.status.message}{"\n"}'
kubectl -n starfleet get workflow deadline-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{" "}{.message}{"\n"}{end}'
```

Read the message and the node message. They name the reason for the failure. Compare them with the spec: the container did not exit with an error code of its own, because the controller ended it.

## Clean up the examples

Delete both objects. The pods are owned by the workflows, so they are removed with them:

```sh
kubectl -n starfleet delete workflow arguments-one deadline-one
kubectl -n starfleet get pods
```

## Reason about what you saw

The argument reached the pod as plain text, because the controller substitutes tags before it creates the pod. The deadline ended a workflow that had no fault of its own, and the status recorded why. The `ttlStrategy` field was a declaration only. Its effect would appear after the stated time, which you did not wait for.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. A failed workflow is the expected result of the deadline exercise, so do not retry it until you have read its message. Delete the example workflows when you finish so later exercises start clean.
