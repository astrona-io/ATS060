---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Run A Locked Partition-Process-Join Pipeline

Build a pipeline that lists parts at run time, processes them in parallel under a mutex and joins the results.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `batch-run` pipeline must produce three parts and join exactly three results.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-060-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-060-01" || exit 1
```

## Required result

Create a Workflow named `batch-run` in `starfleet` with the label `dataset: survey-2026-01`, the `workflow-runner` ServiceAccount, the entrypoint `main`, `activeDeadlineSeconds: 300`, `parallelism: 2` and a workflow mutex named `batch-lock` under `synchronization`. The entrypoint is a `steps` template with three groups. Step `list` runs a `script` template that prints the JSON array `["alpha","beta","gamma"]`. Step `process` runs a template named `produce` for each element with `withParam` on the result of `list`, passes `{{item}}` as the input parameter `item` and prints a JSON object with the key `part` set to the upper case item. The `produce` template has a `retryStrategy` with `limit: "1"`. Step `combine` receives the aggregated result of `process`, parses it as JSON and prints `parts:` and the number of parts. The run must succeed with three processed parts and `parts: 3` as the result of the join.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
