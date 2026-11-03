---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Guided Practice: Script Templates And Steps

In this session you compose a `steps` template that calls a `script` template and passes its printed text to a second step. Then you add a `suspend` step and resume it. You use the module playground, which is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-030-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-030-02" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Compose two steps

Save this as `workflow-compose.yaml`. The first step runs a `script` template and prints text. The second step receives the printed text through the tag `{{steps.shout.outputs.result}}` and writes it to a file that becomes an output parameter:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: compose-one
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
      command: [python]
      source: |
        print("shuttle".upper())
  - name: record
    inputs:
      parameters:
      - name: value
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ['open("/tmp/result","w").write("{{inputs.parameters.value}}")']
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

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/compose-one --timeout=240s
kubectl -n starfleet get workflow compose-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{"\n"}{end}'
```

The node list has one node of type `Steps` for the entrypoint, one `StepGroup` node for each outer group, and one `Pod` node for each step. Only the `Pod` nodes ran containers. Read the values:

```sh
kubectl -n starfleet get workflow compose-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.outputs.result}{" "}{.outputs.parameters}{"\n"}{end}'
```

The `shout` node has the text `SHUTTLE` in `outputs.result`. The `record` node has the parameter `result` with the same text, which proves that the value passed from step to step.

## Add a suspend step

Save this as `workflow-approval.yaml`. The workflow has a `suspend` template between two steps, so it pauses until you resume it:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: approval-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: gated
  templates:
  - name: gated
    steps:
    - - name: approval
        template: wait-here
    - - name: after
        template: say
  - name: wait-here
    suspend: {}
  - name: say
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('approved')"]
```

Apply it:

```sh
kubectl apply -f workflow-approval.yaml
```

Then check that it waits:

```sh
kubectl -n starfleet get workflow approval-one -o jsonpath='{.status.phase}{"\n"}'
kubectl -n starfleet get pods -l workflows.argoproj.io/workflow=approval-one
```

The phase is `Running` and no pod exists, because a `suspend` node creates no pod. A person resumes it with `argo resume approval-one -n starfleet`. Without the `argo` tool, you can delete the workflow, because the workflow has no `activeDeadlineSeconds` and would wait without an end:

```sh
kubectl -n starfleet delete workflow approval-one compose-one
```

## Reason about what you saw

The `steps` template made the order, and the tag moved the printed text between pods. The `script` node needed no file and no output declaration, because its standard output became `outputs.result`. The `suspend` node held the workflow in `Running` without using cluster resources for a pod. That is why a suspend needs a deadline or a person who owns it.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. A workflow with a `suspend` step and no deadline waits forever. A `script` result is for small text only.
