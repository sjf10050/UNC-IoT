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
import json
import xlwt

def executeSQL(sql):
    try:
        db = pymysql.connect(dbconfig.db_Address, dbconfig.db_User,
                         dbconfig.db_Pwd, dbconfig.db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results=cursor.fetchall()
        db.close
        return results
    except:
        db.close
        print('fail to excute sql ')
        return 0

#写入csv、Excel
def exportToFile(tablename):
    #1:检测表名是否存在
    #2:检测文件是否存在
    #3:创建csv、excel
    filenameCSV = 'results/'+tablename+'.csv'
    filenameXLS = 'results/'+tablename+'.xls'
    sql = 'SELECT * FROM baidu.`' + tablename+ '`;'
    results = executeSQL(sql)
    workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = workbook.add_sheet('SearchRecords',cell_overwrite_ok=True)
    sheet.write(0,0, u"title")
    sheet.write(0,1, u"link")
    excelRow=1
    with codecs.open(filenameCSV, 'w', 'utf-8') as filehandle:
        write = csv.writer(filehandle, dialect='excel')
        print('in file')
        for result in results:
            write.writerow(result)#csv write in
            sheet.write(excelRow,0, str(result[1]))#xls write in
            sheet.write(excelRow,1, str(result[2]))#xls write in
            excelRow+=1
    workbook.save(filenameXLS)
    return 1


def getSearchRecords():
    data=[]
    #拉取数据库中所有的表，以json返回
    # {时间，关键词，记录数量}
    pattern = re.compile("'(.*)'")
    sql='select TABLE_NAME from information_schema.tables where TABLE_SCHEMA="baidu";'
    results = executeSQL(sql)
    for result in results:
        str_re1=pattern.findall(str(result))
        tablename=str_re1[0]
        sql='select count(*) from baidu.`'+tablename+'`;'
        num= int(re.sub(r"\D", "", str(executeSQL(sql))))
        #### 
        time=tablename[-14:]
        keyword=tablename[:-14]
        ####
        data.append([tablename,keyword,time,num]) 
    jsona = json.dumps(data)
    #print(jsona)
    return jsona


def DelResult(tablename):
    checkTableName(tablename)
    #1:删除指定表格
    # 2检测CSV Excel 并删除
    pass

def checkTableName(tablename):
    # 1 查看数据路中是否存在该表
    pass