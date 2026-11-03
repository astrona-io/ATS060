---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Summary

A dag template lists tasks and the tasks each one waits for. Independent tasks start together, and the list order creates no order. The dependencies field requires every listed task to succeed. The depends field takes an expression over results such as Succeeded, Failed, Skipped and Omitted, with the operators and, or and not. A task cannot use both fields.

A task reads another task output with the tasks outputs tags, and the reading task must also depend on the producer. A skipped or omitted task has no output. By default a DAG fails fast and schedules no new tasks after a failure, and failFast set to false lets other branches finish. The parallelism fields limit concurrent nodes.

<!-- astrona:playground:destroy -->
