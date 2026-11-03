---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Scheduled Runs With CronWorkflow

A data pipeline often runs on a timetable, for example every night. The `CronWorkflow` custom resource creates Workflow objects on a cron schedule. A cron schedule is a text expression with five fields: minute, hour, day of month, month and day of week.

## The object

```yaml
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  name: nightly-scan
  namespace: starfleet
spec:
  schedules:
  - "0 3 * * *"
  timezone: UTC
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 120
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  workflowSpec:
    serviceAccountName: workflow-runner
    entrypoint: main
    templates:
    - name: main
      container:
        image: docker.io/library/python:3.13-alpine
        command: [python, -c]
        args: ["print('scan')"]
```

The expression `0 3 * * *` means minute 0 of hour 3 on every day. The `workflowSpec` field has the same shape as the spec of a Workflow. The controller creates a new Workflow from it each time the schedule fires.

The field is named `schedules` and holds a list. In the versions of Argo Workflows that this course uses, a non-empty list is required. Older versions used a single `schedule` string, so check the version of your cluster before you copy examples from other sources.

## Fields that shape the behavior

- `timezone` is an IANA time zone name. Without it the schedule uses the time zone of the controller.
- `suspend` set to `true` stops new runs. Existing runs continue.
- `concurrencyPolicy` decides what happens when the schedule fires while the previous run is still active. `Allow` starts another run. `Forbid` skips the new run. `Replace` stops the old run and starts a new one.
- `startingDeadlineSeconds` is how long after the scheduled time a missed run can still start. The controller could be down or busy at the scheduled time. After this many seconds the run is dropped.
- `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` set how many finished Workflows from this schedule are kept. The controller deletes the older ones.
- `workflowMetadata` adds labels and annotations to every generated Workflow.
- `when` holds an expression that is evaluated on each schedule hit. The run starts only if it is true.
- `stopStrategy` stops the schedule when an expression about past results becomes true.

## Choosing the concurrency policy

A pipeline that writes to one place should not overlap with itself. Use `Forbid` for that, and give the schedule enough room that a normal run finishes before the next time. Use `Replace` when a newer run makes the older one useless. Use `Allow` only when runs are independent.

A skipped run does not create an object, so there is no failed run to read. Look at the controller logs or at the lack of a new Workflow to find it.

## Generated Workflows

Each run is an ordinary Workflow. Its name starts with the CronWorkflow name followed by a time-based suffix, and it carries a label that points back to the CronWorkflow. You can list the runs by that label.

The commands in this part run against the module playground, with the kubeconfig of that playground selected.

<!-- astrona:playground:renew -->

```sh
kubectl -n starfleet get workflow -l workflows.argoproj.io/cron-workflow=nightly-scan
```

Because the generated object is a normal Workflow, the controls of the earlier modules apply to it: deadline, retries, cleanup. The history limits clean the objects of this schedule, and `ttlStrategy` inside `workflowSpec` also applies.

## What the CronWorkflow status shows

The status of the CronWorkflow records the last scheduled time and the list of active Workflows. Use it to see whether the schedule has fired and whether a run is active.

```sh
kubectl -n starfleet get cronworkflow nightly-scan -o jsonpath='{.status.lastScheduledTime}{"\n"}'
```

## Reading a cron expression

The five fields are minute, hour, day of month, month and day of week. A star means every value. A comma separates several values, a dash gives a range and a slash gives a step:

- `*/15 * * * *` fires every fifteen minutes.
- `30 2 * * 1-5` fires at 02:30 on Monday to Friday.
- `0 0 1 * *` fires at midnight on the first day of each month.

The `schedules` field holds a list, so one CronWorkflow can fire at several times. Each entry is its own expression.

## Pausing and resuming

To stop new runs without deleting the object, set `suspend` to `true`. To resume, set it to `false`. With `kubectl` this is a patch of one field:

```sh
kubectl -n starfleet patch cronworkflow nightly-scan --type merge -p '{"spec":{"suspend":true}}'
```

A suspended CronWorkflow keeps its history. Missed times during the suspension are not run later, because the starting deadline is counted from the scheduled time.

## Common pitfalls

> [!WARNING]
> A cron schedule without a time zone uses the controller's. A policy of Allow can run two copies of a pipeline at the same time. Setting suspend to true does not stop a run that already started. Use the plural schedules field for the version used in this course.
