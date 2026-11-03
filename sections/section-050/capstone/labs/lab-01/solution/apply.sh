#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != "kind-astro-ats-060-capstone-050-01" ]]; then
  printf 'Refusing to operate on another Kubernetes context\n' >&2
  exit 1
fi
lab_directory="$(cd "$(dirname "$0")/.." && pwd)"
solution_directory="$lab_directory/solution"

kubectl apply -f "$solution_directory/workflow-route-plan.yaml"
kubectl -n starfleet wait --for=jsonpath='{.status.phase}'=Succeeded workflow/route-plan --timeout=300s
