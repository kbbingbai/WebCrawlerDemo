#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/17 9:58
# @Author :zhai shuai
"""
 作用
     一： 辅助工具类，
     二： 功能函数都是写在这个文本里面

 难点

 注意点
"""

import configparser, os, requests, json,re,time,datetime
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from operator import itemgetter


es = Elasticsearch([{'host':'localhost','port':9200,'timeout':3600}])

def readConfig(config, section):
    configDir = "/config/"
    """
        :param section:  想要获取哪个文件的配置信息
        :param section:  想要获取某个配置文件的哪部分的配置信息，如果mysql,es等配置信息
        :return: 返回该配置的字典
    """
    root_dir = os.path.dirname(os.path.abspath('.'))  # 获取当前文件所在目录的上一级目录
    cf = configparser.ConfigParser()
    cf.read(root_dir + configDir + config)  # 拼接得到requestHeader.ini文件的路径，直接使用
    if section != False:
        options = cf.items(section)  # 获取某个section名为Mysql-Database所对应的键
        return dict(options)  # 转成dict
    else:
        return cf


def getBuiltTreeJsonData():
    """
        返回 构建树的信息（订阅信息）
        注意：返回的对象实际上是json信息，里面含有构建树的信息
    """
    cf = readConfig("requestHeader.ini", False)
    headerJson = dict(cf.items("request-header"))
    mainUrl = cf.get("main-url", "main-url")
    mydata = {
        'xjxfun': 'build_tree'
    }
    myheader = headerJson
    myresponse = requests.post(mainUrl, data=mydata, headers=myheader)
    return myresponse


def getPrintArticlesJsonData():
    """
        返回 未读文章信息（订阅频道的未读文章）
        注意：返回的对象实际上是json信息，里面含有未读文章信息
    """
    cf = readConfig("requestHeader.ini", False)
    headerJson = dict(cf.items("request-header"))
    mainUrl = cf.get("main-url", "main-url")
    mydata = {
        'xjxfun': 'print_articles'
    }
    myheader = headerJson
    myresponse = requests.post(mainUrl, data=mydata, headers=myheader)
    return myresponse


def analyseTreeBuiltJsonData(builtTreeJson):
    """
        解析出订阅信息，
            （1）如果没有订阅，则json.loads(jsonStr.content).get('xjxobj')[1]['data'] 的返回值是：<span></span>
            （2）如果有订阅，则返回的数据要远大于这些字符串
        :param jsonStr: 浏览器返回的信息
        :return:
    """
    channelInfo = json.loads(builtTreeJson.content).get('xjxobj')[1]['data']
    return True if len(channelInfo) > 20 else False



def analyseReaderPanel(printArticlesHtml) :
    """
        得到文章的url信息和文章的id,把它组成一个list,组成一个[{id:文章的url},{id:文章的url},.....]的形式
        :return:
    """
    articleUrlPrefixItem = readConfig("requestHeader.ini", 'article-url-prefix')
    articleUrlPrefix = articleUrlPrefixItem.get("article-url-prefix")#文章url的前缀  比如一个文章的url是 https://www.inoreader.com/article/3a9c6e7972bfb2cf-  那articleUrlPrefix就是https://www.inoreader.com/article/

    soup = BeautifulSoup(printArticlesHtml, 'html.parser')
    readerPanels = soup.select('div[data-oid]')

    listTotal = []
    for temp in readerPanels :
        singleMap = {"id":temp['data-aid'],"url":articleUrlPrefix+temp['data-oid']}
        listTotal.append(singleMap)
    return listTotal


def analyseArticlePublicDate(soupObj) :
    """
        解析文章发表时间  日期有两种格式，
            一个是   %a %b %d, %Y %H:%M   接收日期: Thu Jun 13, 2019 16:32 发布日期: Sun Jun 02, 2019 16:12
            一个是：%H:%M                 接收日期: 09:17 发布日期: 09:09
        :param soupObj:
        :return:
    """
    articleTime = soupObj.find("div", attrs={"class": "header_date"}).attrs['title']
    searchObj = articleTime.split(": ")
    publicDate = searchObj[2]
    if (re.search(r'^\d{2}:\d{2}', publicDate)):
        strTime = time.strftime("%Y-%m-%d ") + publicDate
    else:
        timeStruct = time.strptime(publicDate, "%a %b %d, %Y %H:%M")
        strTime = time.strftime("%Y-%m-%d %H:%M", timeStruct)

    return strTime



