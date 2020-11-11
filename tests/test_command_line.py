from sujson._sujson import Sujson
import unittest
import subprocess
from subprocess import PIPE
import sys
import os


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.sujson = Sujson()
        self.input_file = 'example/hdtv5.json'
        self.incorrect_file_path = 'example/incorrect/hdtv1.json'
        self.sujson_format = 'suJSON'
        self.pandas_format = 'Pandas'
        self.output_csv = 'example/output.csv'
        self.output_pickle = 'example/output.pickle'
        self.output_json = "example/output.json"
        self.incorrect_output_path = "example/incorrect/output.pickle"

    def tearDown(self):
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)
        if os.path.exists(self.output_pickle):
            os.remove(self.output_pickle)
        if os.path.exists(self.output_json):
            os.remove(self.output_json)

    def run_command(self, args):
        cmd_args = [sys.executable, "-m", "sujson"]
        cmd_args = cmd_args + args
        return subprocess.Popen(cmd_args, stdout=PIPE, stderr=PIPE, text=True)

    def test_ingest_csv(self):
        proc = self.run_command(
            ["ingest", "example/data/subjective_quality_datasets.csv",
             "-c", "example/config/config_for_hdtv_csv.json",
             "-o", self.output_json])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_json))

    def test_ingest_xlsx(self):
        proc = self.run_command(
            ["ingest", "example/data/VQEG_HDTV_Final_Report_Data.xls",
             "-c", "example/config/config_for_hdtv.json",
             "-o", self.output_json])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_json))

    def test_export_to_pickle_pandas_format(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.output_pickle,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_pickle))

    def test_export_to_pickle_sujson_format(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.output_pickle,
             "-f", self.sujson_format])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_pickle))

    def test_export_to_csv_pandas_format(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.output_csv,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_csv))

    def test_export_to_csv_sujson_format(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.output_csv,
             "-f", self.sujson_format])

        outs, errs = proc.communicate()

        self.assertEqual('ERROR: For suJSON format only .pickle output file is allowed\n', outs)
        self.assertFalse(os.path.isfile(self.output_csv))

    def test_incorrect_input_path(self):
        proc = self.run_command(
            ["export", self.incorrect_file_path,
             "-o", self.output_csv,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()

        self.assertEqual('ERROR: That is not a correct input path: {}\n'.format(self.incorrect_file_path), outs)
        self.assertFalse(os.path.isfile(self.output_csv))

    def test_incorrect_output_path(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.incorrect_output_path,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()

        self.assertEqual('ERROR: That is not a correct output path: {}\n'.format(self.incorrect_output_path), outs)
        self.assertFalse(os.path.isfile(self.output_csv))


if __name__ == '__main__':
    unittest.main()
