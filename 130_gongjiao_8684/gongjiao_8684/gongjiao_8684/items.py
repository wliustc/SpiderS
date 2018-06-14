# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Gongjiao8684Item(scrapy.Item):
    provice = scrapy.Field()
    city = scrapy.Field()
    tran_type = scrapy.Field()
    line_name = scrapy.Field()
    title = scrapy.Field()
    transform_time = scrapy.Field()
    piaojia = scrapy.Field()
    company = scrapy.Field()
    update_time = scrapy.Field()
    descript = scrapy.Field()
    direct = scrapy.Field()
    bus_sum_num = scrapy.Field()
    port_num = scrapy.Field()
    port_name = scrapy.Field()
    dt = scrapy.Field()
