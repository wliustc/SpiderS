# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongqiudiItem(scrapy.Item):
    # define the fields for your item here like:
    group_id = scrapy.Field()
    group_name = scrapy.Field()
    topic_total = scrapy.Field()
    join_user_total = scrapy.Field()
    # group_created_date = scrapy.Field()
    browse_num = scrapy.Field()
    collect_time = scrapy.Field()

    