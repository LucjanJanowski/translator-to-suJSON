import unittest

from tests.test_build_dataframe import BuildDataFrameTests
from tests.test_command_line import CommandLineTests
from tests.test_export import ExportTests
from tests.test_find_by_value import FindByValueTests


def suite():
    suite = unittest.TestSuite()
    suite.addTest(BuildDataFrameTests('test01'))
    suite.addTest(FindByValueTests('test01'))
    suite.addTest(FindByValueTests('test02'))
    suite.addTest(FindByValueTests('test03'))
    suite.addTest(FindByValueTests('test04'))
    suite.addTest(FindByValueTests('test05'))
    suite.addTest(CommandLineTests('test_ingest_csv'))
    suite.addTest(CommandLineTests('test_ingest_xlsx'))
    suite.addTest(ExportTests('test_export_csv_sujson_format'))
    suite.addTest(ExportTests('test_export_csv_pandas_format'))
    suite.addTest(ExportTests('test_export_pickle_pandas_format'))
    suite.addTest(ExportTests('test_export_pickle_sujson_format'))
    suite.addTest(ExportTests('test_pandas_export'))
    suite.addTest(ExportTests('test_export_incorrect_input_file'))
    suite.addTest(ExportTests('test_export_incorrect_output_file'))
    return suite


if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(suite())
    unittest.main()
