----------------------------几个API------------------------------------------------------
#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time   :2019/6/12 9:38
# @Author :zhai shuai
# 作用：
import requests,json
url="https://www.inoreader.com/login"
params={
    "username":"1617079905@qq.com",
    "password":"1617079905",
    "warp_action":"login",
    "remember_me":"on"
}

loginResponse = requests.get(url,data=params)
print(loginResponse.cookies.)
loginResponse.cookies.get_dict()

----------------------class_07生成的数据格式--------------------------------------------

# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

www.inoreader.com	FALSE	/	FALSE		PHPSESSID	vhhu4v92mkrmo9posdpr8oski3
www.inoreader.com	FALSE	/	FALSE	1563154875	al	gyhpggru67_OrZhIaMB10_FQJg9IozsTylyFonuzGiJIWQI-1560476474352316


----------------------python爬虫可以参考的几个网页--------------------------------------------

https://blog.csdn.net/weixin_42134789/article/details/82904741

https://blog.csdn.net/a583179/article/details/78904645

https://blog.csdn.net/hpulfc/article/details/80084398

https://blog.csdn.net/haeasringnar/article/details/82558729

-------------------------------------------analyseReaderPanel函数需要解析的文本-----------------------------------------------

<div id="article_20563636304" class="ar article_unreaded article_subscribed ar_showed article_tile radius article_expanded article_no_thumbnail" data-topiccount="1" data-read="0" data-sunk="0" data-aid="20563636304" data-oid="3a9c6e7972bbcfaf" data-date_usec="1560818945800691" data-date_rel="1560818946" data-suid="72817290" data-fid="110057" data-fav="0" data-liked="0" data-score="" data-brd="0" data-comments="" data-tags="null" data-blanked="0" data-pocket="-1" data-evernote="-1" data-onenote="-1" data-dropbox="-1" data-gdrive="-1" data-ar="0" data-ft="RSS" data-d="0" data-tm="null">
   <div class="article_tile_content_wraper no_pic" dir="ltr">
    <div id="header_date_tile_20563636304" class="article_tile_header_date" title="接收日期: 08:49
发布日期: 08:25">
     17m
    </div>
    <div class="article_tile_title" dir="ltr">
     <a class="boldlink" href="https://cn.reuters.com/article/eu-tradeprotectionism-0617-mon-idCNKCS1TJ01C?feedType=RSS&amp;feedName=CNIntlBizNews" onmousedown="return toggle_articleview('20563636304',false,event,{dont_scroll:true})" id="at_20563636304">中美贸易争端将去年全球贸易壁垒水平推至纪录新高--欧盟报告</a>
    </div>
    <div class="article_tile_content" dir="ltr" id="article_short_contents_20563636304">
      路透布鲁塞尔6月17日 - 欧盟执委会周一发布的一份报告显示，由于旨在限制中美贸易的新壁垒，去年全球贸易保护主义达到创纪录的高点。
    </div>
   </div>
   <div class="article_tile_current_stripe">
    &nbsp;
   </div>
   <div class="article_tile_footer">
    <div class="article_tile_footer_left_buttons">
     <div class="article_tile_footer_feed_title" dir="ltr">
      <a class="ajaxed" href="/feed/http%3A%2F%2Fcn.reuters.com%2FrssFeed%2FCNIntlBizNews" title="前往订阅源">路透: 国际财经</a>
     </div>
    </div>
    <div class="article_tile_footer_right_buttons">
     <span class="article_footer_buttons article_footer_buttons_fav"><a href="javascript:void(0)" title="添加星标 (快捷键: F)" onclick="set_fav('20563636304');l('Article footer','Star');"><span class="star_img icon16 icon-star_empty "></span></a></span>
     <span class="article_footer_buttons"><a href="javascript:void(0)" onclick="mark_read('20563636304');l('Article header','Mark read');"><span class="icon16 icon-radio_checked_big" id="unread_img_20563636304" title="标记为已读"></span></a></span>
     <span class="article_footer_buttons"><a id="aurl_20563636304" target="_blank" rel="noopener" href="https://cn.reuters.com/article/eu-tradeprotectionism-0617-mon-idCNKCS1TJ01C?feedType=RSS&amp;feedName=CNIntlBizNews" onmouseup="arlink_click(20563636304,event);l('Article header','Open in new tab');"><span class="icon16 icon-new_tab" title="在新标签打开"></span></a></span>
     <span class="article_footer_buttons"><a id="amot_20563636304" href="javascript:void(0)" onmouseup="show_article_menu(20563636304,'#amot_20563636304');l('Article header','Article menu');"><span class="icon16 icon-more_horizontal_dots"></span></a></span>
    </div>
   </div>
  </div>


  --------------------------------python读取配置文件------------------------------------------
  import configparser

    cf = configparser.ConfigParser()
    cf.read("E:\Crawler\config.ini")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块

    secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，
                            每个section由[]包裹，即[section])，并以列表的形式返回
    print(secs)

    options = cf.options("Mysql-Database")  # 获取某个section名为Mysql-Database所对应的键
    print(options)

    items = cf.items("Mysql-Database")  # 获取section名为Mysql-Database所对应的全部键值对
    print(items)

    host = cf.get("Mysql-Database", "host")  # 获取[Mysql-Database]中host对应的值
    print(host)
    ---------------------------------------
    import pymysql
#import datetime
#day = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#参数值插入时间
db = pymysql.connect(host='服务器IP', user='账号', passwd='密码', port=端口号)
cur = db.cursor()
cur.execute('use 数据库')
#批量创建测试账号
usersvalues=[]
for i in range(1,5):
  usersvalues.append(('参数值1'+str(i),'参数值2'))
#批量插入数据
cur.executemany('insert into 表名(参数名1,参数名2) value(%s,%s)', usersvalues)
#修改数据（查询和删除数据同）
cur.execute("update 表名 set 参数名='参数更新值' where 条件名='条件值'")