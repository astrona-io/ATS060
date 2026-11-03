---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Guided Practice: A Diamond DAG With Data Flow

In this session you run a diamond DAG, prove the order from node times and then break one branch to see the effect of fail-fast. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-050-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-050-01" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Run a diamond

Save this as `workflow-diamond.yaml`. The task `measure` produces a value, the tasks `east` and `west` wait for it, and `combine` waits for both and receives the value from `measure`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: diamond-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: measure
        template: emit
      - name: east
        template: pause
        dependencies: [measure]
      - name: west
        template: pause
        dependencies: [measure]
      - name: combine
        template: show
        dependencies: [east, west]
        arguments:
          parameters:
          - name: value
            value: '{{tasks.measure.outputs.parameters.reading}}'
  - name: emit
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ['open("/tmp/reading","w").write("42")']
    outputs:
      parameters:
      - name: reading
        valueFrom:
          path: /tmp/reading
  - name: pause
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["import time; time.sleep(5)"]
  - name: show
    inputs:
      parameters:
      - name: value
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('reading is {{inputs.parameters.value}}')"]
```

Apply it:

```sh
kubectl apply -f workflow-diamond.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/diamond-one --timeout=240s
kubectl -n starfleet get workflow diamond-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{" "}{.startedAt}{" "}{.finishedAt}{"\n"}{end}'
kubectl -n starfleet logs -l workflows.argoproj.io/workflow=diamond-one -c main --tail=5
```

Compare the times. The start times of `east` and `west` are close to each other and later than the finish of `measure`. The start of `combine` is later than the finish of both branches. The log of `combine` shows the value that came from `measure`.

## Break one branch

Save this as `workflow-failfast.yaml`. The task `bad` fails at once and `slow` runs for 20 seconds. The task `after` depends on `slow`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: failfast-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: bad
        template: fail
      - name: slow
        template: wait
      - name: after
        template: wait
        dependencies: [slow]
  - name: fail
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["raise SystemExit(1)"]
  - name: wait
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["import time; time.sleep(20)"]
```

Apply it:

```sh
kubectl apply -f workflow-failfast.yaml
```

Then check the result. The expected end state is `Failed`:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Failed workflow/failfast-one --timeout=240s
kubectl -n starfleet get workflow failfast-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{"\n"}{end}'
```

Read which tasks ran. Then delete the workflow, add `failFast: false` under `dag`, apply it again with a new name and compare the node list.

## Clean up the examples

```sh
kubectl -n starfleet delete workflow diamond-one failfast-one
```

## Reason about what you saw

The diamond ran in the order that the dependencies set, and the join read data from a task that was not its direct dependency, which works because the task finished earlier in the chain. The failing branch showed the effect of fail-fast on work that had not started.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. A failed workflow is the expected result of the second example. Use a new workflow name for each comparison, because the controller does not rerun a finished object.
