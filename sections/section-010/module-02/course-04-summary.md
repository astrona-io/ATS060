---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Summary

A Workflow is created with kubectl create, with the argo tool or through the Argo Server. All three create the same object. A Workflow that only has generateName needs create, because apply requires a fixed name. Default arguments live in spec.arguments.parameters, and a submission can override them. The controller replaces the parameter tags before it creates the pod, so the values are visible in the object and must not hold secrets.

A run leaves four kinds of evidence: the Workflow status, the pod logs, stored artifacts and, when configured, the workflow archive. Each has its own lifetime. The ttlStrategy field deletes the Workflow object after a time. The podGC field deletes pods and so deletes their logs. The archiveLogs setting copies logs to the artifact repository.

The ServiceAccount named in the spec is the identity of the pods. A missing task result permission fails a node even when the container exits successfully. Retention settings should match the need to investigate failures, so a common choice keeps failed runs longer than successful ones.

<!-- astrona:playground:destroy -->
