# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()
    src_uid = scrapy.Field()
    shop_name = scrapy.Field()
    base_info = scrapy.Field()
    around_info = scrapy.Field()
    traffic_info = scrapy.Field()
