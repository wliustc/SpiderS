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
        self.url = 'http://api.sports.pptv.com/mobile/v1/page/feeds?appid=PPTVSPORTSNO1&start={}&appplt=aph&ppi=AgACAAAAAQAATkoAAAABAAAAAFkwOgBm8nzH00b2gS8y-XUan9OMqjRJnvDgHtwIMs99TvMG4jKDeyuqfFFIvBLSRpLbH-VxlKlbtg4NqBH1MfyBuNB3&page_id={id}&appver=4.0.8'
        self.video = 'http://apicdn.sc.pptv.com/sc/v3/pplive/ref/vod_{}/feed/list?appplt=web&action=1'
        self.post = 'http://apicdn.sc.pptv.com/sc/v3/pplive/ref/sportsarticle_{}/topfeed/list?appplt=web&action=1'
    def start_requests(self):
        id_list = ['25','35','30','21','23','24','38','26','31','29','28','27','32','34','36','39','22']
        id_list = ['25','22']
        for i in id_list:
            url = self.url.format('',id=i)
            yield scrapy.Request(url,dont_filter=True,callback=self.parse,meta={'id':i})
    def parse(self, response):
        html = json.loads(response.body)
        if len(html.get('data')) == 0:
            pass
        else:
            start = html.get('data')[-1].get('start')
            id_s = response.meta['id']
            urls = self.url.format(start,id=id_s)
            yield scrapy.Request(urls, dont_filter=True, callback=self.parse, meta={'start': start,'id':id_s})
            for i in html.get('data'):
                if i.get('type') == "banner1":
                    title = i.get('banner1').get('title')
                    uid = i.get('banner1').get('action').get('link').split('=')[-1]
                    time_sk = i.get('banner1').get('create_time')
                    url = self.post.format(uid)
                    create_time = i.get('banner1').get('create_time')
                    if create_time > 1496592000:
                        yield scrapy.Request(url,meta={'title':title,'time_sk':time_sk,'url':url},dont_filter=True,callback=self.parse1)
                    else:
                        os._exit(0)
                        
                if i.get('type') == "imagetext":
                    title = i.get('imagetext').get('title')
                    uid = i.get('imagetext').get('action').get('link').split('=')[-1]
                    time_sk = i.get('imagetext').get('create_time')
                    url = self.post.format(uid)
                    create_time = i.get('imagetext').get('create_time')
                    if create_time > 1496592000:
                        yield scrapy.Request(url, meta={'title': title, 'time_sk': time_sk, 'url': url},
                                           dont_filter=True, callback=self.parse1)
                    else:
                        break
                if i.get('type') == "video":
                    title = i.get('video').get('title')
                    uid = i.get('video').get('action').get('link').split('=')[-1]
                    time_sk = i.get('video').get('create_time')
                    url = self.video.format(uid)
                    create_time = i.get('video').get('create_time')
                    if create_time > 1496592000:
                        yield scrapy.Request(url, meta={'title': title, 'time_sk': time_sk, 'url': url},
                                             dont_filter=True, callback=self.parse1)
                    else:
                        break
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

