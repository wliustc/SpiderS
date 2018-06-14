# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiangpinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_id = scrapy.Field()
    gaode_id = scrapy.Field()
