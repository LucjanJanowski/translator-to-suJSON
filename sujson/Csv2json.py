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

    def create_dict(self, collector, headers):


        dict = {}
        os = []
        for row in collector:
            os.append(row["os"])

        for h in headers:
            dict[h] = collector[0][h]

        dict["os"] = os
        return dict

    def convert(self, path):
        json_data = []
        headers = []
        #Getting the column names into the headers array
        for col in self.df.columns:
            headers.append(col)
        headers.remove('tester_id')
        collector = []
        for index, row in self.df.iterrows():


            if len(collector) > 0 and collector[-1]["asset_id"] != row["asset_id"]:

                dict = self.create_dict(collector, headers)
                print(dict)
                json_data.append(dict)
                collector.clear()
            else:
                collector.append(row)



        fp = open(path, "w")
        json_data = json.dump(json_data, fp, indent=2)
