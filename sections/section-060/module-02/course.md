---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Scheduled And Controlled Pipeline Runs

This module covers running a pipeline on a timetable with CronWorkflow and limiting overlap across runs with mutexes and semaphores.

## Learning Goals

- Write a CronWorkflow with a schedule, a policy and history limits.
- Choose a concurrency policy for a stated pipeline.
- Use mutexes and semaphores to limit overlapping runs.
- Read the status of a waiting workflow.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Scheduled Runs With CronWorkflow
2. Safe Repeated Runs With Synchronization
3. Guided Practice: A Schedule And A Mutex
4. Summary

<!-- astrona:playground -->
