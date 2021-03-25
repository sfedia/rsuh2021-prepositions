import json
import os
import re
from datetime import datetime
from collections import namedtuple

dataset_simple_item = namedtuple("DatasetSimpleItem", "title text")


class Dataset:
    def __init__(self, dataset_name, file_prefix=""):
        self.j = json.loads(
            open(os.path.join(file_prefix, "files", "datasets", f"{dataset_name}.json"), encoding="utf-8").read())

    def get_matches_count(self):
        return len(self.j["nk:datasetContent"]["items"])

    def by_years(self):
        now = datetime.now()
        min_limit = 1800
        years = {}
        for item in self.j["nk:datasetContent"]["items"]:
            extracted_date = re.search(r"(\d{4})\)?$", item["title"])
            if extracted_date:
                year_value = int(extracted_date.group(1))
                if year_value not in years:
                    years[year_value] = 1
                else:
                    years[year_value] += 1
                if year_value < min_limit:
                    min_limit = year_value
        return [
            {
                "x": year,
                "y": years[year] if year in years else 0
            } for year in range(min_limit, now.year + 1)
        ]

    @staticmethod
    def get_item_link(item):
        if "itemExpandURL" not in item:
            return f'<a href=\'{item["itemURL"]}\'>смотреть в НКРЯ</a>'
        else:
            return f'<a href=\'{item["itemExpandURL"]}\'>смотреть в НКРЯ</a>' +\
            f'<sup><b><a href=\'{item["itemURL"]}\'>(Q)</a></b></sup>'

    def item_simple_reader(self, offset=0, until=None):
        for item in self.j["nk:datasetContent"]["items"][offset:until]:
            yield dataset_simple_item(
                title=item["title"],
                text="".join([f'<span class=\'text-block {b["status"]}\'>{b["text"]}</span>' for b in item["text"]])
            )
