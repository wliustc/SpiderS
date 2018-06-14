# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoosDirectHireItem(scrapy.Item):
    live_name = scrapy.Field()
    theme = scrapy.Field()
    reply = scrapy.Field()
    new = scrapy.Field()
    time = scrapy.Field()
   # pt_jobid = scrapy.Field()

    
    
    
    
    