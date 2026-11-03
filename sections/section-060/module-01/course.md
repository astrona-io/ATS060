---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Data Processing Pipelines

This module covers the shape of a data processing job in Argo Workflows: input identity, partitioning, parallel processing, joining and safe repetition.

## Learning Goals

- Describe the stages of a pipeline and the data contract between them.
- Create parts with withItems and withParam.
- Join part results and detect a missing part.
- Explain why retries need idempotent work.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Pipeline Shape: Input Identity, Partitioning And Fan-Out
2. Aggregation, Retries And Reproducible Results
3. Guided Practice: Partition, Process And Join
4. Summary

<!-- astrona:playground -->
