# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tongcheng58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    deal_id = scrapy.Field()
    url = scrapy.Field()
    area = scrapy.Field()
    district = scrapy.Field()
    bdistrict = scrapy.Field()
    addr = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    title = scrapy.Field()
    price= scrapy.Field()
    update_time= scrapy.Field()
    type = scrapy.Field()
    miaoshu = scrapy.Field()
    connect = scrapy.Field()
    phone = scrapy.Field()
    statics = scrapy.Field()
    img = scrapy.Field()
    city = scrapy.Field()
    dt = scrapy.Field()