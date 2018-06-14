# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduJsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
   	addr = scrapy.Field()
    data_id = scrapy.Field()
    legalpersonid = scrapy.Field()
    province  = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    catalog = scrapy.Field()
    poi_desc = scrapy.Field()
    baidu_addr= scrapy.Field()
    mc_lng = scrapy.Field()
    mc_lat = scrapy.Field()
    baidu_lat = scrapy.Field()
    baidu_lng = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    
    
    pt_jobid = scrapy.Field()
    

    
    
    