---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Summary

A parameter is a short string stored in the Workflow object. An artifact is a file or directory stored in an artifact repository, and the Workflow stores only a reference to it. Parameters steer decisions and artifacts move data.

The wait container of a pod uploads declared output files, and the init container of the next pod downloads input files. The from field of an argument connects an output of one step or task to an input of another. By default the executor packs an output into a gzip-compressed tar file, and the archive field can change that.

The default repository is set in the workflow-controller-configmap under the key artifactRepository. One workflow can use another repository through artifactRepositoryRef or an inline s3 block. The credential Secret must exist in the namespace where the pods run. A wrong path, a missing Secret, a missing bucket or a wrong endpoint fails the node even when the container exits successfully. Retention of stored objects belongs to the repository or to artifact garbage collection.

<!-- astrona:playground:destroy -->
