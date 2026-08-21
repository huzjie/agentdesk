#!/usr/bin/env bash
set -euo pipefail

echo "Building agentdesk image..."
docker build -t agentdesk:1.0.0 .

echo "Deploying to Kubernetes..."
kubectl apply -f k8s/

echo "Done."
