# -*- coding: utf-8 -*-
import scrapy
import json
import time

start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
class PptvSpider(scrapy.Spider):
    name = "pptv_02"
    start_urls = []

    def __init__(self,*args,**kwargs):
        super(PptvSpider,self).__init__(*args,**kwargs)
        self.url = 'https://tysq.suning.com/tysq-web/club/index?'
    # allowed_domains = ["ppty.org"]
    def start_requests(self):
        yield scrapy.Request(url=self.url)
    def parse(self, response):
        html = json.loads(response.body)
        itme = {}
        for x in html.get('data').get('all').get('list'):
            itme['remark'] = x.get('remark')
            itme['id'] = x.get('id')
            itme['clubName'] = x.get('clubName')
            itme['memberTotal'] = x.get('memberTotal')
            itme['topicTotal'] = x.get('topicTotal')
            itme['time'] = start_time
            yield itme

    
    