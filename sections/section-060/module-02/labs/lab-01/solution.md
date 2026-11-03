---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Schedule A Nightly Scan Without Overlap Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-060-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-060-02-01" || exit 1
```

Save this as `cronworkflow-nightly-scan.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: nightly-scan
  namespace: starfleet
spec:
  schedules:
  - 0 3 * * *
  timezone: UTC
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 120
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  workflowSpec:
    serviceAccountName: workflow-runner
    entrypoint: main
    activeDeadlineSeconds: 180
    templates:
    - name: main
      container:
        image: docker.io/library/python:3.13-alpine
        command:
        - python
        - -c
        args:
        - print('scan')
```

Apply it:

```sh
kubectl apply -f cronworkflow-nightly-scan.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet get cronworkflow nightly-scan
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get cronworkflow nightly-scan -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
