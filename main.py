import os
import argparse
import pickle
import pandas as pd
from sklearn import svm
from bottle import Bottle, run, request, response

app = Bottle()
clf = None  # Global model variable for serving

# API routes for serving mode
@app.route('/', method='GET')
def status():
    response.content_type = 'application/json'
    model_version = os.environ.get("MODEL_VERSION")
    return {"version": model_version}

@app.route('/status', method='GET')
def status():
    response.content_type = 'application/json'
    return {"status": "ok"}

@app.route('/process', method='POST')
def process():
    input_data = request.json.get("data", [])
    if not input_data:
        response.status = 400
        return {"error": "No data provided"}
    result = clf.predict(input_data).tolist()
    response.content_type = 'application/json'
    return {"result": result}

def get_data_filenames(directory, prefix="train"):
    X_file = os.path.join(directory, f"x_{prefix}.csv")
    y_file = os.path.join(directory, f"y_{prefix}.csv")
    return X_file, y_file

def train_model(data_path, model_path, data_hash_file):
    metadata_path = f"{data_path}/current_hash"
    with open(metadata_path, "r") as f:
        data_hash = f.read().strip()

    full_data_path = f"{data_path}/{data_hash}/"
    X_train_file, y_train_file = get_data_filenames(full_data_path, "train")
    X_train = pd.read_csv(X_train_file)
    y_train = pd.read_csv(y_train_file)

    clf = svm.SVC()
    clf.fit(X_train, y_train.values.ravel())

    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)

    with open(data_hash_file, 'w') as f:
        f.write(data_hash)

    print(f"Model trained and saved to: {model_path}")
    print(f"Data hash written to: {data_hash_file}")

def validate_model(data_path, model_path, result_path):
    with open(model_path, "rb") as f:
        clf: svm.SVC = pickle.load(f)

    metadata_path = f"{data_path}/current_hash"
    with open(metadata_path, "r") as f:
        data_hash = f.read().strip()

    full_data_path = f"{data_path}/{data_hash}/"
    X_test_file, y_test_file = get_data_filenames(full_data_path, "test")
    X_test = pd.read_csv(X_test_file)
    y_test = pd.read_csv(y_test_file)

    accuracy = clf.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy}")

    with open(result_path, 'w') as f:
        f.write(str(accuracy))

def serve_model(model_version):
    global clf
    with open(f"/mnt/models/models/{model_version}/model", "rb") as f:
        clf = pickle.load(f)
    run(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Model operations: serve, train, validate")
    parser.add_argument("mode", choices=["serve", "train", "validate"], help="Operation mode")
    parser.add_argument("--model_version", type=str, help="Model version to load (for serve)")
    parser.add_argument("--data_path", type=str, help="Path to data directory")
    parser.add_argument("--model_path", type=str, help="Path to save/load the model")
    parser.add_argument("--data_hash", type=str, help="Path to save data hash")
    parser.add_argument("--result", type=str, help="Path to save validation results")

    args = parser.parse_args()

    if args.mode == "serve":
        model_version = os.environ.get("MODEL_VERSION")
        if not model_version:
            raise EnvironmentError("Environment variable MODEL_VERSION not set for serve mode.")
        serve_model(model_version)

    elif args.mode == "train":
        if not all([args.data_path, args.model_path, args.data_hash]):
            raise ValueError("Missing required arguments for training.")
        train_model(args.data_path, args.model_path, args.data_hash)

    elif args.mode == "validate":
        if not all([args.data_path, args.model_path, args.result]):
            raise ValueError("Missing required arguments for validation.")
        validate_model(args.data_path, args.model_path, args.result)
