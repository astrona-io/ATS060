---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Summary

A Workflow is a Kubernetes custom resource. Its spec is a definition made of templates, arguments and an entrypoint. Its status is the record of one run. A WorkflowTemplate holds only the definition, so changing it affects future runs and never the status of finished runs.

The workflow controller reads Workflow objects and creates one pod for each work node. The pod has an init container, a main container that runs the image, and a wait container that runs the executor. The executor reports outputs through a WorkflowTaskResult object, and the controller copies them into the node entries of the status.

Phases describe progress. A Failed workflow had a node that ran and failed. An Error workflow had a problem outside the application code. A pending node points to scheduling, image or parallelism limits. A Succeeded phase shows that the nodes finished as the templates accept, and it does not prove that an external system holds the right data.

The ServiceAccount of the workflow pods needs permission to create task results, and nothing more than the tasks need. Retries run the work again, so tasks that write outside the cluster must be safe to repeat.

<!-- astrona:playground:destroy -->
