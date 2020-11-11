from sujson._sujson import Sujson
import unittest


class BuildDataFrameTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sujson = Sujson()
        cls.input_file_path = 'example\hdtv5.json'

    def test_build(self):
        self.sujson._read_sujson(self.input_file_path)

        for trial in self.sujson.sujson['trials']:
            self.sujson.build_dataframe(trial, trial['pvs_id'], trial['score_id'])

        self.assertTrue(isinstance(self.sujson.dataframe, dict))

        self.assertEqual(None, self.sujson.dataframe.get('hrc')[0])
        self.assertEqual(3, self.sujson.dataframe.get('stimulus_id')[2])
        self.assertEqual(1, self.sujson.dataframe.get('subject_id')[0])
        self.assertEqual(2, self.sujson.dataframe.get('subject_id')[200])


if __name__ == '__main__':
    unittest.main()
