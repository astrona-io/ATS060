---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Summary

A data pipeline selects an input, partitions it, processes the parts and combines the results. A reproducible run records which input it used and writes output under keys that contain the run and part names. The withItems field takes a list known at authoring time and withParam takes a JSON array that an earlier step printed, so the number of nodes can be decided at run time. The parallelism limit caps nodes of one workflow and not the load on external services.

The join must check that every expected part arrived, and a missing part must fail it or be reported. A retry repeats external writes, so the work needs to be idempotent. Staging output stays apart from published output until the join and its checks pass. A Succeeded phase shows exit codes and not valid data, so record the input identity and check the counts.

<!-- astrona:playground:destroy -->
