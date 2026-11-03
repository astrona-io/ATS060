---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Compose A Workflow From A Reusable Template Library Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-030-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-030-01" || exit 1
```

Save this as `workflowtemplate-crew-library.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: crew-library
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  activeDeadlineSeconds: 180
  arguments:
    parameters:
    - name: crew
      value: apollo
  templates:
  - name: announce
    inputs:
      parameters:
      - name: name
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - 'open("/tmp/result","w").write("{{inputs.parameters.name}}")'
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflowtemplate-crew-library.yaml
```

Save this as `workflow-launch-crew.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: launch-crew
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: main
  activeDeadlineSeconds: 180
  arguments:
    parameters:
    - name: crew
      value: orion
  templates:
  - name: main
    steps:
    - - name: call
        templateRef:
          name: crew-library
          template: announce
        arguments:
          parameters:
          - name: name
            value: '{{workflow.parameters.crew}}'
```

Apply it:

```sh
kubectl apply -f workflow-launch-crew.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/launch-crew --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow launch-crew -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
