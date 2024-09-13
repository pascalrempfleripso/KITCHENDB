from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"CHOOO CHOO": "KITCHEN DB"})
