# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NipponItem(scrapy.Item):
    status = scrapy.Field()
    province = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    gender = scrapy.Field()
    level = scrapy.Field()
    custom = scrapy.Field()
    time = scrapy.Field()
    id = scrapy.Field()
    company = scrapy.Field()
    getdate = scrapy.Field()