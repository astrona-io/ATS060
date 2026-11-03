---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Resources, Identity, Placement And Volumes

The fields in this part decide whether a pod that the controller creates can start and what it may touch. They are Kubernetes concepts that the Workflow spec passes through to the pod.

## Resource requests and limits

A container template can set `resources`:

```yaml
templates:
- name: crunch
  container:
    image: docker.io/library/python:3.13-alpine
    command: [python, -c]
    args: ["print('done')"]
    resources:
      requests:
        cpu: 50m
        memory: 32Mi
      limits:
        cpu: 200m
        memory: 64Mi
```

- A request is the amount the scheduler reserves on a node. A pod is placed only on a node with that much unreserved capacity. The unit `m` means one thousandth of a CPU core, and `Mi` means mebibytes.
- A limit is the maximum the container may use. A container that goes over its memory limit is stopped by the kernel, and the node reports the reason `OOMKilled`. A container that goes over its CPU limit is slowed, not stopped.
- A pod whose request is larger than any node can offer stays in the `Pending` phase. The workflow node stays pending too, and no error is raised unless a deadline ends it.

The workflow pod has more containers than the one you wrote. The `init` and `wait` containers are added by the controller and have small default requests. A namespace quota counts all of them.

## Identity: the ServiceAccount

`serviceAccountName` on the spec selects the identity of the pods. The `wait` container uses it to create a WorkflowTaskResult object that reports the outputs of the node. Without that permission the node can finish its work and still be reported as an error. A step that calls the Kubernetes API, for example with a `resource` template, needs more permissions on top of that, which the role bound to the ServiceAccount must grant.

```yaml
spec:
  serviceAccountName: workflow-runner
  automountServiceAccountToken: false
```

The second field stops Kubernetes from mounting the token into the pod. It suits steps that never call the API. The `wait` container needs a token to report results, so check the behavior of your Argo version before you disable it for a whole workflow.

The pod identity is separate from credentials for external systems. A password for a database or a bucket should come from a Kubernetes Secret, which the template reads through `env` with `valueFrom.secretKeyRef`, and never from a visible parameter.

## Placement

Placement fields decide which nodes may run the pod:

- `nodeSelector` is a map of labels. Only nodes that carry all of them are eligible.
- `tolerations` allow the pod on nodes that have a matching taint. A taint repels pods that do not tolerate it.
- `affinity` expresses preferences and rules for nodes or for other pods.
- `priorityClassName` sets the scheduling priority.

They can be set on the workflow spec for all templates or on a single template. If no node matches, the pod stays `Pending` and its events name the reason. The Workflow spec itself is still valid.

## Volumes

Pod volumes give containers a file system that is shared inside the pod. With an `emptyDir` volume, the directory is created when the pod starts and removed when the pod ends:

```yaml
spec:
  volumes:
  - name: scratch
    emptyDir: {}
  templates:
  - name: writer
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["open('/work/note','w').write('logged')"]
      volumeMounts:
      - name: scratch
        mountPath: /work
```

An `emptyDir` volume is private to one pod, so a later step cannot read it. To share files between steps, the workflow needs either artifacts or a volume that outlives the pod. The field `volumeClaimTemplates` creates a PersistentVolumeClaim for the run, and templates mount it by the claim name with `volumeMounts`. The cluster needs a storage class that can provision the claim. The controller deletes claims that it created when the workflow completes.

## Fields that look related but are not

| Field | What it controls |
| --- | --- |
| resources.requests | Scheduling decision |
| resources.limits | Runtime ceiling |
| serviceAccountName | Kubernetes API identity |
| nodeSelector | Eligible nodes |
| volumes and volumeMounts | Files inside a pod |

Changing one field never fixes a problem that belongs to another row. A `Pending` pod is a scheduling or image problem. A pod that ends with exit code 137 is often a limit problem. A node that reports a permission error for task results is an identity problem.

## Common pitfalls

> [!WARNING]
> A request that is too large leaves the pod pending without a workflow error. An emptyDir volume is lost when the pod ends. Do not put secrets in workflow parameters, because the object, the logs and the status expose them.
