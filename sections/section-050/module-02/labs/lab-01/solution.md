---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Choose A DAG Branch With A When Condition Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-050-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-050-02-01" || exit 1
```

Save this as `workflow-gate.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: gate
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
        dependencies:
        - check
        when: '{{tasks.check.outputs.result}} == green'
      - name: abort
        template: act
        dependencies:
        - check
        when: '{{tasks.check.outputs.result}} != green'
      - name: report
        template: act
        depends: launch || abort
  - name: decide
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        print("green")
  - name: act
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - print('acting')
```

Apply it:

```sh
kubectl apply -f workflow-gate.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/gate --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow gate -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
