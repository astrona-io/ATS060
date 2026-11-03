---
draft: true
exam_objectives:
- Work with DAG (Directed-Acyclic Graphs)
---
# Guided Practice: Execute A DAG Dependency

Use a host shell with the private kubeconfig for this module playground. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-050-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-050-01" || exit 1
node_name="astro-ats-060-playground-050-01-control-plane"
worker_name="astro-ats-060-playground-050-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

Use an enhanced depends expression. Inspect the actual node start and finish times; declaration order alone does not create a dependency.

Save this as `workflow-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: mission
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: pipeline
  activeDeadlineSeconds: 180
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: prepare
        template: produce
      - name: finish
        template: produce
        depends: prepare.Succeeded
  - name: produce
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("mission-complete")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply the scoped correction:

```sh
kubectl apply -f workflow-mission.yaml
```

## Verify The Result

Observe the actual result. A denied request returns a nonzero status when the denial works, so run it separately from a shell sequence that stops on error. Status convergence and a successful request establish different parts of the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/mission --timeout=240s
```

Run the finish node only after prepare succeeds. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.


## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
