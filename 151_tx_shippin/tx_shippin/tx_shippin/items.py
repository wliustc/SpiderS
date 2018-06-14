# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TxShipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    item_id = scrapy.Field()
    type = scrapy.Field()
    title= scrapy.Field()
    score = scrapy.Field()
    count = scrapy.Field()
    floor = scrapy.Field()
    dubo = scrapy.Field()
    zizhi = scrapy.Field()
    year = scrapy.Field()
    dt = scrapy.Field()
    pass
