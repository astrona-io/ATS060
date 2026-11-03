---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Data Flow, Fail-Fast And Parallelism In DAGs

Dependencies say when a task may run. This part covers how a task reads the output of another task, how the DAG reacts to a failure, and how many tasks run at once.

## Passing outputs between tasks

A task reads the outputs of an earlier task with the tag `{{tasks.<name>.outputs...}}`:

```yaml
dag:
  tasks:
  - name: measure
    template: measure
  - name: report
    template: report
    dependencies: [measure]
    arguments:
      parameters:
      - name: value
        value: '{{tasks.measure.outputs.parameters.reading}}'
```

- `tasks.measure.outputs.parameters.reading` reads an output parameter named `reading`.
- `tasks.measure.outputs.result` reads the standard output of a script template.
- `tasks.measure.outputs.artifacts.data` references an artifact for an input.

A reference does not create an order. The task `report` must also depend on `measure`. If it does not, the controller cannot resolve the tag in time and the workflow is rejected or fails at that point.

A task that did not run has no outputs. A reference to the output of a skipped or omitted task resolves to an empty string. A join task that reads such a value needs a defined behavior for empty input.

## Fail-fast

By default a DAG fails fast. When one task fails, the DAG stops scheduling new tasks, lets running tasks finish and ends as failed. Setting `failFast: false` on the DAG template lets every branch that can still run go on to completion:

```yaml
dag:
  failFast: false
  tasks:
  - name: east
    template: step
  - name: west
    template: step
```

The final phase is still failed if any required task failed. The setting changes how much work finishes before the end. It never stops a pod that already runs, and it does not undo effects of finished tasks.

## Tasks that should continue after a failure

Use a `depends` expression for the task that must run anyway. A cleanup task with `depends: "build.Succeeded || build.Failed"` is eligible after either result. An alternative is the `onExit` handler of the workflow, which runs after the whole graph ends.

## Parallelism

A wide DAG can have many eligible tasks. Two fields limit the concurrent nodes:

- `spec.parallelism` limits the nodes of the whole workflow.
- `parallelism` on a DAG template limits the tasks of that DAG.

```yaml
spec:
  parallelism: 2
```

With a limit of two and four independent tasks, two run first and the other two start as the first ones finish. Kubernetes capacity limits apply on top. Pods that cannot be scheduled keep their nodes in the pending phase.

## Reading the status of a DAG

The DAG itself is a node of type `DAG`, and each task is a node of type `Pod` or a structure node. The phase of the DAG node follows its tasks. Read them in this order:

1. Find the tasks that are not `Succeeded`.
2. Decide for each one whether it failed, was skipped by `when` or was omitted by `depends`.
3. For a failed task, read its pod events and logs.
4. For an omitted task, read the `depends` expression and the results of the tasks it names.

A task that shows `Omitted` is not a fault by itself. It means that the graph decided not to run it.

## Choosing between steps and DAG

Both compose templates. Steps fit a short linear pipeline where the order is the list order. A DAG fits work with many branches or joins, because each task names its own prerequisites and the controller starts everything that is ready.

## Retries inside a DAG

A task can use a template with a `retryStrategy`. The DAG sees one task, and the retry attempts are nodes below it. Downstream tasks wait until the task has its final result, so a retry that finally succeeds lets the join continue as if the task had succeeded the first time.

## Common pitfalls

> [!WARNING]
> An output reference without a matching dependency is not ordered. A skipped or omitted task has no output, so its reference is empty. Fail-fast does not stop running pods and it does not roll back finished work.
