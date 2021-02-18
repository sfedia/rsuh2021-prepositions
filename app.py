from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask import render_template
import logging
import json
import os
import re
import sys

app = Flask(__name__, template_folder=os.path.abspath("files/ui/templates"))
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

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

@app.route("/dataset-profile/<dataset_name>")
def show_dataset_profile(dataset_name):
    return render_template("dataset-profile.html", dataset_name=dataset_name)


@app.route("/diachronic/<dataset_name>")
def diachronic(dataset_name):
    j = json.loads(open(os.path.join("files/datasets", f"{dataset_name}.json"), encoding="utf-8").read())
    years = {}
    for item in j["nk:datasetContent"]["items"]:
        extractedDate = re.search(r"(\d{4})\)?$", item["title"])
        if extractedDate:
            yearValue = int(extractedDate.group(1))
            if yearValue not in years:
                years[yearValue] = 1
            else:
                years[yearValue] += 1
    return jsonify({
         "stats": [{"x": year, "y": years[year] if year in years else 0} for year in range(1800, 2021 + 1)]
     })
