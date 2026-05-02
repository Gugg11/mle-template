import os
import pickle
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = os.path.join("experiments", "log_reg.sav")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ML model API is running"
    })


@app.route("/model", methods=["GET"])
def model_info():
    return jsonify({
        "model": "LOG_REG",
        "dataset": "Seeds",
        "model_path": MODEL_PATH,
        "status": "ready"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    X = pd.DataFrame(data["X"])

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    prediction = model.predict(X)

    return jsonify({
        "prediction": prediction.tolist()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)