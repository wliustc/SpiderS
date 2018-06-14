# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import time
import re
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
class Zhibo8Spider(scrapy.Spider):
    name = "zhibo8_spiders"
    allowed_domains = ["zhibo8.cc"]
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(Zhibo8Spider,self).__init__(*args, **kwargs)
        self.url = 'https://bbs.zhibo8.cc/'
    def start_requests(self):
        yield scrapy.Request(self.url,dont_filter=True,meta={'url':self.url})
    def parse(self, response):
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            item = {}
            html = response.body
            name = Selector(text=html).xpath('//*[@class="forum-name"]/a/text()').extract()
            theme = Selector(text=html).xpath('//*[@class="forum-topic"]/text()').extract()
            reply = Selector(text=html).xpath('//*[@class="forum-reply"]/text()').extract()
            new = Selector(text=html).xpath('//*[@class="forum-con"]/span/text()').extract()
            for i in zip(name,theme,reply,new):
                item['live_name'] = i[0]
                item['theme'] = i[1]
                item['reply'] = i[2]
                new = re.findall('\d+',i[3])
                item['new'] = new[0]
                item['time'] = start_time
                yield item
