---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Summary

A CronWorkflow creates a Workflow from its workflowSpec each time a schedule fires. The schedules field is a list of cron expressions. The concurrencyPolicy field chooses between Allow, Forbid and Replace when a previous run is still active. The startingDeadlineSeconds value bounds how late a missed run can start, and the history limits decide how many finished Workflows stay. Setting suspend to true stops new runs and leaves running ones.

A mutex allows one holder at a time and a semaphore allows a counted number of holders from a ConfigMap value. Both work across workflows, unlike parallelism. A workflow that waits for a lock has the phase Pending and no pods, and its status names the lock. A lock limits overlap and does not make a run safe to repeat, so the work itself must be idempotent.

<!-- astrona:playground:destroy -->
