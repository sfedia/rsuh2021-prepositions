import json
import os
import re
from datetime import datetime


class Dataset:
    def __init__(self, dataset_name):
        self.j = json.loads(open(os.path.join("files/datasets", f"{dataset_name}.json"), encoding="utf-8").read())

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
