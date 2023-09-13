from flask import Flask
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# members api route
@app.route("/members")
@cross_origin()
def members():
    return {"members": ["Member1","Member2","Member3"]}

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder,'index.html')


if __name__ == "__main__":
    app.run()