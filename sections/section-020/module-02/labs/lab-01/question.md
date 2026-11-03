---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Stage A Raw Input Without Packing

Store a raw input as an unpacked artifact under a chosen key and pass it to a second step.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `bridge` roster is a short text that must be stored as a plain object.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-020-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-020-02-01" || exit 1
```

## Required result

Create a Workflow named `staging` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline` and `activeDeadlineSeconds: 180`. The entrypoint is a `steps` template with two steps run in order. Step `stage` uses a template `stage` with a raw input artifact `note` (path `/tmp/note`, data `crew-roster`). It copies the file to `/tmp/staged` and stores it as the output artifact `staged` with `archive.none` and the S3 key `{{workflow.name}}/staged.txt`. Step `read` receives `staged` with `from`, reads it at `/tmp/input` and writes the text to `/tmp/result`, exposed as the output parameter `result`. The run must succeed.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
