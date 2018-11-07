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
import csv
import codecs
from DBUtils.PooledDB import PooledDB

dbPool = PooledDB(pymysql,8,host=dbconfig.db_Address,user=dbconfig.db_User,passwd=dbconfig.db_Pwd,db=dbconfig.db_name,port=3306)

headers = config.headers


def creatTable(keyword):
    tablename = keyword + \
        str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    sql = "CREATE TABLE `baidu`.`%s` (\
        `ID` INT NOT NULL AUTO_INCREMENT,\
        `s_title` VARCHAR(45) NULL,\
        `s_link` VARCHAR(120) NULL,\
        PRIMARY KEY (`ID`));" % (tablename)
    try:
        conn = dbPool.connection()
        cursor=conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return tablename
    except:
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
    return 0


def countTag(targetURL):
    response = request.urlopen(targetURL)
    page = response.read()
    soup = BeautifulSoup(page, 'lxml')
    return len(list(soup.find_all(True)))


def saveNewResult(s_table, s_Title, s_Link):
    sql = "INSERT INTO `baidu`.`%s` (`s_title`, `s_link`) VALUES ('%s', '%s');" % \
        (s_table, s_Title, s_Link)
    try:
        conn = dbPool.connection()
        cursor=conn.cursor()
        cursor.execute(sql)
        conn.commit
    except:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def getresultcount(word):
    url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(word)
    response = request.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'lxml')
    for x in soup.find_all('span', string=re.compile('百度为您找到相关结果')):
        result = int((re.sub(r"\D", "", x.renderContents().decode("utf-8"))))
        print('results count:  '+str(result))
        return result


def geturl(path, tablename):
    response = request.urlopen(path)
    page = response.read()
    soup = BeautifulSoup(page, 'lxml')
    tagh3 = soup.find_all('h3')
    for h3 in tagh3:
        href = h3.find('a').get('href')
        title = h3.find('a').renderContents().decode("utf-8")
        title = re.sub(r'<.+?>', "", title)
        title.strip()
        baidu_url = requests.get(
            url=href, headers=headers, allow_redirects=False)
        real_url = baidu_url.headers['Location']  # Get origin URl
        if real_url.startswith('http'):
            saveNewResult(tablename, ''+title, ''+real_url)
            print(title)
            print(real_url)



def getfromBaidu(word):
    tablename = creatTable(word)
    if tablename == 0:
        return 0
    url = config.targerWeb + urllib.parse.quote(word)
    pool = multiprocessing.Pool(config.threadnum)
    pagecount = getresultcount(word)//10
    if pagecount >= 76:
        pagenum = 76
    else:
        pagenum = pagecount
    for i in range(pagenum):
        path = url + '&pn='+str(i)
        result = pool.apply_async(geturl, (path, tablename))  # use multi processing
    pool.close()
    pool.join()

if __name__ == '__main__':
    try:
        print('Report:  '+str(countTag('http://www.baidu.com'))+' tags')
        getfromBaidu('china unicom')
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        dbPool.close()