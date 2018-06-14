# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import re
import os
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
start_times = datetime.date.today()
oneday = datetime.timedelta(days=3)
start = start_times-oneday

def time_s(times):
    times = int(times)
    ltime=time.localtime(times)
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return  timeStr
print time_s(1496626370)
class PptvSpider(scrapy.Spider):
    name = "pptv01"
    allowed_domains = ["ppty.org"]
    def __init__(self,*args,**kwargs):
        super(PptvSpider,self).__init__(*args,**kwargs)
        self.hot = 'http://api.sports.pptv.com/mobile/v1/home/menus?&appid=PPTVSPORTSNO1&appplt=aph&appver=4.0.8&ppi=AgACAAAAAQAATkoAAAABAAAAAFk1gACFC4ERq0TeCfBuvOJWaYELbixabY4mf8lhSzVZJgepYcZsNx4Ur_etb2LKcR4qAuubL5bt1u27JCI4VOtyu_p-'
        self.url = 'http://api.sports.pptv.com/mobile/v1/page/feeds?appid=PPTVSPORTSNO1&start={}&appplt=aph&ppi=AgACAAAAAQAATkoAAAABAAAAAFkwOgBm8nzH00b2gS8y-XUan9OMqjRJnvDgHtwIMs99TvMG4jKDeyuqfFFIvBLSRpLbH-VxlKlbtg4NqBH1MfyBuNB3&page_id={id}&appver=4.0.8'
        self.video = 'http://apicdn.sc.pptv.com/sc/v3/pplive/ref/vod_{}/feed/list?appplt=web&action=1'
        self.post = 'http://apicdn.sc.pptv.com/sc/v3/pplive/ref/sportsarticle_{}/topfeed/list?appplt=web&action=1'
    def start_requests(self):
            url = self.hot
            yield scrapy.Request(url,dont_filter=True,callback=self.parse)
    def parse(self, response):
        html = json.loads((response.body))
        for i in html.get('data'):
            page_id = i.get('page_id')
            url = self.url.format('',id=page_id)
            yield scrapy.Request(url,dont_filter=True,callback=self.parse2,meta={'id':page_id})
    def parse2(self, response):
        html = json.loads(response.body)
        if len(html.get('data')) == 0:
            pass
        else:
            start = html.get('data')[-1].get('start')
            id_s = response.meta['id']
            urls = self.url.format(start,id=id_s)
            yield scrapy.Request(urls, dont_filter=True, callback=self.parse2, meta={'start': start,'id':id_s})
            for i in html.get('data'):
                if i.get('type') == "banner1":
                    title = i.get('banner1').get('title')
                    uid = i.get('banner1').get('action').get('link').split('=')[-1]
                    time_sk = i.get('banner1').get('create_time')
                    url = self.post.format(uid)
                    yield scrapy.Request(url,meta={'title':title,'time_sk':time_sk,'url':url},dont_filter=True,callback=self.parse1)

                if i.get('type') == "imagetext":
                    title = i.get('imagetext').get('title')
                    uid = i.get('imagetext').get('action').get('link').split('=')[-1]
                    time_sk = i.get('imagetext').get('create_time')
                    url = self.post.format(uid)
                    yield scrapy.Request(url, meta={'title': title, 'time_sk': time_sk, 'url': url},
                                           dont_filter=True, callback=self.parse1)

                if i.get('type') == "video":
                    title = i.get('video').get('title')
                    uid = i.get('video').get('action').get('link').split('=')[-1]
                    time_sk = i.get('video').get('create_time')
                    url = self.video.format(uid)
                    yield scrapy.Request(url, meta={'title': title, 'time_sk': time_sk, 'url': url},
                                             dont_filter=True, callback=self.parse1)

    def parse1(self,response):
        time ={}
        create_time = time_s(response.meta['time_sk'])
        html = json.loads(response.body)
        time['title'] = response.meta['title']
        time['create_time'] = create_time
        time['total'] = html.get('data').get('total')
        time['task_time'] = start_time
        time['comments_url'] = response.meta['url']
        yield time


    