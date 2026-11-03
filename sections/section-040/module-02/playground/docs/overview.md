---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Playground: Resources, Identity, Placement And Status

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository and the `workflow-runner` ServiceAccount in the `starfleet` namespace. No learner Workflow exists at the start.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-040-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-040-02`.

Use it to run workflows with resource settings, volumes and failing nodes. The environment is private and disposable. It is not graded.
