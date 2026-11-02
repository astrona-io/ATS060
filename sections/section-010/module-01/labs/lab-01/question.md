---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Run A Workflow Through The Executor

Execute a Workflow and read its real output parameter.

## Starting state

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-010-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-010-01-01" || exit 1
node_name="astro-ats-060-lab-010-01-01-control-plane"
worker_name="astro-ats-060-lab-010-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

Use the provided ServiceAccount. The controller creates Pods and the executor reports result parameters. Inspect Workflow nodes and their Pod names; a submitted resource is not a completed run.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
