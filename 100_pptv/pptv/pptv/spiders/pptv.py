# -*- coding: utf-8 -*-
import scrapy
import json
import time
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
class PptvSpider(scrapy.Spider):
    name = "pptv"
    allowed_domains = ["ppty.org"]
    start_urls = ['https://tysq.suning.com/tysq-web/club/index?']
    def parse(self, response):
        html = json.loads(response.body)
        item = {}
        club ={}
        for i in html.get('data').get('hot').get('list'):
            item['comments'] = i.get('remarkTotal')
            item['title'] = i.get('title')
            item['nickname'] = i.get('userInfo').get('nickname')
            item['clubName'] = i.get('clubName')
            item['time'] = start_time
            yield item

# import time
# ltime=time.localtime(1496372833)
# timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
# print timeStr
    