def analyseArticlesLoaded(articlesLoadedHtml) :
    """
        用于解析文章,它的解析
        得到文章的url信息和文章的id, 把它组成一个list, 组成一个[{字段: 字段值.....}, {字段: 字段值.....},.....]
        :param articlesLoadedHtml:
        :return:
    """
    listTotal = []
    articleContent = articlesLoadedHtml[0]
    insertTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for temp in articleContent.items():  # 转成元组, temp的组成是这样的，('20563836790', 'elementHtml')
        soup = BeautifulSoup(temp[1])

        #文章的id
        id = temp[0]
        title = soup.find("a", attrs={"id": "article_title_link_" + temp[0]}).text
        publicDate = analyseArticlePublicDate(soup)


        content = soup.find("div", attrs={"class": "article_content"}).text
        singleMap = {"id": id, "title": title, "publicDate": publicDate, "content": content,"insertDate": insertTime,"analyseFlag":"true"}

        listTotal.append(singleMap)

    return listTotal


def unsubscribeArticles(readerPanelListSorted) :
    """
        取消文章的订阅
        :param readerPanelListSorted: 传入的list，格式是  [{id:文章的url},{id:文章的url},.....]
        :return:
    """
    cf = readConfig("requestHeader.ini", False)

    mainUrl = cf.get("main-url","main-url")
    url = mainUrl

    headerJson = dict(cf.items("request-header"))

    articleIds = []
    for temp in readerPanelListSorted :
        articleIds.append(temp["id"])

    articleIds = "[\"" + "\",\"".join(articleIds) + "\"]"
    mydata = {
        'xjxfun': 'read_article',
        'xjxargs[]': articleIds
    }

    requests.post(url, data=mydata, headers=headerJson)


def getKeyWord():
    """
        得到匹配的关键字并返回这样的形式,{"CommonKW":{"adware","Worm"...}....}
    """
    res = es.search(index="crawlerkeyword", body={'query': {'match_all': {}}},params={"size":500})
    newDict = {}
    for temp in res['hits']['hits']:
        typeValue = temp['_source']['type']
        valueValue = temp['_source']['value']
        if typeValue in newDict:
            newDict[typeValue].append(valueValue)
        else:
            subList = []
            subList.append(valueValue)
            newDict[typeValue]=subList
    return newDict



def articleContentRegularMatch(articlesLoadedListSorted):
    """
    对文章的内容进行正则的匹配，如果一篇文章的content，匹配了相关的关键字，就打相关的标签
    :param articlesLoadedListSorted:
    :return:
    """
    keyWordMap = getKeyWord()

    for singleArticle in articlesLoadedListSorted:
        #取出文章的content
        articleContent = singleArticle["content"]
        tags = []
        for keyWord in keyWordMap:
            singleGroupListReg = "|".join(keyWordMap[keyWord])
            isMatch = re.findall(singleGroupListReg,articleContent) #是否匹配到
            if isMatch: #表示匹配了上
                tags.append(keyWord)
        singleArticle.update({"tags":"|".join(tags)})

def analyseNewArticles():
    """
        查看是否有新的文章,如果有新文章就返回Ture，如果没有新的文章就返回False
        :param printArticleJson:
        :return:
    """
    printArticleInfo = getPrintArticlesJsonData() #得到全部PrintArticles信息

    printArticleInfo = json.loads(printArticleInfo.content).get('xjxobj')

    readerPaneHtml = ''                           #得到{cmd: "as", id: "reader_pane", prop: "innerHTML",…} 这一项的信息
    articlesLoadedHtml = ''                       #得到{cmd: "jc", func: "articles_loaded",…} 这一项的信息
    for tempNum in range(len(printArticleInfo)) :

        if articlesLoadedHtml != '' and readerPaneHtml != '' :
            break

        if 'func' in printArticleInfo[tempNum] :
            if 'check_older_articles_hint' == printArticleInfo[tempNum]['func'] :  #如果有这个方法名，则表明所有的频道下面没有最新的文章
                return False
            if 'articles_loaded' == printArticleInfo[tempNum]['func'] :
                articlesLoadedHtml = printArticleInfo[tempNum]['data']

        if "id" in printArticleInfo[tempNum] :
            if 'as' == printArticleInfo[tempNum]['cmd'] and 'reader_pane' == printArticleInfo[tempNum]['id'] :
                readerPaneHtml = printArticleInfo[tempNum]['data']


    readerPanelList = analyseReaderPanel(readerPaneHtml)
    articlesLoadedList = analyseArticlesLoaded(articlesLoadedHtml)

    readerPanelListSorted = sorted(readerPanelList, key=itemgetter('id'), reverse=True)
    articlesLoadedListSorted = sorted(articlesLoadedList, key=itemgetter('id'), reverse=True)

    for tempNum in range(len(articlesLoadedListSorted)) : #把文章的url加入到articlesLoadedListSorted里面去
       articlesLoadedListSorted[tempNum].update({"url":readerPanelListSorted[tempNum]['url'],"analyseDate":""})



    #进行正则的匹配,与关键字进行撞击
    #articleContentRegularMatch(articlesLoadedListSorted)

    #取消文章的订阅
    unsubscribeArticles(articlesLoadedListSorted)

    return articlesLoadedListSorted



