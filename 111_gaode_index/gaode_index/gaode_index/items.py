# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MapGapdeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    comment_score = scrapy.Field()
    comment_text = scrapy.Field()
    comment_dt = scrapy.Field()
    write_time = scrapy.Field()
    comments_avg = scrapy.Field()
    pt_jobid = scrapy.Field()
    insert_time = scrapy.Field()

class MapStaticspeopleItem(scrapy.Item):
    city=scrapy.Field()
    spot_id = scrapy.Field()
    dt = scrapy.Field()
    val = scrapy.Field()




