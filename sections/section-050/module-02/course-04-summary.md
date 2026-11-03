---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Summary

The when field tests a value and marks the task Skipped when the test is false. The depends field tests task results and marks the task Omitted when the test is false. Skipped and omitted nodes create no pod and have no outputs. A join of alternative branches needs a depends expression, because the dependencies list requires every listed task to succeed.

A loop field creates one node for each item. The withItems field takes a known list, withParam takes a JSON array from a parameter or an earlier task, and withSequence takes a count. The outputs of all iterations can be read as one JSON array when each prints valid JSON. A parallelism limit controls how many iterations run together.

<!-- astrona:playground:destroy -->
