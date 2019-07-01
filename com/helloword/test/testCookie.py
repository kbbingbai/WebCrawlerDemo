#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/26 9:12
# @Author :zhai shuai


from urllib.request import *
import http.cookiejar, urllib.parse


cookie_jar = http.cookiejar.MozillaCookieJar('a.txt')
# 创建HTTPCookieProcessor对象
cookie_processor = HTTPCookieProcessor(cookie_jar)
# 创建OpenerDirector对象
opener = build_opener(cookie_processor)

# 定义模拟Chrome浏览器的user_agent
user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
# 定义请求头
headers = {'User-Agent':user_agent, 'Connection':'keep-alive'}

#-------------下面代码发送登录的POST请求----------------
# 定义登录系统的请求参数
params={
    "username":"1617079905@qq.com",
    "password":"1617079905",
    "warp_action":"login",
    "remember_me":"on"
}
postdata = urllib.parse.urlencode(params).encode()
# 创建向登录页面发送POST请求的Request
request = Request('https://www.inoreader.com/login',
    data = postdata, headers = headers)
# 使用OpenerDirector发送POST请求
response = opener.open(request)

# 将cookie信息写入磁盘文件
cookie_jar.save(ignore_discard=True, ignore_expires=True)  # ①

# #-------------下面代码发送访问被保护资源的GET请求----------------
# # 创建向"受保护页面"发送GET请求的Request
# request = Request('http://localhost:8888/test/secret.jsp',
#     headers=headers)
# response = opener.open(request)
# print(response.read().decode())




######################下面的程序可以取出cookie的信息#####################
cookie_jar = http.cookiejar.MozillaCookieJar("a.txt")
cookie_jar.load("a.txt",ignore_discard=True,ignore_expires=True)
for item in cookie_jar:
    print(item.name)
    print(item.value)