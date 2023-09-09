from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "ppp"


@app.route("/test", methods=['POST'])
def test():
    data = request.get_json()
    return data

