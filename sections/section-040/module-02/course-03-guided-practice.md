---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Guided Practice: Resources, Volumes And Status Evidence

In this session you run a workflow with resource settings and a pod volume, read its status node by node, and then create a pod that cannot be scheduled so that you can read a pending node. The playground is separate from the graded task.

## Select the playground cluster

A kubeconfig identifies the cluster and credentials that `kubectl`, the Kubernetes command-line tool, uses. Select the private cluster of this playground and check the context.

<!-- astrona:playground:renew -->

```sh
export KUBECONFIG="$(astrona kubeconfig ats-060-playground-040-02)"
test "$(kubectl config current-context)" = "kind-astro-ats-060-playground-040-02" || exit 1
kubectl -n argo get deployment workflow-controller
```

The controller must be available before you create a Workflow.

## Run a workflow with resources and a volume

Save this as `workflow-resourced.yaml`. The container has a request and a limit, and it writes a file to an `emptyDir` volume and then exposes the content as an output parameter:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: resourced-one
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
      command: [python, -c]
      args: ["open('/work/note','w').write('logged'); open('/tmp/result','w').write(open('/work/note').read())"]
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

Then check the result:

```sh
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/resourced-one --timeout=240s
kubectl -n starfleet get workflow resourced-one -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{" "}{.outputs.parameters}{"\n"}{end}'
```

The node of type `Pod` carries the output parameter `result`. Check the pod spec to see that the controller passed your settings through:

```sh
kubectl -n starfleet get pod -l workflows.argoproj.io/workflow=resourced-one -o jsonpath='{.items[0].spec.containers[?(@.name=="main")].resources}{"\n"}'
```

## Read a pending node

Save this as `workflow-pending.yaml`. The request is much larger than a small test node can offer, so the pod cannot be scheduled. The workflow deadline ends the run after 60 seconds:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: pending-one
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: heavy
  activeDeadlineSeconds: 60
  templates:
  - name: heavy
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('never runs')"]
      resources:
        requests:
          memory: 4000Gi
```

Apply it:

```sh
kubectl apply -f workflow-pending.yaml
```

Then check the evidence. The pod stays in `Pending` until the deadline fires:

```sh
kubectl -n starfleet get pod -l workflows.argoproj.io/workflow=pending-one
kubectl -n starfleet describe pod -l workflows.argoproj.io/workflow=pending-one
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Failed workflow/pending-one --timeout=180s
```

In the events of the pod, find the scheduling message that names the missing resource. Compare it with the workflow message, which names the deadline and not the cause.

## Clean up the examples

```sh
kubectl -n starfleet delete workflow resourced-one pending-one
```

## Reason about what you saw

The resource settings appeared unchanged in the pod, so the controller passes them through. The volume existed only inside the pod, and the output parameter was the way the value left it. The pending run failed because of the deadline, while the real cause was in the pod events. This is why you read node messages and pod events together.

## Common pitfalls

> [!WARNING]
> Confirm the private context before every change. Do not read the workflow message as the cause of a pending pod. The cause is in the pod events. Delete the example workflows when you finish.
