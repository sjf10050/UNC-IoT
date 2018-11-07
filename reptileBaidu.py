# -*- coding:utf-8 -*-
import multiprocessing
import time
from bs4 import BeautifulSoup
import sys
import requests
from urllib import request
import urllib
import pymysql
import re
import random
import string
import config as config
import dbconfig as dbconfig
from DBUtils.PooledDB import PooledDB

dbPool = PooledDB(pymysql,5,host=dbconfig.db_Address,user=dbconfig.db_User,passwd=dbconfig.db_Pwd,db=dbconfig.db_name,port=3306)

headers = config.headers

class reptileBaidu():
    def __init__(self, keyword,dbPool,headers):
        self.keyword=keyword
        self.tablename=keyword+str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        self.__dbPool = dbPool
        self.__countTag()
        self.__getResultCount()
        self.__headers=headers

    def __getResultCount(self):
        url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(self.keyword)
        response = request.urlopen(url)
        page = response.read()
        soup = BeautifulSoup(page, 'lxml')
        for x in soup.find_all('span', string=re.compile('百度为您找到相关结果')):
            result = int((re.sub(r"\D", "", x.renderContents().decode("utf-8"))))
            self.ResultCount=result
            return result
    
    def __countTag(self):
        response = request.urlopen('http://www.baidu.com')
        page = response.read()
        soup = BeautifulSoup(page, 'lxml')
        self.tagCount=len(list(soup.find_all(True)))
    def printtagCount(self):
        print(self.tagCount)
result_google=reptileBaidu('google',dbPool,config.headers)
print(result_google.tagCount)
result_google.printtagCount()
dbPool.close()