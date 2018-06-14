# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohongshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cate1_name = scrapy.Field()
    cate2_name = scrapy.Field()
    cate3_name = scrapy.Field()
    discount_price = scrapy.Field()
    goods_id = scrapy.Field()
    origin_price = scrapy.Field()
    title = scrapy.Field()
    shop_name = scrapy.Field()
    member_price = scrapy.Field()
    brand_id = scrapy.Field()
    shortName = scrapy.Field()
    brand = scrapy.Field()
    attr_list = scrapy.Field()


class XiaohongshuComment(scrapy.Item):
    pass


class XhsFansItem(scrapy.Item):
    user_id = scrapy.Field()
    cate = scrapy.Field()
    fans_num = scrapy.Field()
    collect = scrapy.Field()
    name = scrapy.Field()
    note_num = scrapy.Field()
    brief = scrapy.Field()