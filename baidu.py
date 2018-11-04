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

try:
    db = pymysql.connect(dbconfig.db_Address, dbconfig.db_User,
                         dbconfig.db_Pwd, dbconfig.db_name)
    cursor = db.cursor()
except:
    db.close

headers = config.headers

def creatTable(keyword):
    tablename = keyword+str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
    sql = "CREATE TABLE `baidu`.`%s` (\
        `ID` INT NOT NULL AUTO_INCREMENT,\
        `s_title` VARCHAR(45) NULL,\
        `s_link` VARCHAR(120) NULL,\
        PRIMARY KEY (`ID`));" % (tablename)
    try:
        cursor.execute(sql)
        db.commit()
        return tablename
    except:
        db.rollback()
        return 0
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
        cursor.execute(sql)
    except:
        db.rollback()

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
            #print(title)
            #print(real_url)
            saveNewResult(tablename, ''+title, ''+real_url)
        db.commit()


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
        result = pool.apply_async(
            geturl, (path, tablename))  # use multi processing
    pool.close()
    pool.join()


if __name__ == '__main__':
    try:
        print('Report:  '+str(countTag('http://www.baidu.com'))+' tags')
        getfromBaidu('china unicom')
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        db.commit()
        db.close()
