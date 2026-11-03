---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Guided Practice: Raw Inputs, Archive Options And Passing Artifacts

This session uses the module playground. You run a workflow that takes a raw input artifact, stores it without packing under a chosen key, and passes it to a second step with `from`. Then you read the stored references. The graded task uses its own environment, so nothing here affects it.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-020-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-020-02" || exit 1
kubectl -n argo get deployment workflow-controller minio
```

Both deployments must be available. MinIO is the artifact repository and the controller creates the pods.

## Check the repository configuration

The default repository is set in the controller ConfigMap. Read it before the run so you know where the objects will go:

```sh
kubectl -n argo get configmap workflow-controller-configmap -o jsonpath='{.data.artifactRepository}'
kubectl -n starfleet get secret my-minio-cred
```

The first command prints the `s3` block with the bucket `my-bucket` and the endpoint `minio.argo.svc:9000`. The second command shows that the credential Secret exists in the namespace where the pods run.

## Run a workflow with a raw input

Save this as `workflow-stage-note.yaml`. The first step takes the raw input `note`, copies it to an output file and stores that file without packing. The second step receives it with `from` and reads it:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: stage-note
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
          data: roster-bridge
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
kubectl apply -f workflow-stage-note.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/stage-note --timeout=240s
kubectl -n starfleet get workflow stage-note -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.outputs.artifacts}{"\n"}{end}'
```

The `stage` node shows an artifact named `staged`. Its `s3.key` is `stage-note/staged.txt`, because the controller replaced the tag with the workflow name. The `read` node shows no artifact, because it only reads.

## Read the output parameter

The second step copied the input into a parameter, so you can compare the value with the raw data:

```sh
kubectl -n starfleet get workflow stage-note -o jsonpath='{range .status.nodes.*}{.outputs.parameters}{"\n"}{end}'
```

The value is `roster-bridge`. It went through three places: the manifest, the repository and the parameter of the second node.

## Reason about what you saw

The data of the first step came from the manifest through `raw`, so no external service was needed for the input. The `archive.none` field stored the file as it is. That is why the key `stage-note/staged.txt` is a plain text object. The default packing would have stored a `.tgz` object. The second pod downloaded the object through its `init` container, because the `from` field gave it the reference.

If you remove the `archive` block and run again with a new name, the stored object is packed, and the `read` step still sees the same text. The unpacking is invisible to your code. It becomes visible only to a program that reads the bucket directly.

## Clean up

Delete the workflow before you leave the playground. The stored object stays in MinIO, because no garbage collection was configured, and the playground is removed with the next page:

```sh
kubectl -n starfleet delete workflow stage-note
```

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. A deleted Workflow leaves its objects in the repository unless garbage collection is configured. The raw data keeps its trailing line break when you use a YAML block scalar.
