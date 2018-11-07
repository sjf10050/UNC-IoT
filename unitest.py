# -*- coding: utf-8 -*-
import unittest
from restfulAPI import *
from dbAPI import *
import baidu
import os
import csv


class TestdbAPI(unittest.TestCase):
    def test_exportToFile(self):
        self.assertEqual(0, exportToFile('fnsjkhgnv'))
        tableName = baidu.creatTable('hnbvusbagbngfd')
        baidu.saveNewResult(tableName, 'aaa', 'bbb')
        self.assertEqual(1, exportToFile(tableName))
        self.assertTrue(os.path.isfile('results/'+tableName+'.csv'))
        self.assertTrue(os.path.isfile('results/'+tableName+'.xls'))
        if(os.path.isfile('results/'+tableName+'.csv')):
            os.remove(('results/'+tableName+'.csv'))
        if(os.path.isfile('results/'+tableName+'.xls')):
            os.remove(('results/'+tableName+'.xls'))
        DelResult(tableName)

    def test_getSearchRecords(self):
        self.assertIsInstance(getSearchRecords(), str)
        # self.assertIsNotNone(getSearchRecords()[0])

    def test_DelResult(self):
        self.assertEqual(0, DelResult('fnsjkhgnv'))
        self.assertEqual(1, DelResult(baidu.creatTable('hnbvusbagbngfd')))


if __name__ == '__main__':
    unittest.main()
