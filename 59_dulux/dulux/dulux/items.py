# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuluxItem(scrapy.Item):
    province = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    level = scrapy.Field()
    time = scrapy.Field()
    company = scrapy.Field()
    getdate = scrapy.Field()
