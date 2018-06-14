# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_list = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    sale_num = scrapy.Field()
    comment_num = scrapy.Field()
    comment_url = scrapy.Field()
    detail_url = scrapy.Field()
    # 名称，单价，总销量，评价数，评价内容
