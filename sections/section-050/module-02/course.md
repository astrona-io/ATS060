---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Conditional Tasks And Fan-Out

This module covers tasks that run only when a condition holds and tasks that run once for every item of a list.

## Learning Goals

- Choose between when and depends for a condition.
- Distinguish Skipped from Omitted.
- Build a two-branch choice with a join.
- Use withItems, withParam and withSequence and explain aggregation.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Conditional Tasks With When And Depends
2. Fan-Out With Loops And Aggregation
3. Guided Practice: Conditional Branches And A Fan-Out
4. Summary

<!-- astrona:playground -->
