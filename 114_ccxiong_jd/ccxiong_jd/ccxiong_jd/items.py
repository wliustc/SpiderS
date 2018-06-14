# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class B2CItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    menu = scrapy.Field()
    sub_title = scrapy.Field()
    b2c_name = scrapy.Field()
    b2c_type = scrapy.Field()
    comments = scrapy.Field()
    code = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    task_time = scrapy.Field()

    