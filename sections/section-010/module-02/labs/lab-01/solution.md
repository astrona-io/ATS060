---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Report An Overridden Argument With Cleanup Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-010-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-010-02-01" || exit 1
```

Save this as `workflow-launch-report.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: launch-report
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: report
  activeDeadlineSeconds: 180
  arguments:
    parameters:
    - name: message
      value: launch-approved
  ttlStrategy:
    secondsAfterCompletion: 3600
  podGC:
    strategy: OnWorkflowCompletion
  templates:
  - name: report
    inputs:
      parameters:
      - name: message
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - open("/tmp/result","w").write("{{inputs.parameters.message}}")
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-launch-report.yaml
```

Then wait for the run:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/launch-report --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow launch-report -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
