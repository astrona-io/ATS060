---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Lifecycle Controls: Retry, Deadline, Parallelism And Cleanup

A workflow can fail in many ways, and it can also run longer, wider or longer-lived than you want. Four groups of fields bound that behavior. Each acts on a different event, so a field for one problem does not fix another.

## Retry: run a failed node again

`retryStrategy` is set on a template. When a node of that template fails, the controller can create a new pod for it:

```yaml
templates:
- name: fetch
  retryStrategy:
    limit: "3"
    retryPolicy: OnFailure
  container:
    image: docker.io/library/python:3.13-alpine
    command: [python, -c]
    args: ["raise SystemExit(1)"]
```

- `limit` is the maximum number of retries, written as a string. With `limit: "3"`, a node runs at most four times: one first attempt and three retries.
- `retryPolicy` chooses which failures count. `OnFailure` retries when the main container ends with a failed state. `OnError` retries when the controller or an init or wait container reports an error. `Always` retries both. `OnTransientError` retries only errors that the controller treats as transient.
- `expression` is an extra condition evaluated after each attempt. Both the policy and the expression must allow the retry. For example, `asInt(lastRetry.exitCode) > 1` retries only when the last exit code was above one.
- `backoff` sets a delay between attempts, so repeated retries do not hit a failing service at once.

Each attempt is a separate node in the status, and the retry node that groups them has the type `Retry`. The tag `{{retries}}` holds the number of the current attempt, which starts at zero. A template can read it to behave differently on the first attempt.

A retry repeats everything the container does. If the container wrote a row to a database before it failed, the retry writes it again. A retry is safe only for work that can be repeated without changing the outcome.

## Deadline: stop work that runs too long

`activeDeadlineSeconds` sets a time limit in seconds. It can be set on the workflow spec, where it bounds the whole run, or on one template, where it bounds that template's node:

```yaml
spec:
  activeDeadlineSeconds: 600
  templates:
  - name: slow
    activeDeadlineSeconds: 60
```

When the limit passes, the controller stops the work that is still running. The deadline does not undo any effect that already happened outside the cluster, such as a file written to a bucket. A workflow without a deadline can wait forever, for example in a `suspend` step, so a deadline is a safe default for unattended runs.

## Parallelism: limit concurrent pods

`parallelism` limits how many nodes of one workflow run at the same time. It can be set on the workflow spec and on a `steps` or `dag` template. A fan-out of one hundred items with `parallelism: 5` creates pods in batches, so five run at once and the others wait.

```yaml
spec:
  parallelism: 2
```

The limit counts nodes of this workflow only. It does not cap the total pods in the namespace, and it does not replace a Kubernetes quota. The controller also has its own limits, which the cluster administrator sets.

## Cleanup: what stays after the run

A finished workflow and its pods stay in the cluster until something removes them. Two fields control that.

`ttlStrategy` deletes the Workflow object after it ends:

```yaml
spec:
  ttlStrategy:
    secondsAfterCompletion: 3600
    secondsAfterSuccess: 600
    secondsAfterFailure: 86400
```

The three fields count seconds from the end of the run. The first applies to any end state, and the other two apply to only one of them. Deleting the Workflow object also deletes its pods, because the pods are owned by it.

`podGC` deletes pods while the workflow object stays:

```yaml
spec:
  podGC:
    strategy: OnWorkflowSuccess
```

The strategies are `OnPodCompletion`, `OnPodSuccess`, `OnWorkflowCompletion` and `OnWorkflowSuccess`. Pod deletion removes the pod logs from the cluster. If you need the logs later, archive them first, or choose a strategy that keeps failed pods.

## Which control fits which problem

| Problem | Field |
| --- | --- |
| A step fails sometimes and can run again | retryStrategy |
| A step or run hangs | activeDeadlineSeconds |
| Too many pods start at once | parallelism |
| Old workflow objects pile up | ttlStrategy |
| Finished pods pile up | podGC |

## Common pitfalls

> [!WARNING]
> A retry repeats external effects. A deadline does not undo them. A limit written as a number may be rejected where a string is expected, so quote it as the examples do. A ttlStrategy that is too short deletes the evidence you need to debug a failure.
