# Reusable Question Banks

`assessments/index.yaml` lists banks in teaching order. Each bank uses schema
version 1 and the contract in `schemas/question-bank.schema.json`. This is an
authoring format for future application integration, not an existing Astrona
quiz API. No YAML question file is registered as a Markdown reading.

Banks follow their declared module summaries. Larger domains use an intermediate
checkpoint after the third section and a final domain review; smaller domains
use a final domain review. The index records covered sections and teaching order. Banks contain 5–15 original single-choice
questions, scoped to concepts taught in the course. They remain draft for review.

## Fields And Rendering

- `id`: stable bank or question identity; preserve it when editing wording.
- `scope`: section or domain checkpoint.
- `placement`: relative reading path after which the checkpoint belongs.
- `learning_objective`: the measurable outcome checked by the question.
- `source_readings`: author traceability to the teaching; not learner navigation.
- `prompt`: learner-visible question text.
- `options`: stable option IDs, answer text and per-option feedback.
- `correct_option`: the ID of the single correct option.
- `explanation`: feedback reinforcing the supported answer.

The application should send only the question ID, prompt and option IDs/text to
the learner before submission. Keep `correct_option`, `explanation` and option
explanations on the server until feedback is permitted. Match answers by option
ID, not display position, so a later renderer can shuffle choices safely.

The banks contain answer keys and are public learning material, so this is not
a secure examination bank. Do not treat scores as an official CAPA result.

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
