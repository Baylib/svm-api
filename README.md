# svm api
This repository is a demo SVM use as a demo model in our MLOps GitOps workflow.
It follows the contribution guidelines in our GitOps master-thesis-nlops project.

## run the image locally

```bash
source ./venv/bin/activate
python3 main.py
pip freeze requirements.txt

```

## call the api

```bash
curl -X POST http://localhost:8080/process \
     -H "Content-Type: application/json" \
     -d '{"data": [6,-5]}'
```

## Docker buid and run

```bash
podman build -t svm-api .
podman run --rm -p 8080:8080 svm-api
```

## Push to docker hub

```bash
podman login -u mthmlops
podman tag svm-api docker.io/mthmlops/svm-api:0.0.1
podman push docker.io/mthmlops/svm-api:0.0.1
```

## install helm chart locally

```bash
# helm install svm-api-helm ./svm-api-helm # first time only
helm upgrade svm-api-helm ./svm-api-helm 
export POD_NAME=$(
  kubectl get pods --namespace default \
    -l "app.kubernetes.io/name=svm-api-helm,app.kubernetes.io/instance=svm-api-local" \
    -o jsonpath="{.items[0].metadata.name}"
)
export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
kubectl logs $POD_NAME
```
