#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-060-capstone-030-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"

kubectl apply -f "$solution_directory/workflowtemplate-crew-library.yaml"
kubectl apply -f "$solution_directory/workflow-launch-crew.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/launch-crew --timeout=240s
