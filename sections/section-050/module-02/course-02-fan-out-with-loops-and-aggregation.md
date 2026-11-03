---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Fan-Out With Loops And Aggregation

Fan-out runs the same template many times with different inputs. In a DAG, one task with a loop field creates one node for each item. A later task can collect the results.

## withItems

`withItems` takes a list. The task runs once for every item, and the tag `{{item}}` holds the current value:

```yaml
dag:
  tasks:
  - name: survey
    template: scan
    arguments:
      parameters:
      - name: sector
        value: '{{item}}'
    withItems: [alpha, beta, gamma]
```

This creates three nodes. Each node has a name that contains the item index, and each one is a pod. Items can be objects too, and a template reads their fields with tags such as `{{item.sector}}`.

## withParam

`withParam` takes a JSON array as text, usually from a workflow parameter or from the output of an earlier task:

```yaml
- name: survey
  template: scan
  dependencies: [list]
  arguments:
    parameters:
    - name: sector
      value: '{{item}}'
  withParam: '{{tasks.list.outputs.result}}'
```

The earlier task must print valid JSON, for example `["alpha","beta"]`. The list size can be decided at run time, so the number of nodes is not known when you write the spec. If the text is not valid JSON, the controller cannot create the nodes and the task fails.

## withSequence

`withSequence` generates a count instead of a list:

```yaml
withSequence:
  count: "5"
```

The tag `{{item}}` holds the number of the iteration. The value for `count` is a string.

## Aggregation

When every iteration of a task has finished, the outputs of all iterations can be read as one JSON array through the `outputs.result` of the looped task. Every iteration must print valid JSON for this to work. A later task depends on the looped task and reads the array:

```yaml
- name: gather
  template: show
  dependencies: [survey]
  arguments:
    parameters:
    - name: all
      value: '{{tasks.survey.outputs.result}}'
```

The task `gather` starts after all iterations have finished. With the default fail-fast behavior, one failed iteration stops further scheduling, and `gather` does not run.

## Results of a looped task in depends

A looped task has extra result names for `depends`: `AnySucceeded` is true when at least one iteration succeeded, and `AllFailed` is true when every iteration failed. Use them to run a join after a partial success:

```yaml
depends: "survey.AnySucceeded"
```

## Limiting the fan-out

A loop with a large list creates many pods. The `parallelism` field of the workflow or of the DAG limits how many run together. The cluster still needs capacity for each pod, so plan the size of the list.

```yaml
spec:
  parallelism: 3
```

## Choosing a loop

- Use `withItems` when the list is known when you write the spec.
- Use `withParam` when the list comes from a parameter or an earlier task.
- Use `withSequence` when you need a count without a list.

## Common pitfalls

> [!WARNING]
> Output from a looped task is aggregated as JSON, so each iteration must print valid JSON. A large fan-out without a parallelism limit can exhaust the cluster. A loop over an empty list creates no nodes, so a join that reads their output gets an empty value.
