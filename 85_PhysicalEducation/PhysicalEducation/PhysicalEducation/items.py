# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhysicaleducationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    response_content = scrapy.Field()
    
class AiRuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    response_content = scrapy.Field()
    category_child = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    
class KuChuanItem(scrapy.Item):
    response_content = scrapy.Field()
    
class AiRuiDetailItem(scrapy.Item):
    Appid =scrapy.Field()
    RootType = scrapy.Field()
    TypeName = scrapy.Field()
    Proportion = scrapy.Field()
    task_time = scrapy.Field()
    TimeName = scrapy.Field()
    
    