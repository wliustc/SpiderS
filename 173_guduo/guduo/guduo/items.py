# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuduoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    datetimes = scrapy.Field()
    platformImgUrl = scrapy.Field()
    today_play_count = scrapy.Field()
    incType = scrapy.Field()
    directors = scrapy.Field()
    douban_score = scrapy.Field()
    episode = scrapy.Field()
    coverImgUrl = scrapy.Field()
    duration = scrapy.Field()
    actors = scrapy.Field()
    showId = scrapy.Field()
    total_comment_count = scrapy.Field()
    url = scrapy.Field()
    market_share_ratio = scrapy.Field()
    nowEpisode = scrapy.Field()
    release_date = scrapy.Field()
    baidu_exponent = scrapy.Field()
    dianshi_names = scrapy.Field()
    increaseCount = scrapy.Field()
    days = scrapy.Field()
    platformName = scrapy.Field()
    rise = scrapy.Field()
    ordinal = scrapy.Field()
    riseAbs = scrapy.Field()
    dt = scrapy.Field()

    
    