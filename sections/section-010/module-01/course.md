---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Workflow Resources, Templates And Execution Ownership

This module explains the objects that Argo Workflows adds to Kubernetes, the templates that define work, and the components that turn a Workflow into running pods and a recorded status.

## Learning Goals

- Distinguish a Workflow execution from its reusable templates.
- Explain controller, pod and executor responsibilities.
- Interpret entrypoint, arguments and node status.
- Evaluate identity and cleanup independently of execution success.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Workflow Resources And Templates
2. Controller, Pods And Executor
3. Guided Practice: Run A Workflow Through The Executor
4. Summary

<!-- astrona:playground -->
