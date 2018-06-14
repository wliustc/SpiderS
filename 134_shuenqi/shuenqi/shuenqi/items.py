# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShuenqiItem(scrapy.Item):
    type_name = scrapy.Field()
    min_type = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    addr = scrapy.Field()
    tel = scrapy.Field()
    contact = scrapy.Field()
    cellphone = scrapy.Field()
    mail = scrapy.Field()
    facsimile = scrapy.Field()
    license = scrapy.Field()
    legal_person = scrapy.Field()
    operate = scrapy.Field()
    founding_time = scrapy.Field()
    capital = scrapy.Field()
    name = scrapy.Field()
    sp_url = scrapy.Field()
    state = scrapy.Field()
    set_up = scrapy.Field()
    certificate = scrapy.Field()
    audit = scrapy.Field()
    min_type_href = scrapy.Field()
    url = scrapy.Field()
    district = scrapy.Field()
    dd = scrapy.Field()

    
    