import pandas as pd
import json


class Csv2json:
    def __init__(self):
        self.df = None
        self.headers = []

    def load(self, path, delimiter=","):
        df = pd.read_csv(path, delimiter=delimiter)
        self.df = df
        return df

    def convert(self, path):
        json_data = []
        os = {}
        asset_id = []
        content_id = []
        path_data = []
        for index, row in self.df.iterrows():
            if row["asset_id"] not in asset_id:
                asset_id.append(row["asset_id"])
                content_id.append(row["content_id"])
                id = row["asset_id"]
                path_data.append(row["path"])
                os[id] = []

        for index, row in self.df.iterrows():
            os[row["asset_id"]].append(row["os"])

        for i in range(len(asset_id)):
            json_data.append(dict())
            json_data[-1]["asset_id"] = asset_id[i]
            json_data[-1]["content_id"] = content_id[i]
            json_data[-1]["os"] = os[asset_id[i]]
            json_data[-1]["path"] = path_data[i]

        fp = open(path, "w")
        json_data = json.dump(json_data, fp, indent=2)
        fp.close()
