# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingdoctorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shopid = scrapy.Field()
    skills = scrapy.Field()
    doctor_id = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    isCertified = scrapy.Field()
    isVoted = scrapy.Field()
    workYear = scrapy.Field()
    avatar = scrapy.Field()
    voteCount = scrapy.Field()
    briefDesc = scrapy.Field()
    shopname = scrapy.Field()
