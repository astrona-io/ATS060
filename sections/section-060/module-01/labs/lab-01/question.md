---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Fan Out A Bounded Processing Job

Complete three independent processing nodes with bounded concurrency.

## Starting state

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-060-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-060-01-01" || exit 1
node_name="astro-ats-060-lab-060-01-01-control-plane"
worker_name="astro-ats-060-lab-060-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

Use withItems and parallelism two. Verify three successful produce template nodes. These items exercise workflow scheduling; a real data job would replace the deterministic fixture operation.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
