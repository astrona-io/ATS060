---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Pass A Script Result Between Steps Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-030-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-030-02-01" || exit 1
```

Save this as `workflow-compose.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: compose
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 180
  templates:
  - name: pipeline
    steps:
    - - name: shout
        template: shout
    - - name: record
        template: record
        arguments:
          parameters:
          - name: value
            value: '{{steps.shout.outputs.result}}'
  - name: shout
    script:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      source: |
        print("bridge".upper())
  - name: record
    inputs:
      parameters:
      - name: value
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("{{inputs.parameters.value}}")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-compose.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/compose --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow compose -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
