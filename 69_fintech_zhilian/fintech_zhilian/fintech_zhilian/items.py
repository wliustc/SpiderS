# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianCampanyItem(scrapy.Item):  
    company=scrapy.Field()
    Job_title=scrapy.Field()
    Job_type=scrapy.Field()
    Job_describe=scrapy.Field()
    keyword=scrapy.Field()
    number=scrapy.Field()
    recruiting_city=scrapy.Field()
    payment=scrapy.Field()
    learn=scrapy.Field()
    experience=scrapy.Field()
    source=scrapy.Field()
    release_time=scrapy.Field()
    task_time=scrapy.Field()

    
    
    
    
    
    