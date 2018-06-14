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

    name = "black_bird_01"
    allowed_domains = ["blackbirdsport.org"]
    # start_urls = ['']
    def __init__(self,*args,**kwargs):
        super(BlackBirdSpider,self).__init__(*args,**kwargs)
        self.activity_url ='http://client.blackbirdsport.com/team_getTeams?ton=zJJQDHR6RmPVQ0tK&page={}'
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
        if html.get('more') == 'NO' or html.get('status') == 'error':
            global pag
            pag =False
        
            for i in  html.get('teams'):
                item['teamId'] = i.get('teamId')
                item['teamName'] = re.sub(re_sub,'',i.get('teamName'))
                item['teamCode'] = i.get('teamCode')
                item['teamSlogon'] = re.sub(re_sub,'',i.get('teamSlogon'))
                item['active'] = i.get('teamActiveIndex')
                item['number'] = i.get('teamMemberNumber')
                item['cityId'] = i.get('cityId')
                item['cityName'] = i.get('cityName')
                # print item
                yield item
        else:
            for i in  html.get('teams'):
                item['teamId'] = i.get('teamId')
                item['teamName'] = re.sub(re_sub,'',i.get('teamName'))
                item['teamCode'] = i.get('teamCode')
                item['teamSlogon'] = re.sub(re_sub,'',i.get('teamSlogon'))
                item['active'] = i.get('teamActiveIndex')
                item['number'] = i.get('teamMemberNumber')
                item['cityId'] = i.get('cityId')
                item['cityName'] = i.get('cityName')
                yield item
    
    
    
    