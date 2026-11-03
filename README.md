# Argo Workflows (ATS060)

Certified Argo Project Associate (CAPA): Argo Workflows, worth 36% of the official curriculum. This course belongs to ATP012.

Each of the six sections has two modules, a section capstone lab and a section quiz, and the course ends with a final domain quiz. Every module has a landing page, developed parts, guided practice, a summary, a private playground and a graded lab. Technical content remains draft. Labs and playgrounds are untested.

## Course Outline

| Section / module | Module |
| --- | --- |
| 010 / 01 | Workflow Resources, Templates And Execution Ownership |
| 010 / 02 | Running And Inspecting Workflows |
| 020 / 01 | Generating, Storing And Consuming Workflow Artifacts |
| 020 / 02 | Artifact Sources, Archive Options And Cleanup |
| 030 / 01 | Reusable WorkflowTemplate And ClusterWorkflowTemplate Definitions |
| 030 / 02 | Template Types And Composition |
| 040 / 01 | Reading The Workflow Spec |
| 040 / 02 | Resources, Identity, Placement And Status |
| 050 / 01 | DAG Tasks, Dependencies And Data Flow |
| 050 / 02 | Conditional Tasks And Fan-Out |
| 060 / 01 | Data Processing Pipelines |
| 060 / 02 | Scheduled And Controlled Pipeline Runs |

## Author Review

See [curriculum coverage](CURRICULUM.md), [primary sources](SOURCES.md), [question-bank documentation](ASSESSMENTS.md) and [contribution instructions](CONTRIBUTING.md). No runtime execution is claimed.

## Hands-On Coverage

This course has 12 ungraded playgrounds (one per module) and 19 independent draft labs: 13 module labs and 6 section capstones. Tasks, launch entries and solutions follow their teaching reading. Guided practice precedes the summary. Static checks (`astrona validate`, `bash -n`, YAML parsing) are done. Live execution is pending, so every lab and playground is untested.

| Section / module | Lab | Difficulty |
| --- | --- | --- |
| 010/01 | Run A Workflow Through The Executor | intermediate |
| 010/02 | Report An Overridden Argument With Cleanup | intermediate |
| 010/capstone | Build A Two-Step Report With Retention | advanced |
| 020/01 | Produce Store And Consume An Artifact | intermediate |
| 020/02 | Stage A Raw Input Without Packing | intermediate |
| 020/capstone | Build A Three-Step Artifact Pipeline With Cleanup Policy | advanced |
| 030/01 | Instantiate A Reusable WorkflowTemplate | intermediate |
| 030/01 | Instantiate A Cluster Scoped Template | intermediate |
| 030/02 | Pass A Script Result Between Steps | intermediate |
| 030/capstone | Compose A Workflow From A Reusable Template Library | advanced |
| 040/01 | Recover A Workflow Step With A Bounded Retry | intermediate |
| 040/02 | Run A Workflow With Resources And A Pod Volume | intermediate |
| 040/capstone | Bound A Survey Run With Argument, Retry, Deadline And Cleanup | advanced |
| 050/01 | Execute A DAG Dependency | intermediate |
| 050/02 | Choose A DAG Branch With A When Condition | intermediate |
| 050/capstone | Build A Branching DAG With A Fan-Out And A Join | advanced |
| 060/01 | Fan Out A Bounded Processing Job | intermediate |
| 060/02 | Schedule A Nightly Scan Without Overlap | intermediate |
| 060/capstone | Run A Locked Partition-Process-Join Pipeline | advanced |
