import json
import logging
import os
import re
import sys

from flask import Flask
from flask import Markup
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from . import query

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


def get_dataset_profile(dataset_name):
    corpus, prep, branch, criterion = dataset_name.split("_")
    meta_file = json.loads(open(os.path.join("files/meta", "datasets.json"), encoding="utf-8").read())
    this_dataset = None
    for dataset in meta_file["datasets_meta"]:
        if dataset["name"].replace(":", "_") == dataset_name:
            this_dataset = dataset
            break
    ds_file = json.loads(open(os.path.join("files/datasets", f"{dataset_name}.json"), encoding="utf-8").read())
    valid_matches = len(ds_file["nk:datasetContent"]["items"])
    del ds_file
    return {
        "preposition": this_dataset["prepositionVariants"],
        "property": criterion,
        "matches": {
            "all": this_dataset["allMatches"],
            "processed": this_dataset["processedMatches"],
            "valid": valid_matches
        },
        "query": this_dataset["query"],
        "query_efficiency": str(int(round(valid_matches / this_dataset["processedMatches"], 2)*100)) + "%"
    }


@app.route("/dataset-profile/<dataset_name>")
def show_dataset_profile(dataset_name):
    profile = get_dataset_profile(dataset_name)
    profile["preposition"] = Markup(profile["preposition"])
    profile["query"] = Markup(query.CorpusQuery(profile["query"]).to_markup())
    return render_template("dataset-profile.html", dataset_name=dataset_name, meta=profile)


@app.route("/diachronic/<dataset_name>")
def diachronic(dataset_name):
    j = json.loads(open(os.path.join("files/datasets", f"{dataset_name}.json"), encoding="utf-8").read())
    years = {}
    for item in j["nk:datasetContent"]["items"]:
        extracted_date = re.search(r"(\d{4})\)?$", item["title"])
        if extracted_date:
            year_value = int(extracted_date.group(1))
            if year_value not in years:
                years[year_value] = 1
            else:
                years[year_value] += 1
    return jsonify({
         "stats": [{"x": year, "y": years[year] if year in years else 0} for year in range(1800, 2021 + 1)]
     })
