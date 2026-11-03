---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Build A Two-Step Report With Retention

Build a two-step workflow that passes a value between templates and sets retention fields.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `bridge` crew needs a report built in two steps.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-010-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-010-01" || exit 1
```

## Required result

Create a Workflow named `fleet-report` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline` and `activeDeadlineSeconds: 240`. Give it the workflow argument `crew` with the value `bridge`. The entrypoint is a `steps` template with two steps run one after the other. Step `prepare` receives `crew`, writes the upper case value to `/tmp/value` and exposes it as the output parameter `value`. Step `publish` receives that output as its input `value`, writes `report:` followed by the value to `/tmp/result` and exposes it as the output parameter `result`. Retention: delete the Workflow 3600 seconds after success and 86400 seconds after failure, and delete only successful pods (`podGC` strategy `OnPodSuccess`). The run must succeed.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
