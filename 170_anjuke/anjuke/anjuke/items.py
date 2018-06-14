# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    addr = scrapy.Field()
    sum_price = scrapy.Field()
    unit_price = scrapy.Field()
    dt = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    base_url = scrapy.Field()

class Renting(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    addr = scrapy.Field()
    unit_price = scrapy.Field()
    dt = scrapy.Field()
