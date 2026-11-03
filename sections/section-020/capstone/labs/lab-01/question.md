---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Build A Three-Step Artifact Pipeline With Cleanup Policy

Build a pipeline that generates, transforms and consumes artifacts with an explicit key and a garbage collection policy.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `probe` data must move through three steps and one result must stay in the repository.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-020-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-020-01" || exit 1
```

## Required result

Create a Workflow named `data-flow` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline` and `activeDeadlineSeconds: 240`. The entrypoint is a `steps` template with three steps run in order. Step `generate` writes `probe data` to `/tmp/source` and stores it as the output artifact `source` with default packing. Step `transform` receives it with `from` at `/tmp/in`, writes the upper case text to `/tmp/final` and stores it as the output artifact `final` with `archive.none` and the S3 key `{{workflow.name}}/final.txt`. Step `summarise` receives `final` with `from` at `/tmp/final` and writes its content to `/tmp/result`, exposed as the output parameter `result`. Set the workflow artifact garbage collection strategy to `OnWorkflowDeletion` with the ServiceAccount `workflow-runner`, and keep the `final` artifact with its own strategy `Never`. The run must succeed.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
