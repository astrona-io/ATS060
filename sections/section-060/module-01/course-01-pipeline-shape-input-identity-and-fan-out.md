---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Pipeline Shape: Input Identity, Partitioning And Fan-Out

A data processing job usually follows one shape: choose an input, split it into parts, process each part and combine the results. Argo Workflows expresses the shape with templates and loops. This part covers the first three stages. The next part covers the join and the safety of repeated runs.

## The four stages

1. **Select** the input and record exactly which data the run used.
2. **Partition** the input into independent parts.
3. **Process** every part with the same template.
4. **Combine** the part results into one output.

A Workflow can hold all four stages as `steps` or as a `dag`. The stages share a data contract: each one states what it reads and what it writes.

## Input identity

A run is reproducible only if you can say which input it read. An input such as `latest` can point to different data on the next run, or even between two tasks of the same run. Use these habits:

- Pass the dataset name or version as a workflow parameter and record it in the metadata of the workflow, for example as a label.
- Read the input once, in the first stage, and pass the result on as an artifact or parameter. Later stages then use the same data.
- Name outputs with the workflow name, for example `{{workflow.name}}`, so that two runs never write the same key.

```yaml
spec:
  arguments:
    parameters:
    - name: dataset
      value: survey-2026-01
```

The value is text. The workflow does not check that it names real data, so the first stage should check the input and fail early when it is missing or malformed. A successful download shows that bytes arrived. It does not show that the data is valid.

## Partitioning

The partition stage turns one input into a list of parts, for example file names, date ranges or sector names. There are two ways to give that list to a loop.

When the list is known at authoring time, write it in the spec with `withItems`:

```yaml
- - name: process
    template: produce
    withItems: [alpha, beta, gamma]
    arguments:
      parameters:
      - name: item
        value: '{{item}}'
```

When the list depends on the input, let a first step print it as JSON and read it with `withParam`:

```yaml
- - name: list
    template: list-parts
- - name: process
    template: produce
    withParam: '{{steps.list.outputs.result}}'
    arguments:
      parameters:
      - name: item
        value: '{{item}}'
```

The step `list` must print a JSON array such as `["alpha","beta","gamma"]`. The number of nodes is then decided at run time.

## Processing in parallel

Each iteration is a separate pod with its own input and output. The iterations are independent, so they can run at the same time. Two limits decide how many do:

- `parallelism` on the workflow or the template caps the nodes that run together.
- Cluster capacity and resource requests decide how many pods can be scheduled.

The limit should come from the full processing path. A hundred small pods can be too much for a database or a storage service that all of them call, even if the cluster has room for them.

## Part identity

Each part should know which part it is. Pass the item as an input parameter and use it in names:

```yaml
outputs:
  artifacts:
  - name: part
    path: /tmp/part.txt
    s3:
      key: '{{workflow.name}}/{{inputs.parameters.item}}.txt'
```

Part names in the key mean that iterations never replace each other's output. Without the item in the key, parallel parts that use the same key overwrite one another, and the winner is whichever finished last.

## Reading the status

Every iteration appears as a node whose display name includes the item. A failure of one node shows which part failed and leaves the evidence of the others.

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{"\n"}{end}'
```

## Common pitfalls

> [!WARNING]
> A mutable input name gives different data on different runs. Output keys without the part name collide. Parallelism limits pods of one workflow, not the load on the services behind them.
