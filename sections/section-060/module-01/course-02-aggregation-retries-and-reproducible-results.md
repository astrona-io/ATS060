---
draft: true
exam_objectives:
- Run Data Processing Jobs with Argo Workflows
---
# Aggregation, Retries And Reproducible Results

After the parts are processed, the pipeline has to join them and must be safe to run again. This part covers the join, the effect of retries and the checks that tell you the result is valid.

## Joining part results

The join task runs after all parts. It needs to know whether every part is required and how to treat a part that failed.

With the default behavior of `steps`, a failed part stops the workflow before the join step starts. With a DAG, a `depends` expression chooses:

```yaml
- name: combine
  template: combine
  depends: "process.Succeeded"
```

The task result `process.AnySucceeded` accepts a partial success, and `process.AllFailed` is true when no part succeeded. Accept a partial result only when the business rule allows it, and record which parts are missing.

The outputs of all iterations of a looped step are available as one JSON array in `{{steps.process.outputs.result}}`, if every iteration printed valid JSON. For file data, each iteration writes an artifact with a key that contains its part name, and the join step reads them by that key.

## What a missing part must not become

If a part has no output, the join should fail or report it. A missing file that silently turns into an empty value hides the loss. Write the join so that it checks the count of inputs against the number of parts it expects.

## Retries repeat effects

A `retryStrategy` on the processing template runs a failed part again. This helps with transient faults such as a network error. It is also a risk:

- A part that wrote a database row before it failed writes it again on the retry.
- A part that appended to a file appends again.
- A part that sent a message sends it again.

Make the work idempotent: running it twice leaves the same result as running it once. Common ways are to write to a key that contains the run and part name, to replace instead of append and to check before writing.

## Staging and publishing

Keep intermediate output apart from final output. Write parts to a staging key. After the join succeeded and the result was checked, publish by writing the final key. A failed run then leaves only staging data, and consumers never read a partial result.

```yaml
s3:
  key: 'staging/{{workflow.name}}/{{inputs.parameters.item}}.txt'
```

A cleanup policy should keep staging data until the join has finished and remove it afterward. Artifact garbage collection and repository lifecycle rules can do that.

## Evidence that the result is valid

A phase of `Succeeded` shows that every container exited with code zero. Other evidence shows that the data is right:

- The count of processed parts equals the count of expected parts.
- The output of each part has the expected size or format.
- The final output carries the identity of the input and of the run.

Record the dataset version, the workflow name and the image tag with the result, so that you can explain it later.

## Observing the pipeline

Task phases, logs and output checks describe different things. A part can finish and produce an empty file, and a write to an external system can fail after the computation is done. Useful measures are the duration of the run, the number of parts processed and the time of the last successful run. Keep confidential data out of logs and parameters.

## A join in steps form

In a steps template, the join is the next outer group. It receives the aggregated output as an argument:

```yaml
- - name: process
    template: produce
    withParam: '{{steps.list.outputs.result}}'
- - name: combine
    template: combine
    arguments:
      parameters:
      - name: parts
        value: '{{steps.process.outputs.result}}'
```

The group of `combine` starts only after every iteration of `process` ended. The tag holds one JSON array with an element for each iteration, so the combine template can parse it and count the elements.

## Running a failed pipeline again

A finished workflow is not rerun from edited fields. To run again, submit a new Workflow object. You have two choices:

- Run the full pipeline under a new name. This is simplest when the stages are idempotent and cheap.
- Run only the failed parts. This needs the part list as a parameter, so you can pass a shorter list, and it needs the join to accept results from an earlier run.

The `argo resubmit` and `argo retry` commands of the Argo command-line tool exist for this. A resubmit creates a new run from the same spec. A retry continues the failed run and reuses finished nodes. Check the behavior of your version before you rely on either in a data pipeline.

## Recording the run identity

A result is easier to explain when it carries its origin. Add labels to the workflow when you submit it, for example the dataset and the version of the pipeline definition. The labels stay on the object while it exists. Copy the same values into the final output so that they remain after cleanup.

```yaml
metadata:
  labels:
    dataset: survey-2026-01
    pipeline: v3
```

## Common pitfalls

> [!WARNING]
> A retry can repeat external writes. A missing part must fail the join or be reported. Publish only after the join and its checks have passed, and never leave final keys writable by failed runs.
