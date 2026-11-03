---
draft: true
exam_objectives:
- Understand Argo Workflow Fundamentals
---
# Submitting Workflows And Setting Parameters

A Workflow only runs after someone creates the object. People create it in three ways: with `kubectl`, with the `argo` command-line tool, or through the Argo Server (the web interface and API). Each way ends in the same result: a `Workflow` object in the Kubernetes API. This part shows the differences, because the exam asks which tool fits which task, and because one common `kubectl` mistake fails silently for new learners.

## Submit with kubectl

The Kubernetes tool treats a `Workflow` as any other object. `kubectl create -f file.yaml` creates it and `kubectl get workflows` lists it. The command works for objects that use `metadata.generateName`, where the API server picks a unique name:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: greet-
  namespace: starfleet
spec:
  serviceAccountName: workflow-runner
  entrypoint: greet
  templates:
  - name: greet
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('hello')"]
```

`kubectl apply -f` does not work with `generateName`. Apply needs a fixed name to compare the stored object with the file, so the command fails with an error that says a name is required. Use `kubectl create -f` for generated names. Use `kubectl apply -f` only when the file has `metadata.name`.

## Submit with the argo tool

The `argo` command-line tool adds workflow-specific helpers on top of the same API. These commands are the ones to know:

- `argo submit file.yaml` creates a Workflow from a file.
- `argo submit --from workflowtemplate/<name>` creates a Workflow from a stored `WorkflowTemplate`.
- `argo submit --from cronworkflow/<name>` creates a one-time run from a `CronWorkflow`.
- `argo list` shows the workflows in the current namespace.
- `argo get <name>` prints the tree of nodes with their phases.
- `argo logs <name>` prints the logs of the pods of the run.
- `argo watch <name>` follows the status until the run ends.

The name `@latest` stands for the newest workflow, which saves typing. The tool reads the same kubeconfig as `kubectl`. It talks to the Kubernetes API directly in this setup, so it needs RBAC permission on `workflows`. When the Argo Server is used, the tool sends requests to the server instead, and the server's own authentication mode decides who may do what.

## Submit through the Argo Server

The Argo Server is a Deployment that offers a web interface and an HTTP API for workflows. It is optional. A cluster can run workflows with only the controller. The server is useful when people need a browser view of a workflow, when another system calls an API, or when the workflow archive is used. This course playground keeps the server turned off, because every task uses `kubectl`.

## Parameters and overrides

A workflow can declare default arguments and a user can override them at submission. The defaults live in `spec.arguments.parameters`:

```yaml
spec:
  entrypoint: greet
  arguments:
    parameters:
    - name: message
      value: hello
  templates:
  - name: greet
    inputs:
      parameters:
      - name: message
    container:
      image: docker.io/library/python:3.13-alpine
      command: [python, -c]
      args: ["print('{{inputs.parameters.message}}')"]
```

The workflow-level parameter `message` holds `hello`. The template declares an input with the same name but no value. The entrypoint template gets the workflow arguments as its inputs, because it has no caller. Any other template receives its input from the `arguments` of the step or task that calls it.

`argo submit file.yaml -p message=goodbye` replaces the default for that run only. The stored file is not changed. With `kubectl` there is no such flag, so you edit the file or you write a second file that sets the value.

## Where a parameter value is replaced

The controller replaces `{{...}}` tags when it processes the template, before it creates the pod. The container never sees the braces. This has two effects.

First, a value with quote characters can break the command. The text `print('{{inputs.parameters.message}}')` fails when the value itself contains a single quote, because the replaced text closes the string early. Pass such values as environment variables or as files instead of putting them into a shell or code string.

Second, the replaced value is visible in the pod specification and in the `Workflow` object. Do not pass secrets this way. Mount a Kubernetes Secret as an environment variable or a volume instead.

## Common values you can use

Besides `inputs.parameters`, templates can use a set of global values. The most used are:

- `{{workflow.name}}` is the name of the run.
- `{{workflow.namespace}}` is its namespace.
- `{{workflow.parameters.<name>}}` is a workflow-level parameter.
- `{{workflow.creationTimestamp}}` is the creation time.
- `{{pod.name}}` is the name of the pod of the current node.

The `workflow.name` value is useful for naming output files or labels, because it is unique in the namespace.

## What you now know

You can create a Workflow with `kubectl create`, with `argo submit` or through the Argo Server, and you know that `generateName` needs `create`. You can set default arguments, override them at submission, and you know the controller replaces the tags before the pod exists. The open question is what remains after the run ends and how to read it. The next part covers status, logs and cleanup.

## Common pitfalls

> [!WARNING]
> `kubectl apply` fails on a Workflow that has only `generateName`. A parameter value containing quotes can break an inline command. Do not pass secrets as parameters, because the `Workflow` object shows every value.
