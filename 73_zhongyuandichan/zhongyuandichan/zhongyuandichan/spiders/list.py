# -*- coding: utf-8 -*-
import scrapy
import json

class ListSpider(scrapy.Spider):
    name = "list"
    def __init__(self, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.detail = 'http://202.72.14.230/Mobile/JsonFeed/GetPosts?FromIndex={}'
        self.start_urls = []

    def start_requests(self):
        for it in xrange(0,30000,10):
            url = self.detail.format(it)
            yield scrapy.Request(url,
                callback = self.parse
                )

    def parse(self, response):
        if response.body == "":
            yield {}
        else:
            data = json.loads(response.body)
            for item in data:
                tmp = {}
                tmp['id'] = item['Id']
                tmp['data'] = json.dumps(item)
                yield tmp

    
    
    
    
    