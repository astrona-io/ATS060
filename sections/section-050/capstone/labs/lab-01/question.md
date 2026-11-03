---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Build A Branching DAG With A Fan-Out And A Join

Combine a when branch, a withItems fan-out, a depends join and a parallelism limit in one DAG.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `route-plan` scan must choose the proceed branch and survey three sectors.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-050-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-050-01" || exit 1
```

## Required result

Create a Workflow named `route-plan` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline`, `activeDeadlineSeconds: 300` and `parallelism: 2`. The entrypoint is a `dag` template. Task `scan` runs a `script` template that prints `clear`. Tasks `proceed` and `hold` depend on `scan` and have opposite `when` conditions on its result (`== clear` and `!= clear`). Task `survey` depends on `scan` and runs a container template once for each of the items `alpha`, `beta` and `gamma` with `withItems`, passing `{{item}}` as the parameter `sector`. Task `report` uses `depends: (proceed || hold) && survey` and no `dependencies` field. The run must succeed with `hold` skipped, three survey nodes succeeded and `report` started after all of them finished.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
