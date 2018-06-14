# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    city_name = scrapy.Field()
    province = scrapy.Field()
    naem = scrapy.Field()
    href = scrapy.Field()

