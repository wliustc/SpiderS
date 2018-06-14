# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class JdSkuItem(scrapy.Item):
    id= scrapy.Field()
    sku = scrapy.Field()
    spu = scrapy.Field()
    shop_name = scrapy.Field()
    brand= scrapy.Field()
    price=scrapy.Field()
    dt= scrapy.Field()
    title = scrapy.Field()
    chicun = scrapy.Field()
    yanse = scrapy.Field()


class JdCommentItem(scrapy.Item):
    sku = scrapy.Field()
    shop_name = scrapy.Field()
    brand= scrapy.Field()
    dt= scrapy.Field()
    comments=scrapy.Field()
    comment_type=scrapy.Field()
    good_comment_rate=scrapy.Field()
    comment_time=scrapy.Field()
    comments_name=scrapy.Field()
    score= scrapy.Field()
    agree=scrapy.Field()
    reply=scrapy.Field()
    user_id=scrapy.Field()
    price = scrapy.Field()
    comment_id=scrapy.Field()
    chicun=scrapy.Field()
    yanse=scrapy.Field()

    