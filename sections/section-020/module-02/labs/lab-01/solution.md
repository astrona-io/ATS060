---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Stage A Raw Input Without Packing Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-020-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-020-02-01" || exit 1
```

Save this as `workflow-staging.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: staging
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 180
  templates:
  - name: pipeline
    steps:
    - - name: stage
        template: stage
    - - name: read
        template: read
        arguments:
          artifacts:
          - name: staged
            from: '{{steps.stage.outputs.artifacts.staged}}'
  - name: stage
    inputs:
      artifacts:
      - name: note
        path: /tmp/note
        raw:
          data: crew-roster
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/staged","w").write(open("/tmp/note").read())
    outputs:
      artifacts:
      - name: staged
        path: /tmp/staged
        archive:
          none: {}
        s3:
          key: '{{workflow.name}}/staged.txt'
  - name: read
    inputs:
      artifacts:
      - name: staged
        path: /tmp/input
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write(open("/tmp/input").read())
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-staging.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/staging --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow staging -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
