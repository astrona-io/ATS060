---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Playground: Artifact Sources, Archive Options And Cleanup

This private kind cluster has the Argo Workflows controller, a MinIO artifact repository (bucket `my-bucket`) and the `workflow-runner` ServiceAccount and `my-minio-cred` Secret in the `starfleet` namespace.

Select the cluster with `export KUBECONFIG="$(astrona kubeconfig ats-060-playground-020-02)"` and check that `kubectl config current-context` prints `kind-astro-ats-060-playground-020-02`.

Use it to run workflows with raw, from and archive options and to read the stored artifact references from the node status. The environment is private and disposable. It is not graded.
