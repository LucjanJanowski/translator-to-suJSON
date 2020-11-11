from sujson._sujson import Sujson
import unittest
import os
import pandas as pd


class ExportTests(unittest.TestCase):

    def setUp(self):
        self.sujson = Sujson()
        self.incorrect_file_path = 'example/incorrect/hdtv1.json'
        self.input_file_path = 'example/hdtv5.json'
        self.sujson_format = 'suJSON'
        self.pandas_format = 'Pandas'
        self.output_csv = 'example/output.csv'
        self.output_pickle = 'example/output.pickle'

    def tearDown(self):
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)
        if os.path.exists(self.output_pickle):
            os.remove(self.output_pickle)

    def test_export_csv_sujson_format(self):
        self.sujson.export(self.input_file_path, self.sujson_format, self.output_csv)
        self.assertTrue(os.path.isfile(self.output_csv))

    def test_export_csv_pandas_format(self):
        self.sujson.export(self.input_file_path, self.pandas_format, self.output_csv)
        self.assertTrue(os.path.isfile(self.output_csv))

    def test_export_pickle_pandas_format(self):
        self.sujson.export(self.input_file_path, self.pandas_format, self.output_pickle)
        self.assertTrue(os.path.isfile(self.output_pickle))

    def test_export_pickle_sujson_format(self):
        self.sujson.export(self.input_file_path, self.sujson_format, self.output_pickle)
        self.assertTrue(os.path.isfile(self.output_pickle))

    def test_pandas_export(self):
        self.sujson._read_sujson(self.input_file_path)
        df = self.sujson.pandas_export()
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_export_incorrect_input_file(self):
        with self.assertRaises(SystemExit):
            self.sujson.export(self.incorrect_file_path, self.sujson_format, self.output_csv)

    def test_export_incorrect_output_file(self):
        with self.assertRaises(SystemExit):
            self.sujson.export(self.input_file_path, self.sujson_format, self.incorrect_file_path)


if __name__ == '__main__':
    unittest.main()
