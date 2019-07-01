#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/12 9:38
# @Author :zhai shuai
"""
 作用
    一：模拟点击全部文章的按钮，查询出订阅频道的文章
    二：可以实现的效果是 取出的字段是：文章id号--文章title--文章发布时间--文章内容--文章所属频道的id
 难点
    一：对返回数据的处理，要转换成html进行解析
    二：用到了正则表达式取出想要的数据
 注意点
    一：熟悉print_articles返回数据的json格式，并找出想要的数据
"""

import requests,json,re,time
from bs4 import BeautifulSoup

url2 = 'https://www.inoreader.com/'
mydata = {
    'xjxfun': 'print_articles'
}
myheader={
    # 'cookie': '_ga=GA1.2.592634811.1560232436; _gid=GA1.2.2086943265.1560232436; screen_pixel_ratio=1.125; screen_resolution=1536x864; device_type=normal; OAID=2fd986ed236324f9105ca6cf43621701; PHPSESSID=sq6qtjg3vjocngbjp7h266n811; al=ssNij_i4iGQbZk1Xf60zttYctCt9JxdMajG04I162YMBfHf-1560302105463424; OAGEO=CN%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C; _gat=1; feed_params=%7B%22filter_type%22%3A%22subscription%22%2C%22filter_id%22%3A%2272688566%22%7D; window_dimensions=1707x387',
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
divContent=json.loads(myresponse.content).get('xjxobj')[9]['data'][0]

print(divContent)
print(type(divContent))
for temp in divContent.items():  #转成元组

    soup = BeautifulSoup(temp[1], 'html.parser')
    print("文章id号："+temp[0])
    print("文章title: "+soup.find("a",attrs={"id":"article_title_link_"+temp[0]}).text)

    #日期有两种格式，一个是   %a %b %d, %Y %H:%M  一个是：%H:%M
    articleTime = soup.find("div", attrs={"class": "header_date"}).attrs['title']
    searchObj = articleTime.split(": ")
    publicDate = searchObj[2]
    if(re.search(r'^\d{2}:\d{2}',publicDate)):
        strTime = time.strftime("%Y-%m-%d ")+publicDate
    else:
        timeStruct = time.strptime(publicDate, "%a %b %d, %Y %H:%M")
        strTime = time.strftime("%Y-%m-%d %H:%M", timeStruct)
    print("文章时间："+strTime)
    print("文章内容：" + soup.find("div", attrs={"class": "article_content"}).text)
    #新闻对应的频道
    regex = re.compile(r"article_feed_info_click.*")
    pingdaoIds = soup.find("a",attrs={"onclick":regex}).attrs['onclick']
    searchObj = re.search(r'article_feed_info_click(.*)', pingdaoIds)
    publicDate = searchObj.group(1).split(",")[1].replace("'",'')

    print("文章频道id："+publicDate)
    print("-----------------------------------------------------------------------------------------------")

