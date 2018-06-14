# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduThePharmacyItem(scrapy.Item):
    city = scrapy.Field()
    hospital = scrapy.Field()
    level_name = scrapy.Field()
    address = scrapy.Field()
    tel_info = scrapy.Field()
    type_info = scrapy.Field()
    province = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()

