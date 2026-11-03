---
draft: true
exam_objectives:
- Generating and Consuming Artifacts
---
# Summary

An input artifact can come from an earlier step with from, from the manifest with raw, from an HTTP address, from a Git repository or from a bucket. The init container downloads it before the main container starts. A Git branch or URL can change between runs, so a reproducible run pins a commit or a version.

An output can change packing with archive, set its object key with s3.key, and tolerate a missing file with optional. By default the executor stores a gzip-compressed tar file. With archive none a single file is stored as it is, which matters when another program reads the repository directly.

Artifact garbage collection deletes repository objects on workflow completion or deletion, with per-artifact overrides. A garbage collection pod does the work, the Workflow carries a finalizer until it finishes, and the pod needs permission on workflowartifactgctasks. The archiveLogs setting saves container logs as artifacts so they survive pod deletion. A full retention policy combines podGC, archiveLogs, ttlStrategy and artifactGC.

<!-- astrona:playground:destroy -->
