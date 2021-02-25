import flask
import hashlib
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"
