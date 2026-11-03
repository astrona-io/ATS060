---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Guided Practice: Parameters, Results And Retention

This practice session uses the module playground. You create two runs of the same workflow with different arguments, read the output parameter of each run, and add the retention fields. The graded task on the previous pages uses a separate environment, so nothing here changes it.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check its context before you create anything.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-010-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-010-02" || exit 1
kubectl -n starfleet get serviceaccount workflow-runner
```

The last command shows that the ServiceAccount for the workflow pods exists. No learner Workflow exists yet.

## Create a run with default arguments

Save this as `workflow-report.yaml`. The workflow has one parameter, `message`, with the default `draft`. The template writes the value into a file and exposes the file as an output parameter:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: report-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: report
  activeDeadlineSeconds: 180
  arguments:
    parameters:
    - name: message
      value: draft
  templates:
  - name: report
    inputs:
      parameters:
      - name: message
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("{{inputs.parameters.message}}")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-report.yaml
```

Then wait for the run and read the output parameter that the executor reported:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/report-one --timeout=240s
kubectl -n starfleet get workflow report-one -o jsonpath='{range .status.nodes.*}{.outputs.parameters}{"\n"}{end}'
```

The value is `draft`, the default argument. The controller replaced the tag before it created the pod, and the executor read the file and reported it.

## Override the argument in a second run

`kubectl` has no flag for parameters, so create a second file that sets a different value. Save this as `workflow-report-approved.yaml`. Only the name and the argument value differ from the first file:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: report-two
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: report
  activeDeadlineSeconds: 180
  ttlStrategy:
    secondsAfterCompletion: 600
  podGC:
    strategy: OnWorkflowCompletion
  arguments:
    parameters:
    - name: message
      value: approved
  templates:
  - name: report
    inputs:
      parameters:
      - name: message
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("{{inputs.parameters.message}}")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

This run also adds `ttlStrategy` and `podGC`. Apply it and read the result in the same way:

```sh
kubectl apply -f workflow-report-approved.yaml
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/report-two --timeout=240s
kubectl -n starfleet get workflow report-two -o jsonpath='{range .status.nodes.*}{.outputs.parameters}{"\n"}{end}'
```

The value is now `approved`. Compare the pods of both runs:

```sh
kubectl -n starfleet get pods -l workflows.argoproj.io/workflow=report-one
kubectl -n starfleet get pods -l workflows.argoproj.io/workflow=report-two
```

The first run keeps its completed pod, because it set no `podGC`. The second run has no pod, or a pod that is shutting down, because `OnWorkflowCompletion` deletes the pods when the run ends.

## Check the retention fields

Read the stored retention settings of the second run directly from the object:

```sh
kubectl -n starfleet get workflow report-two -o jsonpath='{.spec.ttlStrategy}{"\n"}{.spec.podGC}{"\n"}'
```

The controller deletes `report-two` 600 seconds after it completes, and `report-one` stays until you delete it. Delete it now so that the practice ends clean:

```sh
kubectl -n starfleet delete workflow report-one
```

## Reason about what you saw

The two runs used the same template and different arguments, so the template is the definition and each `Workflow` is one execution. The output parameter appeared in the node status because the `wait` container reported it. The pod difference came only from `podGC`, not from the result of the run. When you must keep logs of a run with `podGC`, add `archiveLogs: true` or choose `OnPodSuccess` so failed pods stay.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. A `ttlStrategy` removes the `Workflow` object you may still want to inspect, so read the result before the time ends. A deleted pod cannot give its logs again.
