---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Compose A Workflow From A Reusable Template Library

Store a reusable template in a WorkflowTemplate and call it from a Workflow with an overridden argument.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `crew-library` template must be stored once and used by a launch workflow.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-030-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-030-01" || exit 1
```

## Required result

Create a WorkflowTemplate named `crew-library` in `starfleet` with the `workflow-runner` ServiceAccount, `activeDeadlineSeconds: 180`, the argument `crew` with the default `apollo`, and one `container` template `announce`. It has the input parameter `name`, writes the value to `/tmp/result` and exposes it as the output parameter `result`. Then create a Workflow named `launch-crew` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `main`, `activeDeadlineSeconds: 180` and the argument `crew` set to `orion`. The entrypoint is a `steps` template with one step `call`. It uses `templateRef` with the template `announce` of `crew-library` and passes `{{workflow.parameters.crew}}` as `name`. The run must succeed and the output result must be `orion`.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
