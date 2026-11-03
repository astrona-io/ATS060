---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Resources, Identity, Placement And Status

This module covers the pod-level settings that decide whether a node can start, and how to read the status when a run does not end as planned.

## Learning Goals

- Set requests and limits and explain their different effects.
- Explain the role of the ServiceAccount and of placement fields.
- Use emptyDir and claim volumes correctly.
- Find the first failing node and the evidence for its cause.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Resources, Identity, Placement And Volumes
2. Reading Status And Failure Evidence
3. Guided Practice: Resources, Volumes And Status Evidence
4. Summary

<!-- astrona:playground -->
