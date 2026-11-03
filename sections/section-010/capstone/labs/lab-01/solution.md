---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Build A Two-Step Report With Retention Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-010-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-010-01" || exit 1
```

Save this as `workflow-fleet-report.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: fleet-report
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  arguments:
    parameters:
    - name: crew
      value: bridge
  ttlStrategy:
    secondsAfterSuccess: 3600
    secondsAfterFailure: 86400
  podGC:
    strategy: OnPodSuccess
  templates:
  - name: pipeline
    steps:
    - - name: prepare
        template: prepare
        arguments:
          parameters:
          - name: crew
            value: '{{workflow.parameters.crew}}'
    - - name: publish
        template: publish
        arguments:
          parameters:
          - name: value
            value: '{{steps.prepare.outputs.parameters.value}}'
  - name: prepare
    inputs:
      parameters:
      - name: crew
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/value","w").write("{{inputs.parameters.crew}}".upper())
    outputs:
      parameters:
      - name: value
        valueFrom:
          path: /tmp/value
  - name: publish
    inputs:
      parameters:
      - name: value
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("report:{{inputs.parameters.value}}")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-fleet-report.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/fleet-report --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow fleet-report -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
