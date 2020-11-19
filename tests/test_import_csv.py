from sujson._sujson import Sujson
import unittest
import os
from pathlib import Path
from io import StringIO
import sys

# should be run in main project directory
class ImportCsvTests(unittest.TestCase):

    def setUp(self):
        self.sujson = Sujson()
        self.incorrect_input_file_path = str(Path('example', 'incorrect', 'hdtv1.json'))
        self.incorrect_input_file_format = str(Path('example', 'data', 'VQEG_HDTV_Final_Report_Data.xls'))
        self.incorrect_output_file_format = str(Path('example', 'output.pickle'))
        self.input_file_path = str(Path('example', 'data', 'subjective_quality_datasets.csv'))
        self.output_sujson = str(Path('example', 'output.json'))
        self.config_file = str(Path('example', 'config', 'config_for_hdtv_csv.json'))

    def tearDown(self):
        if os.path.exists(self.output_sujson):
            os.remove(self.output_sujson)

    def test_import_csv(self):
        self.sujson.import_csv(self.input_file_path, self.config_file, output_file=self.output_sujson)
        self.assertTrue(os.path.isfile(self.output_sujson))

    def test_import_csv_without_output_file(self):
        # redirecting standard output to variable result
        stdout = sys.stdout
        stdout_from_function = StringIO()
        sys.stdout = stdout_from_function

        self.sujson.import_csv(self.input_file_path, self.config_file)
        sys.stdout = stdout
        self.assertIn('sujson_version', stdout_from_function.getvalue())

    def test_import_csv_incorrect_input_path(self):
        with self.assertRaises(SystemExit):
            self.sujson.import_csv(self.incorrect_input_file_path, self.config_file, output_file=self.output_sujson)

    def test_import_csv_incorrect_input_file_format(self):
        with self.assertRaises(SystemExit):
            self.sujson.import_csv(self.incorrect_input_file_format, self.config_file, output_file=self.output_sujson)

    def test_import_csv_incorrect_output_file_format(self):
        with self.assertRaises(SystemExit):
            self.sujson.import_csv(self.input_file_path, self.config_file, output_file=self.incorrect_input_file_format)


if __name__ == '__main__':
    unittest.main()
