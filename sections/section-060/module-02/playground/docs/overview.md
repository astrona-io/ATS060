---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Playground: Scheduled And Controlled Pipeline Runs

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository and the `workflow-runner` ServiceAccount in the `starfleet` namespace. No learner Workflow exists at the start.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-060-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-060-02`.

Use it to run a schedule and to try a mutex. The environment is private and disposable. It is not graded.
