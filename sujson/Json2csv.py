import pandas as pd
import json
from copy import copy
class Json2csv:
    def __init__(self):
        self.df = None
        self.json_data = []
        self.csv_headers = []

    def load_json(self, path):
        with open(path, encoding='utf8') as f:
            self.json_data = json.load(f)

        new_table = []

        for dict in self.json_data:
            id = 0
            os = dict["os"]
            copied_dict = dict
            for o in os:
                copied_dict["tester_id"] = id
                id+=1
                copied_dict["os"] = o
                new_table.append(copy(copied_dict))

            self.json_data = new_table
        return self.json_data

    def convert(self, path, delimiter=","):
        if len(self.json_data) == 0:
            return pd.DataFrame() #Returns an empty dataframe object

        #We load and save the names of the columns
        headers = []
        for key in self.json_data[0].keys():
            headers.append(key)
        self.csv_headers = headers

        df = pd.DataFrame(self.json_data, columns=headers)
        df.to_csv(path, index=False, sep=delimiter)
        self.df = df
        return df
