# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GudongSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    game_name = scrapy.Field()
    game_people_num = scrapy.Field()
    game_time = scrapy.Field()


class GudongActSpiderItem(scrapy.Item):
    act_name = scrapy.Field()
    act_heat = scrapy.Field()
    act_starttime = scrapy.Field()
    act_endtime = scrapy.Field()


class GudongClubSpiderItem(scrapy.Item):
    club_name = scrapy.Field()
    club_rank = scrapy.Field()
    club_person_num = scrapy.Field()
    club_avg_steps = scrapy.Field()
    collect_time = scrapy.Field()
