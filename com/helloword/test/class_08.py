#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/14 13:41
# @Author :zhai shuai
"""
 作用
    一：标记文章为已读
 难点
    
 注意点
    一：如果取消订阅文章的id为 20521560111，运行该程序一遍，则该文章被标记为已读，
        如果该程序再运行一次且同样的文章id，则该文章又会被标记为未读，按此循环

    二：如果想取消多个，可以这样传值'xjxargs[]': '["20523721120","20523721120"]',
"""
import requests,json,re,time
from bs4 import BeautifulSoup

url2 = 'https://www.inoreader.com/'

mydata = {
    'xjxfun': 'read_article',
    'xjxargs[]': '["20589410153"]',
}
myheader={
    'cookie': 'PHPSESSID=vhhu4v92mkrmo9posdpr8oski3; al=gyhpggru67_OrZhIaMB10_FQJg9IozsTylyFonuzGiJIWQI-1560476474352316',
    'referer': 'https://www.inoreader.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'content-length': '603',
    'content-type': 'application/x-www-form-urlencoded'
}

myresponse = requests.post(url2,data=mydata,headers=myheader)
print(myresponse)