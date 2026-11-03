---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# DAG Tasks, Dependencies And Depends Expressions

A DAG is a directed acyclic graph: tasks are the nodes, dependencies are the edges, and no path of edges leads back to the same task. In Argo Workflows, a `dag` template lists tasks and states what each task waits for. This part explains how the controller decides when a task may start.

## A DAG template

```yaml
templates:
- name: pipeline
  dag:
    tasks:
    - name: prepare
      template: step
    - name: east
      template: step
      dependencies: [prepare]
    - name: west
      template: step
      dependencies: [prepare]
    - name: combine
      template: step
      dependencies: [east, west]
```

A task has a `name`, a `template` to run and optional `arguments`. The tasks `east` and `west` both wait for `prepare`, and they do not wait for each other, so the controller can start them together. The task `combine` waits for both. This shape is called a diamond.

Order in the list does not matter. A task with no dependency is eligible at once, even if it is listed last. Only the dependency fields create an order.

## How the controller decides

The controller checks the DAG repeatedly. A task becomes eligible when all tasks it depends on have finished and the dependency condition is true. It then creates a node for the task and, for a container or script template, a pod. If a dependency never becomes true, the task is marked `Omitted` and its pod never exists.

Eligible is not the same as running. The pod still needs a node with free capacity, an image and permissions, and the workflow `parallelism` limit can hold it back.

## Two dependency fields

The plain form is `dependencies`, a list of task names. It means that every listed task must have succeeded.

The enhanced form is `depends`, a string with an expression. A task may use one of the two fields, and a task cannot use both:

```yaml
- name: report
  template: step
  depends: "east.Succeeded && west.Succeeded"
```

The expression names a task and a result, joined by a dot. The results are:

- `Succeeded` means the task finished without error.
- `Failed` means the task exited with a non-zero code.
- `Errored` means the task had an error other than a non-zero exit code.
- `Skipped` means the task's `when` condition was false.
- `Omitted` means the task's own `depends` condition was false.
- `Daemoned` means a daemon task is running and is no longer pending.

The operators are `&&` for both, `||` for either and `!` for not. Parentheses group terms. A name without a result is a shortcut. The expression `east` means `east.Succeeded || east.Skipped || east.Daemoned`.

## Using depends to run after a failure

With `dependencies`, a failure upstream means that the downstream task never runs. With `depends`, you can choose:

```yaml
- name: collect-logs
  template: step
  depends: "build.Failed"
- name: publish
  template: step
  depends: "build.Succeeded"
```

Here `collect-logs` runs only when `build` fails, and `publish` runs only when it succeeds. The one that does not match is marked `Omitted`. A task with an expression such as `build.Succeeded || build.Failed` runs after `build` in both cases, which fits a cleanup task.

## Reading the result from the status

Each task is a node in `.status.nodes` with a `displayName` equal to the task name, a `phase` and the times `startedAt` and `finishedAt`. A dependency was honored when the finish time of the earlier node is not later than the start time of the later node. The declaration order proves nothing.

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.startedAt}{" "}{.finishedAt}{"\n"}{end}'
```

## Cycles and unknown names

A task that depends on itself, directly or through other tasks, forms a cycle. No task in the cycle could ever be first, so the controller rejects the workflow. A dependency on a name that is not in the list is rejected as well.

## Common pitfalls

> [!WARNING]
> Do not use dependencies and depends in the same task. Listing a task later in the file does not make it run later. The shortcut form of a depends expression also accepts a skipped task, which can be wider than you intend.
