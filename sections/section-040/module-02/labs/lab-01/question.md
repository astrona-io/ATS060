---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Run A Workflow With Resources And A Pod Volume

Set resource requests and limits, mount an emptyDir volume and expose a value read from it.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `resourced` run must stay inside a small resource budget.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-040-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-040-02-01" || exit 1
```

## Required result

Create a Workflow named `resourced` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `write` and `activeDeadlineSeconds: 180`. Declare an `emptyDir` volume named `scratch` in the spec. The `write` template runs one container that mounts `scratch` at `/work` and requests `32Mi` memory and `50m` CPU with the limits `64Mi` memory and `200m` CPU. It writes `logged` to `/work/note`, copies the content to `/tmp/result` and exposes it as the output parameter `result`. The run must succeed.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
