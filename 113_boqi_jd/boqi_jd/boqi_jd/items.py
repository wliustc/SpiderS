# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoqiJdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category1_name = scrapy.Field()
    category2_name = scrapy.Field()
    goods_id = scrapy.Field()
    comment_num = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    collect_time = scrapy.Field()
