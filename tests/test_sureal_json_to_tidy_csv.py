from sujson.Json2csv import Json2csv
import unittest

class ConversionJsonToCsv(unittest.TestCase):
    def setUp(self):
        self.json_to_csv = Json2csv()

    def test_conversion(self):
        self.json_to_csv.load_json("files/Netflix.json")
        self.json_to_csv.convert("files/Netflix_ctest.csv", delimiter=";")


if __name__ == '__main__':
    unittest.main()
