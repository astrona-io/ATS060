---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# DAG Tasks, Dependencies And Data Flow

This module covers the DAG template: tasks, the two dependency fields, output references, fail-fast and parallelism.

## Learning Goals

- Write a DAG with independent branches and a join.
- Use depends expressions for results other than success.
- Pass outputs between tasks with a matching dependency.
- Explain fail-fast and parallelism limits.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. DAG Tasks, Dependencies And Depends Expressions
2. Data Flow, Fail-Fast And Parallelism In DAGs
3. Guided Practice: A Diamond DAG With Data Flow
4. Summary

<!-- astrona:playground -->
