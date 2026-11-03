---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Reading Status And Failure Evidence

The spec says what you asked for. The status says what the controller observed. This part shows where to look when a run does not end as planned and how to tell the causes apart.

## The status structure

A Workflow has a `status` field written by the controller. These parts matter most:

- `phase` is the state of the whole workflow: `Pending`, `Running`, `Succeeded`, `Failed` or `Error`.
- `message` gives a short reason when the workflow did not succeed.
- `startedAt` and `finishedAt` are timestamps.
- `nodes` is a map with one entry for each step, task, group or retry attempt. Each node has `displayName`, `type`, `phase`, `message` and, when present, `outputs`.
- `progress` counts finished nodes against all nodes.

The difference between `Failed` and `Error` matters. `Failed` means a node ran and ended unsuccessfully, for example with a non-zero exit code. `Error` means the controller or the executor could not do its own work, for example a missing ServiceAccount permission or an invalid template.

## Node phases and what they point to

| Node phase | Typical meaning |
| --- | --- |
| Pending | The pod exists and has not started. Check events for scheduling or image pull problems. |
| Running | The main container is running. |
| Succeeded | The container exited with code zero and results were recorded. |
| Failed | The container exited with a non-zero code, or a deadline ended it. |
| Error | The controller could not complete its work for the node. |
| Omitted | A condition skipped the node. |

A node of type `Pod` has a pod behind it. Nodes of type `Steps`, `StepGroup`, `DAG` and `Retry` are structure only and have no pod.

## Find the first failing node

When a large workflow fails, the last failed node is usually a consequence. Follow this order:

1. Read `.status.phase` and `.status.message`.
2. List all nodes with their type, phase and message.
3. Find the earliest node of type `Pod` that is not `Succeeded`.
4. Read the pod events for that node with `kubectl describe pod`.
5. Read the logs of the `main` container. The `init` and `wait` containers are only needed when the node phase is `Error`.

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.type}{" "}{.phase}{" "}{.message}{"\n"}{end}'
```

## Spec, status and outside evidence

A workflow can reach `Succeeded` and still be wrong. Success means each container exited with code zero and the outputs were recorded. It does not mean the data is correct. For a run that changes outside systems, check those systems as well: the artifact in the bucket, the row in the database, the object in the cluster.

The status of a deleted pod is kept in the workflow object, so the node list stays readable after pod cleanup. The pod logs do not, unless logs were archived. This is why a `podGC` strategy that deletes every pod needs an archive policy for logs.

## A short decision guide

- Pod pending: read events, then check requests, node selectors, taints and image names.
- Pod failed with an application error: read the main container logs.
- Pod failed after exactly the deadline: the deadline fired. Read the node message.
- Node in `Error`: read the `wait` container logs and the permissions of the ServiceAccount.
- Workflow `Succeeded` with wrong data: check the content of outputs, not the phase.

## Outputs in the status

A node that declared outputs carries them in `outputs`. Parameters appear in `outputs.parameters` as a name and a value. A script template also has `outputs.result`, which holds its standard output. Artifacts appear in `outputs.artifacts` with the repository key that was used.

```sh
kubectl -n starfleet get workflow mission -o jsonpath='{range .status.nodes.*}{.displayName}{" "}{.outputs.parameters}{"\n"}{end}'
```

A missing output on a node that succeeded usually means that the declared path was not written. The controller then marks the node as failed or in error, because the output declaration is part of the contract of the template.

## Exit codes as evidence

The exit code of the main container points to a cause when you read it with the node message:

- Code 0 means the process ended normally.
- Code 1 and other small values are set by the program. Read its logs.
- Code 137 means the process received a kill signal. A memory limit, a deadline or a node shutdown can cause it.
- Code 143 means the process received a termination request and stopped.

The workflow status does not translate every code for you. Use the code together with the pod events and the logs.

## Reproducing a failure safely

To test a fix, change one field and submit a new workflow object with a new name. Do not edit the failed object, because the controller does not rerun a finished workflow from edited fields. A resubmission of the same spec is a new run with its own nodes, so the evidence of the first run stays available for comparison until cleanup removes it.

## Common pitfalls

> [!WARNING]
> Do not change workflow-wide settings in response to one node's error. The last failed node is often only a result of an earlier one. A phase of Succeeded proves that the exit code was zero, not that the result is correct.
