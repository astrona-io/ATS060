---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Conditional Tasks With When And Depends

A conditional task runs only when a stated condition holds. Argo Workflows has two places for a condition: the `when` field on a task, which tests a value, and the `depends` field, which tests the result of other tasks. They answer different questions and mark skipped work differently.

## The when field

`when` holds an expression that the controller evaluates after the dependencies of the task are met. The expression can use tags, so it can test the output of an earlier task:

```yaml
dag:
  tasks:
  - name: check
    template: check
  - name: launch
    template: act
    dependencies: [check]
    when: "{{tasks.check.outputs.result}} == green"
  - name: abort
    template: act
    dependencies: [check]
    when: "{{tasks.check.outputs.result}} != green"
```

The controller replaces the tag with the text of the output and then evaluates the comparison. Supported operators include `==`, `!=`, `>`, `<`, `&&` and `||`. A string without spaces can be compared as written. A value that contains spaces or special characters needs quotes around the tag.

If the expression is false, the task is not run and its node gets the phase `Skipped`. No pod is created.

## The depends field and results

`depends` tests the outcome of tasks rather than their data. It can name `Succeeded`, `Failed`, `Skipped`, `Omitted` and the other results. Use it to say what should happen after a branch:

```yaml
- name: report
  template: act
  depends: "launch || abort"
```

The shortcut `launch` accepts `Succeeded`, `Skipped` and `Daemoned`. For the two branches above exactly one is run and the other is skipped, so `report` is eligible as soon as both have a final state. The same task with `dependencies: [launch, abort]` would not behave this way, because that form requires both tasks to succeed.

## Skipped and Omitted

| Phase | Cause |
| --- | --- |
| Skipped | The `when` condition was false. |
| Omitted | The `depends` condition was false. |

Both nodes have no pod and no outputs. A later task that reads their outputs receives an empty string.

## Designing a choice between branches

A clear two-branch choice has three parts:

1. A task that produces the decision as an output, usually a short text such as `green` or `red`.
2. Two tasks with opposite `when` conditions that depend on it.
3. A join task whose `depends` expression accepts either branch.

Make the conditions opposite and complete. If the decision can produce a third value, neither branch runs, and the join runs with nothing done. Test the values you expect and decide what the join should do with an unexpected value.

## Conditions on parameters

A `when` can test a workflow parameter too:

```yaml
when: "{{workflow.parameters.mode}} == full"
```

This lets one workflow definition serve several submissions, for example a full run and a quick run, without a second definition.

## What the condition does not do

The condition is evaluated once, when the task becomes eligible. It does not watch the value afterward. It does not stop a task that already runs. It also does not check that the output is valid. A task that printed extra text, such as a trailing space or a new line, can make an equality comparison false. The `outputs.result` of a script template has its final newline trimmed, but other whitespace can remain, so print the decision value without extra text.

## Reading the result

Read the node phases to see which branch ran:

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow gate -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.phase}{"\n"}{end}'
```

The branch that ran is `Succeeded`, and the other branch is `Skipped`. The join is `Succeeded` when its expression accepted the result.

## Common pitfalls

> [!WARNING]
> A false when condition skips the task, and a false depends condition omits it. The two are not the same result. Do not use the dependencies list for a join of alternative branches, because it needs every listed task to succeed.
