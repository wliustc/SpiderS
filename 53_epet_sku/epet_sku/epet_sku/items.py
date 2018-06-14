# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EpetSkuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #一级品类（猫/狗)
    sku = scrapy.Field()
    list_0 = scrapy.Field()
    list_1 = scrapy.Field()
    list_2 = scrapy.Field()
    list_3 = scrapy.Field()
    good_name = scrapy.Field()
    goodbrand = scrapy.Field()
    eprice = scrapy.Field()
    sprice = scrapy.Field()
    countnum = scrapy.Field()
    xiaoliang = scrapy.Field()
    url = scrapy.Field()
    last_url = scrapy.Field()
    task_day = scrapy.Field()

class EpetJdSkuItem(scrapy.Item):
    sku = scrapy.Field()
    list_1 = scrapy.Field()
    list_2 = scrapy.Field()
    good_name = scrapy.Field()
    comment_num = scrapy.Field()
    price = scrapy.Field()
    dt = scrapy.Field()