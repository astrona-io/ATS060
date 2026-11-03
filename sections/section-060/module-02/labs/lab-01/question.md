---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Schedule A Nightly Scan Without Overlap

Create a CronWorkflow with a time zone, a concurrency policy and history limits.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `nightly-scan` schedule must not start a second run while one is active.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-060-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-060-02-01" || exit 1
```

## Required result

Create a CronWorkflow named `nightly-scan` in `starfleet` with the single schedule `0 3 * * *`, the time zone `UTC`, `concurrencyPolicy: Forbid`, `startingDeadlineSeconds: 120`, `successfulJobsHistoryLimit: 2` and `failedJobsHistoryLimit: 1`. Its `workflowSpec` uses the `workflow-runner` ServiceAccount, the entrypoint `main` and `activeDeadlineSeconds: 180`, and one container template `main` that prints `scan`. Do not suspend the schedule.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
