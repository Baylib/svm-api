# svm api

[https://pythonprogramming.net/predictions-svm-machine-learning-tutorial/?completed=/svm-optimization-python-2-machine-learning-tutorial/]

## run

```bash
source ./venv/bin/activate
python3 main.py
pip freeze requirements.txt

```

## call

```bash
curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d '{"data": [6,-5]}'
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
