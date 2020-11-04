from sujson._sujson import Sujson
import unittest
import pprint


# TODO @awro1444 Change the name of the class to something like BuildDataframeTests
class FindByValueTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sujson = Sujson()
        cls.input_file_path = 'example\hdtv5.json'

    def test01(self):
        self.sujson._read_sujson(self.input_file_path)

        for trial in self.sujson.sujson['trials']:
            self.sujson.build_dataframe(trial, trial['pvs_id'], trial['score_id'])

        self.assertTrue(isinstance(self.sujson.dataframe, dict))

        self.assertEqual(None, self.sujson.dataframe.get('hrc')[0])
        self.assertEqual(3, self.sujson.dataframe.get('stimulus_id')[2])
        self.assertEqual(1, self.sujson.dataframe.get('subject_id')[0])
        self.assertEqual(2, self.sujson.dataframe.get('subject_id')[200])




