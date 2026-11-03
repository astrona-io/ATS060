---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Summary

Every template has a name and exactly one type field. The container and script types run code in a pod. The resource type changes a Kubernetes object and needs RBAC permission for its action. The suspend type pauses the workflow without a pod. The standard output of a script template becomes the output result of its node, and it is limited in size.

A steps template runs outer groups in order and the steps inside a group in parallel. A step passes values in with arguments and reads values from earlier groups with the steps outputs tags. A steps template can expose an output of its inner steps. A step can call a template from a WorkflowTemplate with templateRef or define a one-off template with inline.

The steps type fits linear pipelines with a few parallel groups. A graph with many dependencies is clearer as a DAG. A workflow that waits in a suspend step stays Running and needs an owner or a deadline.

<!-- astrona:playground:destroy -->
