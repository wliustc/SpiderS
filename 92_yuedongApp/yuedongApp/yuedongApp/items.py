# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YuedongappItem(scrapy.Item):
    # define the fields for your item here like:
    topic_content = scrapy.Field()
    topic_time = scrapy.Field()
    comment_num = scrapy.Field()
    browse_num = scrapy.Field()
    topic_id = scrapy.Field()
    like_num = scrapy.Field()
    collect_time = scrapy.Field()


class YuedongappCommentItem(scrapy.Item):
    pass


class YuedongappGameItem(scrapy.Item):
    game_info = scrapy.Field()
    person_num = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
    game_type = scrapy.Field()
    game_id = scrapy.Field()


class YuedongappCityItem(scrapy.Item):
    city_name = scrapy.Field()


class YuedongappCityActItem(scrapy.Item):
    act_id = scrapy.Field()
    act_name = scrapy.Field()
    address = scrapy.Field()
    begin_time = scrapy.Field()
    end_time = scrapy.Field()
    province_name = scrapy.Field()
    city_name = scrapy.Field()