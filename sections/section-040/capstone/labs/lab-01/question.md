---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Bound A Survey Run With Argument, Retry, Deadline And Cleanup

Combine an argument, a retry, two deadlines, a parallelism limit, a resource request and a cleanup policy in one workflow.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The first `survey` attempt fails on purpose and the retry must finish the work.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-040-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-040-01" || exit 1
```

## Required result

Create a Workflow named `survey-run` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `survey`, `activeDeadlineSeconds: 240`, `parallelism: 1` and `ttlStrategy.secondsAfterCompletion: 3600`. Set the argument `ship` to `voyager`. The `survey` template has `activeDeadlineSeconds: 120`, a `retryStrategy` with `limit: "2"` and `retryPolicy: OnFailure`, and a container that requests `50m` CPU and `32Mi` memory. The container exits with code 3 on attempt zero (read the tag `{{retries}}`). On a later attempt it writes the value of the workflow parameter `ship` to `/tmp/result`, exposed as the output parameter `result`. The run must succeed after a failed first attempt.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
