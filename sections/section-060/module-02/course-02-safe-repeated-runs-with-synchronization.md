---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Safe Repeated Runs With Synchronization

A pipeline that runs often will sometimes overlap with itself or with other pipelines that share a resource. This part covers the tools that Argo Workflows offers to limit that overlap, and the habits that make repeated runs safe.

## The problem

Two runs of the same pipeline can write the same output key, update the same table or compete for a limited service. A `parallelism` field does not help, because it counts only the nodes of one workflow. You need a control that works across workflows.

## Mutex

A mutex is a lock with a name. Only one holder can have it. Set it on the workflow spec to serialize whole runs:

```yaml
spec:
  synchronization:
    mutexes:
    - name: pipeline-lock
```

A workflow that finds the lock taken waits in a queue and starts when it reaches the front. Higher `priority` values go first, and older workflows go before newer ones. The state of the lock is in `.status.synchronization` of each workflow.

The same block can be placed on a single template, so only that stage is serialized and the rest of the workflow runs freely:

```yaml
templates:
- name: publish
  synchronization:
    mutexes:
    - name: publish-lock
```

## Semaphore

A semaphore is a counted lock. It allows a fixed number of holders. The limit is stored in a ConfigMap key:

```yaml
spec:
  synchronization:
    semaphores:
    - configMapKeyRef:
        name: pipeline-limits
        key: scan
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pipeline-limits
  namespace: starfleet
data:
  scan: "2"
```

With the value `"2"`, two workflows or templates can hold the semaphore. A third one waits. Change the value in the ConfigMap to change the limit without editing the workflows.

## Which tool for which limit

| Need | Tool |
| --- | --- |
| Concurrent nodes inside one workflow | parallelism |
| One run at a time for a schedule | concurrencyPolicy: Forbid |
| One run at a time across any workflows | mutex |
| N runs at a time across workflows | semaphore |

## Idempotent runs

A lock keeps runs from overlapping. It does not make one run safe to repeat. For that, the work needs these properties:

- Output keys contain the run or the input version, so a rerun writes a new key or the same key with the same content.
- Writes replace content instead of appending.
- A step checks for existing results before it does expensive work.

A run that is repeated after a failure then leaves the system in the same state as a run that worked the first time.

## Observing waiting runs

A workflow that waits for a lock stays in the phase `Pending` and has no pods. Its status holds a message about the lock it waits for. If many workflows wait, look at the holder: it might be stuck without a deadline. A deadline on the holder releases the lock when it fires.

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.phase}{"\n"}{end}'
```

## Reusing the pipeline definition

A pipeline that runs on a schedule and on demand should have one definition. Store it in a WorkflowTemplate and let the CronWorkflow refer to it with `workflowSpec.workflowTemplateRef`. A manual submission then uses the same definition, so both paths behave the same way.

## Common pitfalls

> [!WARNING]
> A mutex held by a run without a deadline blocks everything behind it. A lock limits overlap and does not undo a partial write. A semaphore limit lives in a ConfigMap, so the ConfigMap must exist in the namespace of the workflow.
