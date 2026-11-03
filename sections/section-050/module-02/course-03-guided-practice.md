---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Guided Practice: Conditional Branches And A Fan-Out

In this session you run a DAG that chooses between two branches with `when`, then a DAG that fans out over a list. You read the node phases to see which tasks ran. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-050-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-050-02" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Run a two-branch choice

Save this as `workflow-branch.yaml`. The task `check` prints `amber`, so the branch for `green` is skipped and the other branch runs. The task `report` accepts either branch:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: branch-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: check
        template: decide
      - name: launch
        template: act
        dependencies: [check]
        when: "{{tasks.check.outputs.result}} == green"
      - name: abort
        template: act
        dependencies: [check]
        when: "{{tasks.check.outputs.result}} != green"
      - name: report
        template: act
        depends: "launch || abort"
  - name: decide
    script:
      image: docker.io/library/python:3.13-alpine
      command: [python]
      source: |
        print("amber")
  - name: act
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('acting')"]
```

Apply it:

```sh
kubectl apply -f workflow-branch.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/branch-one --timeout=240s
kubectl -n starfleet get workflow branch-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{"\n"}{end}'
```

The node `launch` is `Skipped` because its `when` condition was false. The node `abort` ran, and `report` ran after both had a final state. Change the printed text to `green`, apply the file under a new name and compare which branch is skipped.

## Run a fan-out

Save this as `workflow-fanout.yaml`. The task `survey` runs once for each item:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: fanout-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  parallelism: 2
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: survey
        template: scan
        arguments:
          parameters:
          - name: sector
            value: '{{item}}'
        withItems: [alpha, beta, gamma]
      - name: gather
        template: done
        dependencies: [survey]
  - name: scan
    inputs:
      parameters:
      - name: sector
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('scanned {{inputs.parameters.sector}}')"]
  - name: done
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('all sectors scanned')"]
```

Apply it:

```sh
kubectl apply -f workflow-fanout.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/fanout-one --timeout=240s
kubectl -n starfleet get workflow fanout-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{" "}{.startedAt}{" "}{.finishedAt}{"\n"}{end}'
```

Count the nodes of the looped task. There is one for each item, and each name contains the item. Compare the start time of `gather` with the finish times of all of them.

## Clean up the examples

```sh
kubectl -n starfleet delete workflow branch-one fanout-one
```

## Reason about what you saw

The `when` field chose a branch from data, and the `depends` expression of the join accepted a skipped task. The loop created nodes from a list, and the parallelism limit set how many ran together. The join waited for the whole loop.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. Use a new workflow name for each comparison. A skipped node is a normal result of a false condition and not an error.
