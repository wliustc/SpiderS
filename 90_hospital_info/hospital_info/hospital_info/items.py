# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalInfoItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    city = scrapy.Field()
    level_name = scrapy.Field()
    hospital = scrapy.Field()
    address = scrapy.Field()
    tel_info = scrapy.Field()
    type = scrapy.Field()

class HospitalCityLevelItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    level_name = scrapy.Field()
    city_level_url = scrapy.Field()
    