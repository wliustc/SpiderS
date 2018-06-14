# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BailingniaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    addr = scrapy.Field()
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    tel = scrapy.Field()
    cityname = scrapy.Field()
    field_id = scrapy.Field()
    task_time = scrapy.Field()

class BailingniaoOrderFieldItem(scrapy.Item):
    response_content = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    category = scrapy.Field()
    addr = scrapy.Field()
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    tel = scrapy.Field()
    cityname = scrapy.Field()
    field_id = scrapy.Field()
    task_time = scrapy.Field()

    
    
    
    