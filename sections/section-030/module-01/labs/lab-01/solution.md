---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Instantiate A Reusable WorkflowTemplate Solution

Use a host shell with the private kubeconfig for this independent kind environment. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-030-01-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-030-01-01" || exit 1
node_name="astro-ats-060-lab-030-01-01-control-plane"
worker_name="astro-ats-060-lab-030-01-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

Create mission-template, then mission with workflowTemplateRef. The execution must expose the expected result; template presence alone does not pass.

Save this as `workflowtemplate-mission-template.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: mission-template
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: produce
  activeDeadlineSeconds: 180
  templates:
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
---
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: mission
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  workflowTemplateRef:
    name: mission-template
```

Apply the scoped correction:

```sh
kubectl apply -f workflowtemplate-mission-template.yaml
```

## Verify The Result

Observe the actual result. A denied request returns a nonzero status when the denial works, so run it separately from a shell sequence that stops on error. Status convergence and a successful request establish different parts of the result.

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/mission --timeout=240s
```

Separate a reusable definition from its execution. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.

After recording your result, remove the independent lab with `astrona destroy ats-060-lab-030-01-01`.

## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
