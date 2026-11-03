# Run A Locked Partition-Process-Join Pipeline

Build a pipeline that lists parts at run time, processes them in parallel under a mutex and joins the results.

UNTESTED: this lab was built without booting a cluster. Run `testing/smoke.sh` with its private kubeconfig to verify that the starting state is rejected and the reference solution passes. Static validation is not live evidence.
