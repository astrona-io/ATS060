---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Summary

A Workflow spec describes the intended execution graph, inputs and operational constraints. Task images, identity, resources and placement determine whether that intent can run in the cluster.

Retry, timeout and cleanup control different lifecycle decisions. Status records observed progress, while external effects and retained artifacts need their own contracts; accepted YAML and a completed process cannot establish every business outcome.
