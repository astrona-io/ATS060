---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Summary

A Workflow declares an execution using templates, inputs and an entrypoint. The controller reconciles that intent into supported tasks and records their status, while Pods and executors perform the actual work.

Reusable definitions and individual runs have different lifecycles. Permissions, artifacts and cleanup require explicit design, and completion evidence does not establish that every side effect or retained output satisfies the business requirement.
