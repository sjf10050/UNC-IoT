# -*- coding: utf-8 -*-
import unittest
from restfulAPI import *
from dbAPI import *

class TestdbAPI(unittest.TestCase):
    def test_exportToFile(self):
        self.assertEqual(0,exportToFile('aaa'))

    def test_getSearchRecords(self):
        self.assertIsInstance(getSearchRecords(),str)# detect the return value
        # with self.assertRaises(ValueError):
        #     exportToFile('*')


# class TestRestfulAPI(unittest.TestCase):
#     def test_getresultcount(self):
#         pass


if __name__ == '__main__':
    unittest.main()
