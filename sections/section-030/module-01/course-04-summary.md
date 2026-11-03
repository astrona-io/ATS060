---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Summary

A WorkflowTemplate stores a definition with the same spec shape as a Workflow and never runs by itself. A Workflow uses it with workflowTemplateRef, which reuses the whole definition, or a step uses templateRef to reuse one template. With workflowTemplateRef the controller stores a copy of the spec in the status of the run, so later edits to the template do not change that run. A templateRef step reads the template when the step starts.

A ClusterWorkflowTemplate is the cluster-scoped kind. A reference to it must set clusterScope to true, otherwise the lookup uses the namespace of the workflow and fails. The controller reads the template, so the workflow pods need no permission on templates. People who create cluster templates need cluster-wide rights, and people who run them need create on workflows in their namespace.

The workflowRestrictions setting of the controller can require workflowTemplateRef so that only approved templates run. Template versions are managed by name and by storing the YAML in version control, because a template has no version field. A change to a cluster template reaches every namespace at the next run.

<!-- astrona:playground:destroy -->
