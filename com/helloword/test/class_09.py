#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/14 13:53
# @Author :zhai shuai
"""
 作用
    一：标记一个频道下面的所有的文章为已读

 难点
    
 注意点
    一：这个功能还没有实现，实现起来还比较的麻烦或者是实现了不
    
"""
import requests

url2 = 'https://www.inoreader.com/'
cahshu = {"articles_order":0,"filter_type":"subscription","filter_id":72765251,"from_tree_menu":1,"teams":{},"update_articles":0}
mydata = {
    'xjxfun': 'read_article',
    'xjxr': '1560499238608',
    'xjxargs[]': 'Bfalse',
    'xjxargs[]': 'N1',
    'xjxargs[]': cahshu,
    'xjxargs[]': '*',
    'xjxargs[]': '*',
}
print(cahshu)
myheader={
    'cookie': '_ga=GA1.2.1514571880.1560413373; _gid=GA1.2.1374597814.1560413373; screen_pixel_ratio=1.125; screen_resolution=1536x864; device_type=normal; PHPSESSID=cpr48qvj5fqcnle6qmbot335d3; al=JgQcQc5uZ38A8feM7zCdBXYidS4gMSMiuJDFlwTLXfJtsaI-1560475129714818; OAGEO=CN%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C; OAID=0cdc577b4c9b63e1485c8538ef4cc41b; feed_params=%7B%7D; _gat=1; window_dimensions=1707x177',
    'referer': 'https://www.inoreader.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.inoreader.com',
    'referer': 'https://www.inoreader.com/'
}
myresponse = requests.post(url2,data=mydata,headers=myheader)
print(myresponse)