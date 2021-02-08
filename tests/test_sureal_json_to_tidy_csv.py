from sujson.Json2csv import Json2csv
j = Json2csv()
j.load_json("files/Netflix.json")
j.convert("files/Netflix_ctest.csv", delimiter=";")
