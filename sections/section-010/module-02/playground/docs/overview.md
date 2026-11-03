---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Playground: Running And Inspecting Workflows

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository and the `workflow-runner` ServiceAccount in the `starfleet` namespace. No learner Workflow exists at the start.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-010-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-010-02`.

Use the playground to create Workflows with different arguments, read the status of each node, and compare the effect of `ttlStrategy` and `podGC`. This environment is private and disposable. It is not graded.
