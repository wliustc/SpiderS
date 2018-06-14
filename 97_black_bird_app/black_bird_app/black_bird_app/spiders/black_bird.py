# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import json
import re
reload(sys)
sys.setdefaultencoding('utf8')
pag = True
class BlackBirdSpider(scrapy.Spider):

    name = "black_bird"
    allowed_domains = ["blackbirdsport.org"]
    # start_urls = ['']
    def __init__(self,*args,**kwargs):
        super(BlackBirdSpider,self).__init__(*args,**kwargs)
        self.activity_url ='http://client.blackbirdsport.com/activity_getGames?ton=zJJQDHR6RmPVQ0tK&page={}'
    def start_requests(self):
        pagsiz = 0
        while pag:
            url = self.activity_url.format(pagsiz)
            pagsiz+=1
            yield scrapy.Request(url)
    def parse(self, response):
        item = {}
        re_sub = u'\u2022|\xa0|\u25aa'
        html = json.loads(response.body)
        if html.get('more') == 'NO'or html.get('status') == 'error':
            global pag
            pag =False
            for i in  html.get('activitys'):
                item['activity_id'] = i.get('activityId')
                item['title'] = re.sub(re_sub,'',i.get('title'))
                item['route'] = re.sub(re_sub,'',i.get('content'))
                item['abort'] = i.get('closingEntryTime')
                item['startTime'] = i.get('startTime')
                item['endTime'] = i.get('endTime')
                item['sign_up'] = i.get('totalMemberCount')
                yield item
        else:

            for i in  html.get('activitys'):
                item['activity_id'] = i.get('activityId')
                item['title'] = re.sub(re_sub,'',i.get('title'))
                item['route'] = re.sub(re_sub,'',i.get('content'))
                item['abort'] = i.get('closingEntryTime')
                item['startTime'] = i.get('startTime')
                item['endTime'] = i.get('endTime')
                item['sign_up'] = i.get('totalMemberCount')
                yield item
    
    