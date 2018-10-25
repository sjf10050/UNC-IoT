# -*- coding:utf-8 -*-
'''
从百度把前10页的搜索到的url爬取保存
'''
import multiprocessing   #利用pool进程池实现多进程并行
#  from threading import Thread 多线程
import time
from bs4 import BeautifulSoup    #处理抓到的页面
import sys
import requests
from urllib import request
import urllib
import pymysql
import re


 
 
if __name__ == '__main__':
    #getfromBaidu('中国联通')
    #print(120//10+1)
    sql="INSERT INTO `baidu`.`%s` (`s_title`, `s_link`) VALUES ('12', '33');"%(name,)

    for i in range(12//10+1):
        print (i)
    #db.commit()
    #db.close()
    #url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote('中国联通')
    #print(getresultcount(url))
    #print(res_count('http://www.baidu.com/s?wd=中国联通'))

