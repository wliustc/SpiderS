# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AjkrentingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    title = scrapy.Field()
    dt = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()


    