from sujson._sujson import Sujson
import unittest

class FindByValueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sujson = Sujson()
        cls.my_list = []
        for i in range(100):
            cls.my_list.append({"key": "a"+str(i)})

        cls.my_list.append({"key2": {"key3": 3}})
        cls.my_list.append({"key2.0": [{"key3.0": 30}]})

    def test01(self):
        index = self.sujson.find_by_value("key", "a30", self.my_list)
        self.assertEqual(30, index)

    def test02(self):
        index = self.sujson.find_by_value("key", "6", self.my_list)
        self.assertEqual(None, index)

    def test03(self):
        index = self.sujson.find_by_value("incorrect_key", "a20", self.my_list)
        self.assertEqual(None, index)

    def test04(self):
        index = self.sujson.find_by_value("key2", {"key3": 3}, self.my_list)
        self.assertEqual(100, index)

    def test05(self):
        index = self.sujson.find_by_value("key3.0", 30, self.my_list[101].get('key2.0'))
        self.assertEqual(0, index)


if __name__ == '__main__':
    unittest.main()
