---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Reusable WorkflowTemplate And ClusterWorkflowTemplate Definitions

This module covers stored workflow definitions: the namespaced WorkflowTemplate, the cluster-scoped ClusterWorkflowTemplate, the two kinds of reference, and who may create and use them.

## Learning Goals

- Separate a reusable definition from its execution.
- Choose between workflowTemplateRef and templateRef.
- Execute a namespace Workflow from a cluster-scoped reusable definition.
- Explain what is copied into a run and who needs which permission.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. WorkflowTemplate Definitions And References
2. ClusterWorkflowTemplate, Scope And Access
3. Guided Practice: Instantiate A Reusable WorkflowTemplate
4. Summary

<!-- astrona:playground -->
