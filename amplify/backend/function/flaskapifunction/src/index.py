from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import awsgi
import boto3
import os
from uuid import uuid4

app = Flask(__name__)#, static_folder='../build', static_url_path='/')
CORS(app)
BASE_ROUTE = "/items"

def handler(event, context):
    return awsgi.response(app, event, context)

# @app.route(BASE_ROUTE,methods=['GET'])
# def list_items():
#     return jsonify(message='hello world')
 
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# members api route
@app.route(BASE_ROUTE,methods=['GET'])
@cross_origin()
def members():
    return {"members": ["Member1","Member2","Member3"]}

# @app.route('/')
# @cross_origin()
# def serve():
#     return send_from_directory(app.static_folder,'index.html')


if __name__ == "__main__":
    app.run()