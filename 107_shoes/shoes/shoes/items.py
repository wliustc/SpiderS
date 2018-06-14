# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoesItem(scrapy.Item):
	brand = scrapy.Field()
    title = scrapy.Field()
    prince = scrapy.Field()
    type = scrapy.Field()
    task_time = scrapy.Field()
   	pt_jobid = scrapy.Field()
    
    
    