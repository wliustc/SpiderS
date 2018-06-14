# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    addr = scrapy.Field()
    hotel_id = scrapy.Field()
    star = scrapy.Field()
    cityId = scrapy.Field()
    location = scrapy.Field()
    tels = scrapy.Field()
    city_code = scrapy.Field()
    city_name = scrapy.Field()
    type_query = scrapy.Field()

    