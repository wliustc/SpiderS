# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoBaidliItem(scrapy.Item):
    # define the fields for your item here like:
    dataid = scrapy.Field()
    brand = scrapy.Field()
    brand_url = scrapy.Field()
    merchandise_url = scrapy.Field()
    picture_url = scrapy.Field()
    commentaries  = scrapy.Field()
    score_time  = scrapy.Field()
    comments_name = scrapy.Field()
    code = scrapy.Field()
    task_time = scrapy.Field()
    years = scrapy.Field()
    months = scrapy.Field()
    weeks = scrapy.Field()

    
    