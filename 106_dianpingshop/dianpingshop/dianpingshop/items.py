# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingshopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DianPIngAllStoreJson(scrapy.Item):
    response_content = scrapy.Field()
    meta = scrapy.Field()
    shop_response = scrapy.Field()
    