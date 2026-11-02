---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Instantiate A Cluster Scoped Template

Execute a namespace Workflow from a cluster-scoped reusable definition.

## Starting state

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-030-01-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-030-01-02" || exit 1
node_name="astro-ats-060-lab-030-01-02-control-plane"
worker_name="astro-ats-060-lab-030-01-02-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Required result

Use clusterScope true and the namespaced executor ServiceAccount. Explain the ownership and permission difference from a namespaced WorkflowTemplate.

## Verify The Result

The grader checks the required object fields and actual observations. Wait for controller convergence before submitting. Preserve the task's namespace, workload names and unrelated components.
