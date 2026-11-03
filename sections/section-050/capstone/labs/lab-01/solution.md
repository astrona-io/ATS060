---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Build A Branching DAG With A Fan-Out And A Join Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-050-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-050-01" || exit 1
```

Save this as `workflow-route-plan.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: route-plan
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 300
  parallelism: 2
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: scan
        template: decide
      - name: proceed
        template: act
        dependencies:
        - scan
        when: '{{tasks.scan.outputs.result}} == clear'
      - name: hold
        template: act
        dependencies:
        - scan
        when: '{{tasks.scan.outputs.result}} != clear'
      - name: survey
        template: sector
        dependencies:
        - scan
        arguments:
          parameters:
          - name: sector
            value: '{{item}}'
        withItems:
        - alpha
        - beta
        - gamma
      - name: report
        template: act
        depends: (proceed || hold) && survey
  - name: decide
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        print("clear")
  - name: sector
    inputs:
      parameters:
      - name: sector
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - print('scanned {{inputs.parameters.sector}}')
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
kubectl apply -f workflow-route-plan.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/route-plan --timeout=300s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow route-plan -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
