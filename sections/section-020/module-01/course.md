---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Generating, Storing And Consuming Workflow Artifacts

This module explains artifacts: files that tasks produce and consume, how Argo stores them in an artifact repository, and how an output of one task becomes the input of another.

## Learning Goals

- Distinguish artifacts from scalar parameters.
- Trace output files through repository storage and input references.
- Explain repository credentials and where the repository is configured.
- Evaluate missing outputs, wrong paths and repository failures.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Artifacts Compared With Parameters
2. The Artifact Repository
3. Guided Practice: Produce Store And Consume An Artifact
4. Summary

<!-- astrona:playground -->
