---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Template Types And Composition

This module covers the template types that do work, the types that combine them, and how parameters and outputs move between templates.

## Learning Goals

- Select container, script, resource or suspend for a stated task.
- Compose templates with steps and pass parameters between steps.
- Read the output of a script template and expose an output from a steps template.
- Use templateRef and inline templates and explain when each fits.

## Before You Start

You need basic `kubectl` skills and the idea of a Kubernetes pod. The module playground is a private kind cluster with Argo Workflows installed. The hands-on steps start the playground when you reach them.

## Reading Order

1. Template Types
2. Composing Templates With Steps And Parameters
3. Guided Practice: Script Templates And Steps
4. Summary

<!-- astrona:playground -->
