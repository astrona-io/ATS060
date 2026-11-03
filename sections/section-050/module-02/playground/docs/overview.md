---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Playground: Conditional Tasks And Fan-Out

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository and the `workflow-runner` ServiceAccount in the `starfleet` namespace. No learner Workflow exists at the start.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-050-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-050-02`.

Use it to run conditional branches and loops. The environment is private and disposable. It is not graded.
