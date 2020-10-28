from sujson._sujson import Sujson
import unittest
import os
import pandas as pd
from sujson._errors import SujsonError

# TODO @awro1444 Please change the name of this file to test_export.py


class ExportTests(unittest.TestCase):
    # TODO @awro1444 Put these lines into the constructor or into the setUp() function
    # TODO @awro1444 Make sure the code is portable. Please add any relevant files to the repo
    sujson = Sujson()
    incorrect_file_path = 'D:\\incorrect\hdtv1.json'
    input_file_path = 'D:\\translator-to-suJSON-master\hdtv5.json'
    sujson_format = 'suJSON'
    pandas_format = 'Pandas'
    output_csv = 'example\output.csv'
    output_pickle = 'example\output.pickle'

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
        with self.assertRaises(SujsonError):
            self.sujson.export(self.incorrect_file_path, self.sujson_format, self.output_csv)

    def test_export_incorrect_output_file(self):
        self.assertRaises(SujsonError,
                          self.sujson.export(self.input_file_path, self.sujson_format, self.incorrect_file_path))

# TODO @awro1444 We are missing the main function :)
