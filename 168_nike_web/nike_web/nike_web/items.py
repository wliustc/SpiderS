# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NikeWebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    price = scrapy.Field()
    employee_price = scrapy.Field()
    color = scrapy.Field()
    kuanhao = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    size = scrapy.Field()
    dt = scrapy.Field()
    