---
draft: true
exam_objectives:
- Understand Argo Workflow Templates
---
# Reusable WorkflowTemplate And ClusterWorkflowTemplate Definitions

Reusable definitions reduce duplication and make workflow behavior easier to review. Argo distinguishes templates embedded in a Workflow from separately managed WorkflowTemplate and ClusterWorkflowTemplate resources. Their purpose is reuse of execution intent, not automatic execution of every definition that exists.

## Inline Templates Belong To A Run Definition

A Workflow can contain several named templates and select one as its entrypoint. Those templates can call other templates within the supported composition model. Their names are local to that definition context and should express the responsibility they perform.

An inline definition is convenient for a self-contained pipeline, but repeated copies can drift. If several pipelines need the same reviewed task, a reusable resource can centralize its contract. Centralization also creates governance responsibility because a change can affect multiple future executions.

## Reusable Resources Have Scope

A WorkflowTemplate is namespaced. A ClusterWorkflowTemplate is cluster-scoped and supports the corresponding reference behavior. Scope affects where a definition can be found and who may manage it under API permissions. It does not automatically determine the task's execution node or grant the task unrestricted API authority.

Shared definitions should have owners and a review process. A tenant permitted to invoke a template should not necessarily be permitted to modify its privileged behavior. Evaluate invocation, editing and execution credentials separately so reuse does not become an unintended escalation path.

## References Express Different Relationships

A templateRef can refer to a template inside a reusable resource under the supported schema. A workflowTemplateRef can select a reusable workflow definition for a run. The exact fields and supported combinations depend on the intended Argo version, so validate the reference contract rather than assume every resource is interchangeable.

Arguments provide the values needed by the referenced definition. Required parameter names, defaults and artifact inputs must match. A reference to the correct resource but the wrong template name can fail before useful work starts. A valid reference with an incompatible input can instead fail during task execution.

## Version Definitions Deliberately

Changing a shared template can alter future runs. A reproducible execution needs a way to identify the definition and inputs that produced its output. Merely using a stable resource name does not prove that its content remained unchanged over time. Release processes can use reviewed versions or other appropriate immutable references according to the system's design.

A copied Workflow object and its resolved template state should be interpreted under the implementation's lifecycle. Do not claim that editing a definition universally updates already running tasks. Existing task execution and future reference resolution are different stages.

## Keep Authority And Data Explicit

A template may specify images, mounts, resource needs or external credentials. Its reusable nature does not make those choices safe. A broadly writable definition consumed by privileged workflows can expose powerful execution authority. Restrict editing and constrain which inputs can influence sensitive operations.

Document outputs and failure behavior as well as inputs. A reusable task should explain whether retries are safe, which artifacts it produces and which credentials it needs. Consumers then rely on a clear execution contract rather than a name whose implementation and permissions are unknown.

## Common pitfalls

> [!WARNING]
> Reusable scope does not grant execution permissions. Definition editing, invocation and task identity are separate authorities, and a stable resource name alone does not ensure reproducible content.
