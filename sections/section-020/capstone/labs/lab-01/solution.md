---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Build A Three-Step Artifact Pipeline With Cleanup Policy Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-020-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-020-01" || exit 1
```

Save this as `workflow-data-flow.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: data-flow
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 240
  artifactGC:
    strategy: OnWorkflowDeletion
    serviceAccountName: workflow-runner
  templates:
  - name: pipeline
    steps:
    - - name: generate
        template: generate
    - - name: transform
        template: transform
        arguments:
          artifacts:
          - name: source
            from: '{{steps.generate.outputs.artifacts.source}}'
    - - name: summarise
        template: summarise
        arguments:
          artifacts:
          - name: final
            from: '{{steps.transform.outputs.artifacts.final}}'
  - name: generate
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/source","w").write("probe data")
    outputs:
      artifacts:
      - name: source
        path: /tmp/source
  - name: transform
    inputs:
      artifacts:
      - name: source
        path: /tmp/in
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/final","w").write(open("/tmp/in").read().upper())
    outputs:
      artifacts:
      - name: final
        path: /tmp/final
        archive:
          none: {}
        s3:
          key: '{{workflow.name}}/final.txt'
        artifactGC:
          strategy: Never
  - name: summarise
    inputs:
      artifacts:
      - name: final
        path: /tmp/final
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write(open("/tmp/final").read())
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-data-flow.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/data-flow --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow data-flow -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
