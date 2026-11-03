---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Guided Practice: Run A Workflow Through The Executor

Use a host shell with the private kubeconfig for this module playground. A kubeconfig identifies the cluster and credentials used by kubectl, the Kubernetes command-line tool.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-010-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-010-01" || exit 1
node_name="astro-ats-060-playground-010-01-control-plane"
worker_name="astro-ats-060-playground-010-01-worker"
```

Keep this connection selected. Host-level commands name only this environment's node containers. They do not operate on the host operating system.

## Inspect And Explain

The Workflows controller and an internal disposable artifact store are installed. The workflow-runner ServiceAccount can create executor results. No learner Workflow exists. Artifact credentials are private fixture credentials.

Inspect the current objects before changing them:

```sh
kubectl -n starfleet get pods -o wide
kubectl get nodes -o wide
```

Use the provided ServiceAccount. The controller creates Pods and the executor reports result parameters. Inspect Workflow nodes and their Pod names; a submitted resource is not a completed run.

Save this as `workflow-mission.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: mission
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

Execute a Workflow and read its real output parameter. The commands above deliberately target one environment. Keep its remaining components available so an unrelated failure cannot stand in for the required denial or correction. No example command output is presented as evidence of a completed run. A matching field alone does not establish that a process used it or that a controller reconciled it.



## Read The Node Results

After the Workflow succeeds, read the result from the node that ran the container. The `status.nodes` map is keyed by node id, so list the fields you need with a template:

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{.status.phase}{"\n"}'
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{"\n"}{end}'
```

The first command prints the phase of the whole run. The second prints one line for each node with its display name, its type and its phase. A workflow with one `container` template has one node of type `Pod`. Next, read the output parameter that the executor reported:

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.outputs.parameters}{"\n"}{end}'
```

The value is the content of `/tmp/result` from the container. The controller copied it from a `WorkflowTaskResult`, so it appears only after the `wait` container reported it. List the pods of the run to see the pod that the controller created:

```sh
kubectl -n starfleet get pods -l workflows.argoproj.io/workflow=mission
```

## Common pitfalls

> [!WARNING]
> Confirm the private context and exact node names before a change. Check the stated scope and live result. Do not change unrelated components to hide the original fault.
