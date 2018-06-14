# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewrankItem(scrapy.Item):
    name = scrapy.Field()
    paiming = scrapy.Field()
    account = scrapy.Field()
    fabu = scrapy.Field()
    tread_num = scrapy.Field()
    toutiao = scrapy.Field()
    average = scrapy.Field()
    max = scrapy.Field()
    dianzan = scrapy.Field()
    rank_mark = scrapy.Field()
    month_top_times = scrapy.Field()
    start_time=scrapy.Field()
    end_time=scrapy.Field()
    group = scrapy.Field()
    rank = scrapy.Field()
