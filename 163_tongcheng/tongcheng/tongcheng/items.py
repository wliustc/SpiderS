# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TongchengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    img_src = scrapy.Field()
    publish_time = scrapy.Field()
    house_description = scrapy.Field()
    near_description = scrapy.Field()
    money = scrapy.Field()
    house_area = scrapy.Field()
    house_type = scrapy.Field()
    manager_form = scrapy.Field()
    country = scrapy.Field()
    area = scrapy.Field()
    addr = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()
