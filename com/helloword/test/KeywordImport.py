#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/20 14:56
# @Author :zhai shuai
"""
 作用
    一：导入关键字到elasticsearch
 难点
    
 注意点
"""

import codecs
from elasticsearch import Elasticsearch
from elasticsearch import helpers



if __name__ == '__main__':
    f = codecs.open("../config/keyword.txt", "r", "utf-8", buffering=True)
    typeList = []
    valueList = []
    subList = []
    while True:
        line = f.readline()
        if not line:
            valueList.append(subList)
            break
        if "---" in line:
            typeList.append(line)
            if 0 != len(subList):
                valueList.append(subList)
            subList = []
        else:
            subList.append(line)
    f.close()

    es = Elasticsearch([{'host': '39.96.23.140', 'port': 9200, 'timeout': 3600}])

    finalData = []
    for typeData in range(len(typeList)) :
        for valueData in range(len(valueList[typeData])) :
            mydict = {"type":typeList[typeData].split(" ")[0],"value":valueList[typeData][valueData].replace("\r\n","")}
            finalData.append(mydict)

    actions = [
        {
            "_index": "crawlerkeyword",
            "_type": "keywordtype",
            '_source': d
        }
        for d in finalData
    ]
    # 批量插入
    helpers.bulk(es, actions)