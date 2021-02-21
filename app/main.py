import json
import logging
import os
import sys

from flask import Flask
from flask import Markup
from flask import jsonify
from flask import request
from flask import render_template
from flask import send_from_directory
from app.dataset import Dataset
from app.dataset import dataset_simple_item
from app.query import CorpusQuery

app = Flask(__name__, template_folder=os.path.abspath("files/ui/templates"))
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route("/")
def main_page():
    return send_from_directory("../files/ui", "main_page.html")


@app.route("/datasets")
def show_datasets():
    return send_from_directory("../files/ui", "datasets.html")


@app.route("/static/<filename>")
def response_static(filename):
    return send_from_directory("../files/static", filename)


@app.route("/meta.json/<filename>")
def meta_json_file(filename):
    return send_from_directory("../files/meta", filename)


@app.route("/datasets.json/<filename>")
def datasets_json_file(filename):
    return send_from_directory("../files/datasets", filename)


def get_dataset_profile(dataset_name):

    corpus, prep, branch, criterion = dataset_name.split("_")
    meta_file = json.loads(open(os.path.join("files/meta", "datasets.json"), encoding="utf-8").read())
    this_dataset = None
    for dataset in meta_file["datasets_meta"]:
        if dataset["name"].replace(":", "_") == dataset_name:
            this_dataset = dataset
            break
    valid_matches = Dataset(dataset_name).get_matches_count()

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
    qis = type(profile["query"]) == str
    if qis:
        profile["query"] = Markup(CorpusQuery(profile["query"]).to_markup())
    else:
        profile["query"] = [Markup(CorpusQuery(q).to_markup()) for q in profile["query"]]
    return render_template("dataset-profile.html", dataset_name=dataset_name, meta=profile, query_is_string=qis,
                           enumerate=enumerate, len=len)


@app.route("/diachronic/<dataset_name>")
def diachronic(dataset_name):
    return jsonify({
         "stats": Dataset(dataset_name).by_years()
     })


@app.route("/dataset-json/<dataset_name>")
def dataset_json(dataset_name):
    _from = int(request.args.get("from", 0))
    _until = request.args.get("until", None)
    if _until:
        _until = int(_until)

    return jsonify({
        "data": [item._asdict() for item in Dataset(dataset_name).item_simple_reader(_from, _until)]
    })


@app.route("/view-matches/<dataset_name>")
def view_matches(dataset_name):
    return render_template("dataset-matches.html", dataset_name=dataset_name)
