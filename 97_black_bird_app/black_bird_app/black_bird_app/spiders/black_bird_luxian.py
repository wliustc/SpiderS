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

    name = "black_bird_luxian"
    allowed_domains = ["blackbirdsport.org"]
    # start_urls = ['']
    def __init__(self,*args,**kwargs):
        super(BlackBirdSpider,self).__init__(*args,**kwargs)
        self.activity_url ='http://client.blackbirdsport.com/route_getRoutesByHot?ton=qBtZwdLoi5RnHlCV&page={}'
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
        if html.get('more') == 'NO':
            global pag
            pag =False
            for i in  html.get('routes'):
                item['nickname'] = i.get('creater').get('nickname')
                item['cityName'] = i.get('cityName')
                item['cityId'] = i.get('cityId')
                item['commentCount'] = i.get('commentCount')
                item['routeName'] = i.get('routeName')
                item['subCount'] = i.get('subCount')
                item['accountId'] = i.get('creater').get('accountId')
                yield item
        else:
            for i in  html.get('routes'):
                item['nickname'] = i.get('creater').get('nickname')
                item['cityName'] = i.get('cityName')
                item['cityId'] = i.get('cityId')
                item['commentCount'] = i.get('commentCount')
                item['routeName'] = i.get('routeName')
                item['subCount'] = i.get('subCount')
                item['accountId'] = i.get('creater').get('accountId')
                yield item