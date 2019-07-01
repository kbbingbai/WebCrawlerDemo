#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/11 23:04
# @Author :zhai shuai
"""
 作用
    一：模拟某个用户进行登陆
    二：取出登陆用户订阅的频道我名称与id号
 难点
    一：对返回数据的处理，要转换成html进行解析
    二：用到了正则表达式取出想要的数据
 注意点
    一：熟悉build_tree返回数据的json格式，并找出想要的数据
    二：这里的cookie写死了
"""

import requests, json, re
from bs4 import BeautifulSoup

# ----------------------实现用户名与密码的登陆------------------------------------------
url = "https://www.inoreader.com/login"
params = {
    "username": "1617079905@qq.com",
    "password": "1617079905",
    "warp_action": "login",
    "remember_me": "no"
}
loginResponse = requests.post(url, data=params)


# -----------------------获取 该用户订阅的频道名称与频道id-------------------------------------------
url2 = 'https://www.inoreader.com/'
mydata = {
    'xjxfun': 'build_tree',
    'xjxr': '1560238356193'
}

myheader = {
    'cookie': '_ga=GA1.2.592634811.1560232436; _gid=GA1.2.2086943265.1560232436; '
              'screen_pixel_ratio=1.125; screen_resolution=1536x864; device_type=normal; '
              'OAGEO=CN%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C; OAID=2fd986ed236324f9105ca6cf43621701; '
              'PHPSESSID=ckjqjl30oifombrj9sqpk4s2u3; al=HJUsAuEBU1ZYF8IGoQC0h0bTgjr1adAgC1zi_951ceo2GRA-1560236436952708; '
              'feed_params=%7B%22filter_type%22%3A%22feed%22%2C%22filter_id%22%3A%22http%253A%252F%252Ffeeds.bbci.co.uk%252Fnews%252Fworld%252Fasia%252Fchina%252Frss.xml%22%7D;'
              ' _gat=1; window_dimensions=1707x426 ',
    'referer': 'https://www.inoreader.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}

loginedResponse = requests.post(url2, data=mydata, headers=myheader)

myresponse = requests.post(url2, data=mydata, headers=myheader)
divContent = json.loads(myresponse.content).get('xjxobj')[1]['data']

soup = BeautifulSoup(divContent, 'html.parser')


# 输出频道名称与频道的id
for temp in soup.find_all('span', class_=re.compile('tree_node tree_link normal')):
    print(temp.text)  #频道名称

    searchObj = re.search(r'link_(.*)_(.*)', temp.attrs['id'])
    print(searchObj.group(2))  #频道的id
