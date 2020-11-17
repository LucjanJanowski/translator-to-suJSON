from sujson._sujson import Sujson
from subprocess import PIPE
from pathlib import Path
import unittest
import subprocess
import sys
import os


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.sujson = Sujson()
        self.input_file = str(Path('example', 'hdtv5.json'))
        self.incorrect_file_path = str(Path('example', 'incorrect', 'hdtv1.json'))
        self.sujson_format = 'suJSON'
        self.pandas_format = 'Pandas'
        self.output_csv = str(Path('example', 'output.csv'))
        self.output_pickle = str(Path('example', 'output.pickle'))
        self.output_json = str(Path('example', 'output.json'))
        self.incorrect_output_path = str(Path('example', 'incorrect', 'output.pickle'))

    def tearDown(self):
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)
        if os.path.exists(self.output_pickle):
            os.remove(self.output_pickle)
        if os.path.exists(self.output_json):
            os.remove(self.output_json)

    def run_command(self, args):
        cmd_args = [sys.executable, '-m', 'sujson']
        cmd_args = cmd_args + args
        return subprocess.Popen(cmd_args, stdout=PIPE, stderr=PIPE, text=True)

    def test_ingest_csv(self):
        csv_hdtv_test = str(Path('example', 'data', 'subjective_quality_datasets.csv'))
        csv_hdtv_config = str(Path('example', 'config', 'config_for_hdtv_csv.json'))
        proc = self.run_command(
            ["ingest", csv_hdtv_test,
             "-c", csv_hdtv_config,
             "-o", self.output_json])

        outs, errs = proc.communicate()
        self.assertEqual('', errs)
        self.assertTrue(os.path.isfile(self.output_json))

    def test_ingest_xlsx(self):
        xls_hdtv_test = str(Path('example', 'data', 'VQEG_HDTV_Final_Report_Data.xls'))
        xls_hdtv_config = str(Path('example', 'config', 'config_for_hdtv.json'))
        proc = self.run_command(
            ["ingest", xls_hdtv_test,
             "-c", xls_hdtv_config,
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

        self.assertIn('ERROR', outs)
        self.assertFalse(os.path.isfile(self.output_csv))

    def test_incorrect_input_path(self):
        proc = self.run_command(
            ["export", self.incorrect_file_path,
             "-o", self.output_csv,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()

        self.assertIn('ERROR', outs)
        self.assertFalse(os.path.isfile(self.output_csv))

    def test_incorrect_output_path(self):
        proc = self.run_command(
            ["export", self.input_file,
             "-o", self.incorrect_output_path,
             "-f", self.pandas_format])

        outs, errs = proc.communicate()

        self.assertIn('ERROR', outs)
        self.assertFalse(os.path.isfile(self.output_csv))


if __name__ == '__main__':
    unittest.main()
