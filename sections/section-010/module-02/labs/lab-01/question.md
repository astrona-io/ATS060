---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Report An Overridden Argument With Cleanup

Run a Workflow whose argument is set to a chosen value and which cleans up after itself.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The shuttle crew needs one report run. The report text is the parameter `message`.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-010-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-010-02-01" || exit 1
```

## Required result

Create a Workflow named `launch-report` in `starfleet`. It uses the `workflow-runner` ServiceAccount, the entrypoint `report` and `activeDeadlineSeconds: 180`. Set the workflow argument `message` to `launch-approved`. The `report` template writes the value of its `message` input to `/tmp/result` and exposes that file as the output parameter `result`. The workflow must delete its pods when the workflow completes (`podGC` strategy `OnWorkflowCompletion`) and delete itself 3600 seconds after completion (`ttlStrategy.secondsAfterCompletion`). The run must reach the phase `Succeeded`.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
