from sujson._sujson import Sujson
import unittest

# should be run in main project directory
class FindByValueTests(unittest.TestCase):

    def setUp(self):
        self.sujson = Sujson()
        self.my_list = []
        for i in range(100):
            self.my_list.append({"key": "a" + str(i)})

        self.my_list.append({"key2": {"key3": 3}})
        self.my_list.append({"key2.0": [{"key3.0": 30}]})

    def test_find_by_value(self):
        index = self.sujson.find_by_value("key", "a30", self.my_list)
        self.assertEqual(30, index)

    def test_find_by_nonexistent_value(self):
        index = self.sujson.find_by_value("key", "6", self.my_list)
        self.assertEqual(None, index)

    def test_find_by_nonexistent_key(self):
        index = self.sujson.find_by_value("incorrect_key", "a20", self.my_list)
        self.assertEqual(None, index)

    def test_find_by_value_dictionary(self):
        index = self.sujson.find_by_value("key2", {"key3": 3}, self.my_list)
        self.assertEqual(100, index)

    def test_find_by_value_dictionary_within_dictionary(self):
        index = self.sujson.find_by_value("key3.0", 30, self.my_list[101].get('key2.0'))
        self.assertEqual(0, index)


if __name__ == '__main__':
    unittest.main()
