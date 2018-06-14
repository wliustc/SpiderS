# -*- coding: utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
import time
from scrapy.selector import *
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
class SaishiSpider(scrapy.Spider):
    name = "saishi"

    allowed_domains = ["saishi.org"]
    def __init__(self,*args,**kwargs):
        super(SaishiSpider,self).__init__(*args,**kwargs)
        self.pag = True

        start_urls = []
    def start_requests(self):
        y = 0
        url_list = 'https://race.myrunners.com/Index/index/type/0/city/0/month/0/state/0.html?pno={}'
        while self.pag:
            y+=1
            url = url_list.format(y)
            yield scrapy.Request(url,meta={'url':url})
    def parse(self, response):
        item = {}
        baoming = []
        renshu = []
        html = response.body
        htm = Selector(text=html).xpath('//*[@class="tl_i"]/p[2]/text()').extract()
        name = Selector(text=html).xpath('//*[@class="tl_t"]/text()').extract()
        if len(htm):
            htm = ''.join(htm).replace(u'\u2022', '').replace('\r', '').replace('\t', '').replace('\n', '')
            competition = re.findall(u'比赛时间：(.*?) 比赛地点：', htm)
            attend = re.findall(u'比赛地点：(.*?)报名时间', htm)
            registration_time = re.findall(u'报名时间：(.*?)人参加', htm)
            for i in registration_time:
                i = i.split(' ')
                renshu.append(i[-1])
                baoming.append(''.join(i[0:-1]))
            for i in zip(name, competition, attend, baoming, renshu):
                item['name'] = i[0]
                item['registration_time'] = i[3]
                item['place'] = i[2]
                item['competition'] = i[1]
                item['attend'] = i[4]
                item['task_time'] = start_time
                yield item
        else:
            self.pag = False





