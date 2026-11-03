---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Pass A Script Result Between Steps

Compose a script template and a container template with a steps template and pass the printed text between them.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `bridge` name must be printed in upper case and recorded as a result.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-030-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-030-02-01" || exit 1
```

## Required result

Create a Workflow named `compose` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline` and `activeDeadlineSeconds: 180`. The entrypoint is a `steps` template with two steps in order. Step `shout` calls a `script` template that prints `BRIDGE` (the word `bridge` in upper case). Step `record` calls a `container` template with the input parameter `value`, set from the `result` of the `shout` step. It writes the value to `/tmp/result` and exposes it as the output parameter `result`. The run must succeed.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
