import pickle
import os
from sklearn import svm
from bottle import Bottle, run, request, response

app = Bottle()

# API route to get the service status
@app.route('/status', method='GET')
def status():
    response.content_type = 'application/json'
    return "ok" # svm.get_status()

# API route to process data (POST request)
@app.route('/process', method='POST')
def process():
    input_data = request.json.get("data", [])  # Get data from JSON request
    if not input_data:
        response.status = 400
        return {"error": "No data provided"}

    result = str(clf.predict(input_data))

    response.content_type = 'application/json'

    return result


# Run the Bottle server
if __name__ == '__main__':
    version = os.environ['MODEL_VERSION']
    with open(f"/mnt/models/models/{version}/model", "rb") as f:
        clf: svm.SVC = pickle.load(f)
    run(app, host='0.0.0.0', port=8080)
