# -*- coding: utf-8 -*-
import unittest
from restfulAPI import *
from dbAPI import *
import baidu
class TestdbAPI(unittest.TestCase):
    def test_exportToFile(self):
        self.assertEqual(0,exportToFile('aaa'))

    def test_getSearchRecords(self):
        self.assertIsInstance(getSearchRecords(),str)

    def test_DelResult(self):
        self.assertEqual(0,DelResult('fnsjkhgnv'))
        self.assertEqual(1,DelResult(baidu.creatTable('hnbvusbagbngfd')))
        

# class TestBaidu(unittest.TestCase):
#     def test_exportToFile(self):
#         self.assertEqual(0,exportToFile('aaa'))

#     def test_getSearchRecords(self):
#         self.assertIsInstance(getSearchRecords(),str)# detect the return value
        # with self.assertRaises(ValueError):
        #     exportToFile('*')


# class TestRestfulAPI(unittest.TestCase):
#     def test_getresultcount(self):
#         pass


if __name__ == '__main__':
    unittest.main()
