# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdNikeDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    shop_id = scrapy.Field()
    url = scrapy.Field()
    product_code = scrapy.Field()
    dianpu_name = scrapy.Field()
    shop_name = scrapy.Field()
    dt = scrapy.Field()
    product_code1 = scrapy.Field()