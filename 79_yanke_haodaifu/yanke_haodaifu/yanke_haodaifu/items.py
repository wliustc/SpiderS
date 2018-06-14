# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class YankeaierItem(scrapy.Item):
    name=scrapy.Field()
    hospital_detial=scrapy.Field()
    zhicheng=scrapy.Field()
    professional=scrapy.Field()
    summary=scrapy.Field()
    hospital=scrapy.Field()
    url=scrapy.Field()

class YankeguahaoItem(scrapy.Item):
    name=scrapy.Field()
    technical_title=scrapy.Field()
    specil_skill=scrapy.Field()
    mark_count=scrapy.Field()
    comment_grade=scrapy.Field()
    bespeak=scrapy.Field()
    action_count=scrapy.Field()
    comment_count = scrapy.Field()
    summary = scrapy.Field()
    hospital_info = scrapy.Field()

class YankehaodaifuItem(scrapy.Item):
    province_name=scrapy.Field()
    hospital_name=scrapy.Field()
    room=scrapy.Field()
    name=scrapy.Field()
    summary=scrapy.Field()
    comment_grade=scrapy.Field()
    technical_title=scrapy.Field()
    proffession=scrapy.Field()


class YankehuaxiaItem(scrapy.Item):
    name=scrapy.Field()
    hospital_name=scrapy.Field()
    zhicheng=scrapy.Field()
    professional=scrapy.Field()
    summary=scrapy.Field()
    url=scrapy.Field()


