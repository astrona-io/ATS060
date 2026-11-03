---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Run A Locked Partition-Process-Join Pipeline Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-060-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-060-01" || exit 1
```

Save this as `workflow-batch-run.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: batch-run
  namespace: starfleet
  labels:
    dataset: survey-2026-01
spec:
  serviceAccountName: workflow-runner
  entrypoint: main
  activeDeadlineSeconds: 300
  parallelism: 2
  synchronization:
    mutexes:
    - name: batch-lock
  templates:
  - name: main
    steps:
    - - name: list
        template: list-parts
    - - name: process
        template: produce
        withParam: '{{steps.list.outputs.result}}'
        arguments:
          parameters:
          - name: item
            value: '{{item}}'
    - - name: combine
        template: combine
        arguments:
          parameters:
          - name: parts
            value: '{{steps.process.outputs.result}}'
  - name: list-parts
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        print('["alpha","beta","gamma"]')
  - name: produce
    retryStrategy:
      limit: "1"
      retryPolicy: OnFailure
    inputs:
      parameters:
      - name: item
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        import json
        print(json.dumps({"part": "{{inputs.parameters.item}}".upper()}))
  - name: combine
    inputs:
      parameters:
      - name: parts
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        import json
        parts = json.loads('''{{inputs.parameters.parts}}''')
        print("parts:", len(parts))
```

Apply it:

```sh
kubectl apply -f workflow-batch-run.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/batch-run --timeout=300s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow batch-run -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
