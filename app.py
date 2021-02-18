from flask import Flask
from flask import send_from_directory
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/datasets")
def show_datasets():
    return send_from_directory("files/ui", "datasets.html")

@app.route("/meta.json/<filename>")
def meta_json_file(filename):
    return send_from_directory("files/meta", filename)

@app.route("/datasets.json/<filename>")
def datasets_json_file(filename):
    return send_from_directory("files/datasets", filename)
