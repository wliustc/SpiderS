# -*- coding: utf-8 -*-
import scrapy
import json
from PhysicalEducation.items import PhysicaleducationItem

class SportsSpider(scrapy.Spider):
    name = "sports"
    allowed_domains = ["sports.qq.com"]
    start_urls = ['http://shequweb.sports.qq.com/module/list']

    def parse(self, response):
        item = PhysicaleducationItem()
        item['response_content'] = response.body
        yield item
        # print response.body


    
    
    