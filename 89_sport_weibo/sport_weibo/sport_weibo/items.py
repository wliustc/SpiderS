# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoadContentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    star_name=scrapy.Field()
    weibo_id=scrapy.Field()
    url =scrapy.Field()
    created_at =scrapy.Field()
    weibo_text=scrapy.Field()
    followers_count =scrapy.Field()
    follow_count =scrapy.Field()
    statuses_count =scrapy.Field()
    urank =scrapy.Field()
    retweeted_id =scrapy.Field()
    retweeted_text =scrapy.Field()
    reposts_count =scrapy.Field()
    comments_count =scrapy.Field()
    attitudes_count =scrapy.Field()
    getdate =scrapy.Field()
    pt_jobid =scrapy.Field()

