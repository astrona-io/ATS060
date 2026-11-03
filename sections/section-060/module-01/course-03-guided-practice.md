---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Guided Practice: Partition, Process And Join

In this session you run a pipeline that creates its list of parts at run time, processes each part in parallel and joins the results. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-060-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-060-01" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Run the pipeline

Save this as `workflow-pipeline.yaml`. The step `list` prints a JSON array, the step `process` runs once for each element and prints a JSON object, and the step `combine` receives the aggregated array:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: pipeline-one
  namespace: starfleet
  labels:
    dataset: survey-2026-01
spec:
  serviceAccountName: workflow-runner
  entrypoint: main
  activeDeadlineSeconds: 240
  parallelism: 2
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
      command: [python]
      source: |
        print('["alpha","beta","gamma"]')
  - name: produce
    inputs:
      parameters:
      - name: item
    script:
      image: docker.io/library/python:3.13-alpine
      command: [python]
      source: |
        import json
        print(json.dumps({"part": "{{inputs.parameters.item}}", "size": len("{{inputs.parameters.item}}")}))
  - name: combine
    inputs:
      parameters:
      - name: parts
    script:
      image: docker.io/library/python:3.13-alpine
      command: [python]
      source: |
        import json
        parts = json.loads('''{{inputs.parameters.parts}}''')
        print("parts:", len(parts))
```

Apply it:

```sh
kubectl apply -f workflow-pipeline.yaml
```

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/pipeline-one --timeout=240s
kubectl -n starfleet get workflow pipeline-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{"\n"}{end}'
kubectl -n starfleet logs -l workflows.argoproj.io/workflow=pipeline-one -c main --tail=3
```

The node list has one `Pod` node for each element, and its name contains the element. The log of `combine` reports the number of parts that it received. The number must match the length of the list, which is the check that a join should always make.

## Break a part on purpose

Edit the `produce` template so that it exits with an error for the item `beta`, for example by adding `import sys` and `sys.exit(1) if "{{inputs.parameters.item}}" == "beta" else None` before the print. Apply the edited file under the name `pipeline-two` and read the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Failed workflow/pipeline-two --timeout=240s
kubectl -n starfleet get workflow pipeline-two -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{"\n"}{end}'
```

The expected end state is `Failed`. Read which nodes ran and whether `combine` ran. The failed part stopped the join, which is the safe default.

## Clean up the examples

```sh
kubectl -n starfleet delete workflow pipeline-one pipeline-two
```

## Reason about what you saw

The list was not written in the spec, so the number of nodes was decided at run time. Each part ran as its own pod, and the join checked the count. The failed part stopped the pipeline before a partial result could be combined.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. Print valid JSON in every iteration, or the aggregated output cannot be parsed. Use a new workflow name for each experiment.
