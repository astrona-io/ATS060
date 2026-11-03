---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Summary

A request is reserved by the scheduler, and a limit is a runtime ceiling. A pod with a request that no node can satisfy stays Pending without a workflow error. The ServiceAccount is the identity of the pod, and the wait container needs it to report task results. Placement fields such as nodeSelector and tolerations decide eligible nodes, and an emptyDir volume lives only as long as one pod.

The workflow phase Failed means a node ran and failed, and Error means the controller or executor could not do its work. Read the first failing Pod node, its events and the main container logs. The status keeps node results after pod cleanup, while logs are gone unless they were archived. A Succeeded phase proves exit codes, not correct data.

<!-- astrona:playground:destroy -->
