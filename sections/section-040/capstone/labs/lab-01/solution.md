---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Bound A Survey Run With Argument, Retry, Deadline And Cleanup Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-capstone-040-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-capstone-040-01" || exit 1
```

Save this as `workflow-survey-run.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: survey-run
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: survey
  activeDeadlineSeconds: 240
  parallelism: 1
  ttlStrategy:
    secondsAfterCompletion: 3600
  arguments:
    parameters:
    - name: ship
      value: voyager
  templates:
  - name: survey
    activeDeadlineSeconds: 120
    retryStrategy:
      limit: "2"
      retryPolicy: OnFailure
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - 'import sys; attempt=int("{{retries}}"); sys.exit(3) if attempt==0 else open("/tmp/result","w").write("{{workflow.parameters.ship}}")'
      resources:
        requests:
          cpu: 50m
          memory: 32Mi
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-survey-run.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/survey-run --timeout=300s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow survey-run -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
