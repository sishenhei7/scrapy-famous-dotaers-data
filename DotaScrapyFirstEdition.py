#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 10:36:00 2016

@author: yangzhou
"""
import requests
import re
from bs4 import BeautifulSoup
import xlwt
import urllib2
import urllib
import sys
def get_excel():
    book = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheet = book.add_sheet('data',cell_overwrite_ok = True)
    url='http://dotamax.com/player/match/149486894/?skill=&ladder=&hero=-1'
    global dt
    j = 0
    a=[1,2,3,4,5,6,7,8]
    reload(sys)
    sys.setdefaultencoding('utf8')
    for i in a:
        url=url+'&p='+str(i)
        
#    url = 'http://www.douban.com'
#    info = {'p' : '1'}
#    data = urllib.urlencode(info)
 #   print(data)
 #   req = urllib2.Request(url, data)
 #   print(req)
        h=urllib2.urlopen(url)

    #修改下面的 datelist() 修改起止时间
#    dt = {'cdateEnd':each,'pageNo1':'1','pageNo2':''}
#    get_html()
        soup = BeautifulSoup(h)
    #j = 0
        for tabb in soup.find_all('tr'):
            i=0;
            for tdd in tabb.find_all('td'):
                #print (tdd.get_text()+",",)
                sheet.write(j,i,tdd.get_text())
                i = i+1
            j=j+1
        book.save(r'result.xls') #修改这里更改保存的文件名
get_excel()


























