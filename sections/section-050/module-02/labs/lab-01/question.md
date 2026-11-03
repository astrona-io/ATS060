---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Choose A DAG Branch With A When Condition

Run one of two branches from a task output and join them with a depends expression.

## Starting state

The Argo Workflows controller and a MinIO artifact repository run in the `argo` namespace. The `workflow-runner` ServiceAccount in `starfleet` can create Workflow task results. The `gate` check must pick the launch branch.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-050-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-050-02-01" || exit 1
```

## Required result

Create a Workflow named `gate` in `starfleet` with the `workflow-runner` ServiceAccount, the entrypoint `pipeline` and `activeDeadlineSeconds: 240`. The entrypoint is a `dag` template with four tasks. Task `check` runs a `script` template that prints `green`. Tasks `launch` and `abort` depend on `check`. Task `launch` has `when: '{{tasks.check.outputs.result}} == green'` and `abort` has the opposite condition with `!=`. Task `report` uses `depends: launch || abort` and no `dependencies` field. All three later tasks run a container template that prints a line. The run must succeed with `launch` succeeded and `abort` skipped.

## Verify The Result

The grader reads the object fields and the observed node status. Wait for the controller to finish the run before you submit. Keep the namespace and the names in the task.
