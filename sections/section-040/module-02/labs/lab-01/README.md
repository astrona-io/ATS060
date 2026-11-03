# Run A Workflow With Resources And A Pod Volume

Set resource requests and limits, mount an emptyDir volume and expose a value read from it.

UNTESTED: this lab was built without booting a cluster. Run `testing/smoke.sh` with its private kubeconfig to verify that the starting state is rejected and the reference solution passes. Static validation is not live evidence.
