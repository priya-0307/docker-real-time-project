# app.py
from flask import Flask, jsonify, request
import os
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"message": "Hello from Dockerized ToDo app!"})

# optional simple health endpoint
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
