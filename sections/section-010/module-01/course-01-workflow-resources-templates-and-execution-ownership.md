---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Workflow Resources, Templates And Execution Ownership

Argo Workflows orchestrates tasks on Kubernetes through a declarative execution model. A Workflow resource describes a run, including its templates, inputs and entrypoint, and later carries status about its execution. It is suited to jobs and pipelines whose task relationships need coordination rather than ordinary long-running application reconciliation alone.

## Definition And Execution Are Different

A template describes a supported unit or composition of work. It can define a container task, a sequence, a DAG or another supported execution pattern. A Workflow refers to those definitions and supplies the arguments needed for a particular run. The entrypoint identifies where execution begins.

A reusable WorkflowTemplate provides a separately managed definition that can be referenced for runs. Changing a reusable definition and observing one completed run are different lifecycle operations. Preserve the version and inputs used by a run so its result can be interpreted later rather than assume every historical execution used today's definition.

## The Controller Coordinates Tasks

The workflow controller watches Workflow resources and reconciles their declared execution into supported Kubernetes work. It tracks task or node status and advances dependent work according to the definition. The application task normally runs in its assigned Pod rather than inside the controller process.

Executors participate in task lifecycle and supported output handling according to the deployment. Image access, scheduling, runtime preparation and task credentials are separate dependencies. A Workflow can exist while a task cannot start because the image is unavailable or placement is infeasible.

## Inputs And Outputs Form A Contract

Parameters carry values used by templates, while artifacts represent data transferred through a configured storage and execution arrangement. The type of input should match the task's requirement. A small scalar identifier differs from a large dataset, and embedding confidential data in visible parameters can expose it through resource or diagnostic access.

Each task should have an explicit output and success definition. A process exit code can indicate task success under its contract, but it does not automatically prove that an external database contains correct business results. Validate outputs where the pipeline's correctness requires more than process completion.

## Status Describes Progress And Failure

Workflow status can identify pending, running, completed or failed execution under the supported phase model, with task-level context. A blocked dependency differs from a task that ran and failed. Infrastructure errors, application failures and deliberate conditions should be distinguished before choosing retries or corrections.

Retries can repeat side effects. A task writing an external record needs an idempotency or deduplication strategy if it can run again. A controller's ability to reschedule work does not make every business operation safe to repeat automatically.

## Authority And Retention Remain Explicit

The ServiceAccount used by workflow execution needs only the required API authority, while task credentials for external systems have their own scopes. Controller authority and task authority should not be conflated. A task that only transforms a file does not inherently need cluster administration.

Cleanup policies, task logs and artifact retention determine what remains after completion. Removing execution Pods can reclaim capacity while outputs or archived metadata have separate lifetimes. Define ownership of those retained resources and recovery evidence. A useful workflow design connects definition, execution, identity and output lifecycle without claiming that one green phase proves every downstream effect.

## Common pitfalls

> [!WARNING]
> A Workflow run is not the same as a reusable template. Controller coordination does not grant safe retries, narrow credentials or correct external side effects automatically.
