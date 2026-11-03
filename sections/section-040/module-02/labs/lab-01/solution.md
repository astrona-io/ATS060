---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Run A Workflow With Resources And A Pod Volume Solution

Use the private kubeconfig for this environment.

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-lab-040-02-01)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-lab-040-02-01" || exit 1
```

Save this as `workflow-resourced.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: resourced
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: write
  activeDeadlineSeconds: 180
  volumes:
  - name: scratch
    emptyDir: {}
  templates:
  - name: write
    container:
      image: docker.io/library/python:3.13-alpine
      command:
      - python
      - -c
      args:
      - "open('/work/note','w').write('logged'); open('/tmp/result','w').write(open('/work/note').read())"
      resources:
        requests:
          cpu: 50m
          memory: 32Mi
        limits:
          cpu: 200m
          memory: 64Mi
      volumeMounts:
      - name: scratch
        mountPath: /work
    outputs:
      parameters:
      - name: result
        valueFrom:
          path: /tmp/result
```

Apply it:

```sh
kubectl apply -f workflow-resourced.yaml
```

Then wait for the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/resourced --timeout=240s
```

## Check the result

Read the phase and the node results that the grader uses:

```sh
kubectl -n starfleet get workflow resourced -o yaml
```

The task is complete when the object has the required fields and the controller has recorded the required node results.
