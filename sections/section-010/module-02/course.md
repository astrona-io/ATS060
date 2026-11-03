---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Running And Inspecting Workflows

This module covers how a Workflow is submitted, how arguments change a run, where the results of a run are stored, and which fields control the cleanup of pods and Workflow objects.

## Learning Goals

- Submit a Workflow with kubectl and name the argo tool commands for the same job.
- Override workflow arguments and explain where parameter tags are replaced.
- Find status, output parameters and logs of a finished run.
- Choose ttlStrategy and podGC values for a stated retention need.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Submitting Workflows And Setting Parameters
2. Observing Results And Cleaning Up
3. Guided Practice: Parameters, Results And Retention
4. Summary

<!-- astrona:playground -->
