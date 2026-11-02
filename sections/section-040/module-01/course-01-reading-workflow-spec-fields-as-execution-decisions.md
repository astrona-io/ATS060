---
draft: true
exam_objectives:
- Understand the Argo Workflow Spec
---
# Reading Workflow Spec Fields As Execution Decisions

A Workflow spec is an execution contract composed of related fields. It identifies the starting template, task definitions and arguments, and can supply operational controls for resource use and lifecycle. Reading it as a set of decisions is more reliable than memorizing isolated field names without understanding the transitions they govern.

## Establish The Definition Graph

The entrypoint selects the initial template. The templates collection or supported references provide the definitions used by that entrypoint and its descendants. Arguments supply values at the workflow boundary, while task-level inputs and references connect values inside the graph.

A definition can describe a container, script, DAG, steps or another supported template type. Each has its own field contract. A field meaningful for a container task should not be assumed to have the same effect in every composition template. Validate the intended resource version and structure.

## Match Tasks To Their Environment

Task images and commands describe the work, but the cluster must obtain the image and prepare its runtime. Resource requests affect placement, while limits and other runtime boundaries affect execution. A task requesting unavailable capacity can remain pending even when its workflow graph is valid.

ServiceAccount selection establishes task-related Kubernetes identity under the supported execution model. External storage or database credentials have separate authority. Placement constraints, volumes and runtime prerequisites also influence whether a task can start. API acceptance establishes declaration validity within its contract rather than all those dependencies.

## Inputs And Outputs Must Be Compatible

A parameter value should match the consumer's expected meaning. An artifact input needs a valid source and supported transfer or mount path. Output declarations must identify data actually produced by the task. An incorrect reference can break a pipeline without any defect in the individual container image.

Sensitive values should not be placed casually in visible parameters or arguments. Resource access, logs and process diagnostics can expose them. Use the supported credential-delivery model and narrow task permissions to the work being performed.

## Lifecycle Controls Solve Different Problems

Retry strategy determines whether eligible failed work is attempted again. Timeouts or deadlines bound time under their respective scope. Parallelism controls the amount of concurrent work, while cleanup or TTL settings govern retained execution resources. None of these automatically makes external side effects idempotent.

A task that writes a database row and then fails can repeat the write on retry. The application needs deduplication or a safe operation contract. A timeout can stop waiting or terminate supported work without undoing an already completed external effect. Cleanup can reclaim Pods while artifacts remain elsewhere.

## Read Status As Observed Evidence

Status records the controller's view of progress and task outcomes. Pending preparation, running computation and failed execution have different causes. Inspect the responsible task and transition rather than change every workflow-level setting in response to one error.

A successful task process establishes its stated success criterion, not every possible business validation. Review output content, downstream persistence and side effects where required. The spec, status and external evidence together explain the execution, while each retains a distinct role. This reading course describes those contracts without introducing a live execution environment.

## Common pitfalls

> [!WARNING]
> Accepted spec is not execution readiness. Retry, timeout, parallelism and cleanup govern different transitions and do not automatically reverse or safely repeat external effects.
