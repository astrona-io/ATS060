# Build A Branching DAG With A Fan-Out And A Join

Combine a when branch, a withItems fan-out, a depends join and a parallelism limit in one DAG.

UNTESTED: this lab was built without booting a cluster. Run `testing/smoke.sh` with its private kubeconfig to verify that the starting state is rejected and the reference solution passes. Static validation is not live evidence.
