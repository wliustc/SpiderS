# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiJuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    pass

class TiJuzinew_compitem(scrapy.Item):
    company_id = scrapy.Field()
    brand = scrapy.Field()
    shot_descript = scrapy.Field()
    category = scrapy.Field()
    infor = scrapy.Field()
    company_full_name = scrapy.Field()
    found_time = scrapy.Field()
    guimo = scrapy.Field()
    tag = scrapy.Field()
    investtime = scrapy.Field()
    round = scrapy.Field()
    money=scrapy.Field()
    investors=scrapy.Field()
    dt = scrapy.Field()
    start_people = scrapy.Field()

class TiJuzinew_inverstfirm(scrapy.Item):
   investfirmid=scrapy.Field()
   firm_name=scrapy.Field()
   tag=scrapy.Field()
   firm_xiangxi=scrapy.Field()
   firm_scale=scrapy.Field()
   singel_scale=scrapy.Field()
   invest_file=scrapy.Field()
   invest_lunci=scrapy.Field()
   invest_filed=scrapy.Field()
   invent_manage=scrapy.Field()
   dt=scrapy.Field()

class TiJuzinew_inversttable(scrapy.Item):
   comp_id=scrapy.Field()
   type=scrapy.Field()
   x=scrapy.Field()
   y=scrapy.Field()
   dt=scrapy.Field()

class TiJuzi_newsItem(scrapy.Item):
    pub_time=scrapy.Field() #  发布时间
    org=scrapy.Field() #		  机构
    news_src=scrapy.Field() #  新闻来源
    title=scrapy.Field() #     标题
    content=scrapy.Field() #   新闻内容
    author=scrapy.Field() #	  作者
    read_num=scrapy.Field() #  阅读量
    trans_num=scrapy.Field() #  转发量
    tags=scrapy.Field() #   文章标签
    cm_frm=scrapy.Field() #  哪里有
    insert_time=scrapy.Field() # 爬取时间


class TiJuzi_newsfull(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    new_date = scrapy.Field()
    source = scrapy.Field()
    context = scrapy.Field()
    dt = scrapy.Field()
    url = scrapy.Field()
