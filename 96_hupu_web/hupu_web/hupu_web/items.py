# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuWebItem(scrapy.Item):
    # define the fields for your item here like:
    board_classify = scrapy.Field()
    board_name = scrapy.Field()
    browse_num = scrapy.Field()
    posts_title = scrapy.Field()
    from_mobile_reply_num = scrapy.Field()
    last_reply_date = scrapy.Field()
    post_id = scrapy.Field()


class HupuPostNumItem(scrapy.Item):
    # define the fields for your item here like:
    board_classify = scrapy.Field()
    board_name = scrapy.Field()
    post_num = scrapy.Field()
