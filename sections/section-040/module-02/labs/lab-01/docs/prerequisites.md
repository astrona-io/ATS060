---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Prerequisites

Use astrona, kubectl, kind, Python 3, Podman, curl and a shell. The environment is a private kind cluster with the Argo Workflows controller and a MinIO artifact repository installed.

Use a host shell with the private kubeconfig for this environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-040-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-040-02-01" || exit 1
```
