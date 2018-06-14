# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Weatherhttp2Item(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    statics = scrapy.Field()
    temp = scrapy.Field()
    wind = scrapy.Field()
    dt = scrapy.Field()
    city=scrapy.Field()

class Weatherhttp1Item(scrapy.Item):
    city = scrapy.Field()
    date = scrapy.Field()
    bWendu = scrapy.Field()
    yWendu = scrapy.Field()
    tianqi = scrapy.Field()
    fengxiang = scrapy.Field()
    fengli = scrapy.Field()
    dt = scrapy.Field()
    id = scrapy.Field()

class Weatherhttp3Item(scrapy.Item):
    id =scrapy.Field()
    T = scrapy.Field()
    Tmax = scrapy.Field()
    Tmin = scrapy.Field()
    PP = scrapy.Field()
    dt = scrapy.Field()
    city = scrapy.Field()
    city_latitude = scrapy.Field()
    city_longitude = scrapy.Field()
    date=scrapy.Field()
    city_name =scrapy.Field()

    