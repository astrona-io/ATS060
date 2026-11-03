---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Reading The Workflow Spec

This module covers how to read a Workflow spec as a set of execution decisions: where it starts, how values enter, and which controls bound a run.

## Learning Goals

- Read a spec from entrypoint to leaf templates.
- Pass arguments and inputs correctly.
- Choose between retry, deadline, parallelism and cleanup controls.
- Explain what a retry does to external effects.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Workflow Spec Structure: Entrypoint, Templates And Arguments
2. Lifecycle Controls: Retry, Deadline, Parallelism And Cleanup
3. Guided Practice: Arguments, Deadlines And Cleanup
4. Summary

<!-- astrona:playground -->
