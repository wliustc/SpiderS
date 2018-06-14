# -*- coding: utf-8 -*-
import scrapy
import json
import time

start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

class PptvSpider(scrapy.Spider):
    name = "pptv02"
    allowed_domains = ["ppty.org"]
    start_urls = ['https://tysq.suning.com/tysq-web/club/index?']
    def parse(self, response):
        html = json.loads(response.body)
        club = {}

        for x in html.get('data').get('all').get('list'):
            club['remark'] = x.get('remark')
            club['id'] = x.get('id')
            club['clubName'] = x.get('clubName')
            club['memberTotal'] = x.get('memberTotal')
            club['topicTotal'] = x.get('topicTotal')
            club['time'] = start_time
            yield club

# import time
# ltime=time.localtime(1496372833)
# timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
# print timeStr
    
    
    