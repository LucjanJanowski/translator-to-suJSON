from sujson.Csv2json import Csv2json

c = Csv2json()
c.load("files/Netflix.csv", delimiter=";")
c.convert("files/Netflix_jtest.json")
