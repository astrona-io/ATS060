---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Playground: Template Types And Composition

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository and the `workflow-runner` ServiceAccount in the `starfleet` namespace. No learner Workflow exists at the start.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-030-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-030-02`.

Use it to compose steps, read script results and try a suspend step. The environment is private and disposable. It is not graded.
