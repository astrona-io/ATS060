---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Artifact Sources, Archive Options And Cleanup

This module covers where input artifacts can come from, how outputs are packed and keyed, and how stored artifacts and logs are cleaned up or kept.

## Learning Goals

- Select an input artifact source for a stated need: from, raw, http, git or s3.
- Set archive, key, mode and optional on artifacts.
- Configure artifact garbage collection and explain its finalizer and permissions.
- Save container logs with archiveLogs and combine retention settings.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Input Sources And Archive Options
2. Artifact Garbage Collection And Log Archiving
3. Guided Practice: Raw Inputs, Archive Options And Passing Artifacts
4. Summary

<!-- astrona:playground -->
