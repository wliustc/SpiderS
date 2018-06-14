# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Somefangchan_yingshangItem(scrapy.Item):
    deal_id = scrapy.Field()
    provice = scrapy.Field()
    dt = scrapy.Field()
    platform = scrapy.Field()
    title = scrapy.Field()
    statics = scrapy.Field()
    open_time = scrapy.Field()
    type = scrapy.Field()
    mianji = scrapy.Field()
    need = scrapy.Field()
    city=scrapy.Field()
    address=scrapy.Field()
    distract=scrapy.Field()
    developer=scrapy.Field()
    connect_name=scrapy.Field()
    connect_duty=scrapy.Field()
    connect_phone=scrapy.Field()
    connect_mphone=scrapy.Field()
    connect_email=scrapy.Field()
    price=scrapy.Field()

    