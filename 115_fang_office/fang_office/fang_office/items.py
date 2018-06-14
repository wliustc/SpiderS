# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangOfficeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    building_level = scrapy.Field()
    classes = scrapy.Field()
    floors = scrapy.Field()
    construction_ratio = scrapy.Field()
    floor_space = scrapy.Field()
    frm = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    biz_area = scrapy.Field()
    src_uid = scrapy.Field()
    building_name = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    alias = scrapy.Field()
    address = scrapy.Field()
    sell_price = scrapy.Field()
    rent_price = scrapy.Field()
    built_dt = scrapy.Field()
    developer = scrapy.Field()
    property_fee = scrapy.Field()
    building_area = scrapy.Field()
    parking_space = scrapy.Field()
    greening_rate = scrapy.Field()
    volume_rate = scrapy.Field()
    fang_link = scrapy.Field()
