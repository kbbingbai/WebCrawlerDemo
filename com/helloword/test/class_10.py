#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/17 9:58
# @Author :zhai shuai
"""
 作用
     一：实现文章的抓取，并存入es里面

 难点

 注意点

"""
from funs import *
from elasticsearch import Elasticsearch
from elasticsearch import helpers


#es = Elasticsearch([{'host':'localhost','port':9200,'timeout':3600}])


if __name__ == "__main__":
    treeBuiltJsonDataRes = getBuiltTreeJsonData()
    isSubscribe  = analyseTreeBuiltJsonData(treeBuiltJsonDataRes)
    mylist = []

    if isSubscribe == True : ## 订阅了频道，但是有可能订阅了频道但是没有新的文章，也有可能订阅了频道有新的文章
        articles24Bool = analyseNewArticles()
        while articles24Bool :
            for temp in articles24Bool :
                mylist.append(temp)
            articles24Bool = analyseNewArticles()
        f = open("g:/softwareworkspace/" + "WebCrawler" + ".txt", "w", encoding="utf-8")
        for temp in mylist:
            f.write(str(temp)+"\n")

        # actions = [
        #     {
        #         "_index": "crawler_index",
        #         "_type": "crawler_type",
        #         '_source': d
        #     }
        #     for d in mylist
        # ]
        #
        # # 批量插入
        # helpers.bulk(es, actions)





















