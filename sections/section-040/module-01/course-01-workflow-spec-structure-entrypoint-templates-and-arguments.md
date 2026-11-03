---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Workflow Spec Structure: Entrypoint, Templates And Arguments

A Workflow object has a `spec` field that tells the controller what to run. This part explains the fields that decide where execution starts, which definitions are available and how values enter the run. The controller is the Argo component that watches Workflow objects and creates pods for them.

## The smallest complete spec

Every runnable spec needs an entrypoint and a list of templates that contains it:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: probe-run
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: main
  templates:
  - name: main
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('probe ready')"]
```

The fields have these jobs:

- `entrypoint` names the template where the controller starts. If no template has that name, the controller marks the workflow as an error before any pod exists.
- `templates` is the list of definitions. Each item has a unique `name` and exactly one type field, such as `container`, `script`, `steps` or `dag`.
- `serviceAccountName` selects the Kubernetes ServiceAccount that the workflow pods use. A ServiceAccount is the identity that a pod presents to the Kubernetes API.
- `metadata.name` fixes the object name. The field `generateName` asks the API server to append a random suffix, so every submission gets a new object.

## How the entrypoint walks the graph

The entrypoint is only the first node. If it is a `steps` or `dag` template, it calls other templates by name, and those can call more. The controller creates a node in the status for each call. Only templates that are reachable from the entrypoint run. An unused template is accepted by the API server and then never executed.

A workflow can also set `onExit`, which names a template that runs after the main graph ends, whether it succeeded or failed. This is the place for notification or cleanup work that must run in both cases.

## Arguments cross the workflow boundary

The `arguments` field supplies values when the run starts:

```yaml
spec:
  entrypoint: main
  arguments:
    parameters:
    - name: ship
      value: voyager
    artifacts:
    - name: manifest
      raw:
        data: |
          crew: 12
```

A parameter is a named string. A template reads a workflow-level parameter with the tag `{{workflow.parameters.ship}}`. The controller replaces the tag with the value before it creates the pod, so the container receives plain text and never sees the tag.

A parameter that has no `value` is required: the workflow fails to start when the submission does not supply one. A parameter with a `value` is a default that a submission can override.

Inside the graph, a template declares what it needs with `inputs`, and the caller passes values with its own `arguments`:

```yaml
  templates:
  - name: announce
    inputs:
      parameters:
      - name: name
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('{{inputs.parameters.name}}')"]
```

The tag `{{inputs.parameters.name}}` works only inside the template that declares the input. The workflow-level tag works everywhere in the spec.

## Template fields that change the pod

A container template accepts most fields of a Kubernetes container: `image`, `command`, `args`, `env`, `resources` and `volumeMounts`. Fields that belong to the pod rather than a container, such as `nodeSelector`, `tolerations` and `affinity`, are set on the template itself or on the workflow spec. A value on the template overrides the value on the workflow spec for that template.

```yaml
spec:
  nodeSelector:
    kubernetes.io/os: linux
  templates:
  - name: main
    nodeSelector:
      kubernetes.io/arch: amd64
```

Both fields are part of the declaration. Whether a node matches is decided later by the Kubernetes scheduler, so the pod can stay in the `Pending` phase even when the spec is valid.

## What the API server checks and what it does not

When you apply the object, the API server checks that the YAML matches the Workflow schema. The controller then validates the graph: names must be unique, references must resolve and an input without a value must be supplied. These checks do not prove that the image can be pulled, that the node has capacity or that the ServiceAccount has the needed permission. Those facts appear only when the pod starts.

## Reading a spec in order

Use the same order every time:

1. Find the `entrypoint` and open that template.
2. List the templates it calls and repeat for each one.
3. For each template, note the inputs it needs and the arguments its callers pass.
4. Note the workflow-level `arguments`, `serviceAccountName` and placement fields.
5. Note the controls that bound the run: deadline, retry, parallelism and cleanup.

The last item is the subject of the next part.

## Common pitfalls

> [!WARNING]
> An accepted spec is not a run that works. A misspelled entrypoint is caught by the controller, but a missing image, a wrong ServiceAccount or an unmatched node selector appears only when the pod starts.
