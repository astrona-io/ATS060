---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Summary

The entrypoint names the first template, and only templates reachable from it run. Workflow-level arguments are read with the workflow parameters tag, and a template reads its own inputs with the inputs tag. The controller replaces tags before the pod is created, so containers receive plain text. The API server checks the schema, and the controller checks references, but image pulls, capacity and permissions show up only when the pod starts.

Four groups of fields bound a run. A retryStrategy runs a failed node again and repeats every external effect. An activeDeadlineSeconds value stops work that runs too long and does not undo effects. The parallelism field limits concurrent nodes of one workflow. The ttlStrategy field deletes the workflow object and podGC deletes pods, and deleting pods removes their logs.

<!-- astrona:playground:destroy -->
