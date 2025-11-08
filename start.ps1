#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

# -----------------------
# 1) Set environment variables
# -----------------------
$env:OPENAI_API_KEY="" # This is a placeholder "F4zslf8MlYcfCbwGXINHf4IS9AQQv0Zc77i0l8DkOsbTUUXWgH6nJQQJ99BJACHYHv6XJ3w3AAAAACOGcBEW"
$env:AZURE_OPENAI_API_ENDPOINT="" # This is a placeholder "https://thien-mgl8on6m-eastus2.cognitiveservices.azure.com/openai/v1/"

# -----------------------
# 2) Apply Namespace
# -----------------------
kubectl apply -f k8s/namespace.yaml

# -----------------------
# 3) Apply ConfigMap
# -----------------------
kubectl apply -f k8s/configmap.yaml

# -----------------------
# 4) Apply Secrets dynamically
# -----------------------
(Get-Content k8s/secret.yaml) -replace '\$\{OPENAI_API_KEY\}', $env:OPENAI_API_KEY `
                                       -replace '\$\{AZURE_OPENAI_API_ENDPOINT\}', $env:AZURE_OPENAI_API_ENDPOINT |
kubectl apply -f -

# Check with Git Bash
# kubectl get secret smart-recycle-secrets -n smart-recycle-dev -o jsonpath="{.data.OPENAI_API_KEY}" | base64 --decode

# -----------------------
# 5) Deploy Qdrant
# -----------------------
kubectl apply -f k8s/deployment-qdrant.yaml
# kubectl get pods -n smart-recycle-dev --show-labels
kubectl apply -f k8s/service-qdrant.yaml  
# kubectl describe svc service-qdrant -n smart-recycle-dev

# -----------------------
# 7) Run Qdrant-init Job
# -----------------------
docker build -t qdrant-init-image:latest ./qdrant
kubectl apply -f k8s/job-qdrant-init.yaml 
#kubectl get jobs -n smart-recycle-dev

Write-Host "Waiting for Qdrant-init job to complete..." -ForegroundColor Cyan
$maxRetries = 3
$retry = 0
do {
    $jobStatus = kubectl get job job-qdrant-init -n smart-recycle-dev -o jsonpath="{.status.succeeded}" 2>$null
    if ($jobStatus -eq "1") {
        Write-Host "Qdrant-init job completed successfully." -ForegroundColor Green
        break
    }
    Start-Sleep -Seconds 120
    $retry++
    Write-Host "Waiting for Qdrant-init job... ($retry/$maxRetries)"
} while ($retry -lt $maxRetries)

if ($retry -ge $maxRetries) {
    Write-Host "Qdrant-init job did not complete in time." -ForegroundColor Red
    exit 1
}

# -----------------------
# 8) Deploy Backend
# -----------------------
docker build -t backend-image:latest ./backend 
kubectl apply -f k8s/deployment-backend.yaml

Write-Host "Waiting for Backend pods to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod -l app=backend-pod -n smart-recycle-dev --timeout=120s

kubectl apply -f k8s/service-backend.yaml

# -----------------------
# 9) Deploy Frontend
# -----------------------
docker build -t frontend-image:latest ./frontend 
kubectl apply -f k8s/deployment-frontend.yaml

Write-Host "Waiting for Frontend pods to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod -l app=frontend-pod -n smart-recycle-dev --timeout=120s

kubectl apply -f k8s/service-frontend.yaml