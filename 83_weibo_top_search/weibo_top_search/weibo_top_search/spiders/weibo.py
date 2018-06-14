# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import time


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
headers = {'User-Agent': user_agent}
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        self.url = [[u'http://s.weibo.com/top/summary?cate=realtimehot', u'热搜榜']]
    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url[0], headers=headers, callback=self.parse, meta={'bang': url[1], 'url': url[0]})

    def parse(self, response):
        item = {}
        html = response.body
        bang = response.meta['bang']
        star_name = Selector(text=html).xpath('//*[@class="star_name"]/a/text()').extract()
        star_num = Selector(text=html).xpath('//*[@class="star_num"]/span/text()').extract()
        rank_long = Selector(text=html).xpath('//*[@class="rank_long"]/span/@style').extract()
        for rem in zip(star_name[1:], star_num, rank_long):
            item['bang'] = bang
            item['star_name'] = rem[0]
            item['star_num'] = rem[1]
            if len(rem[2]):
                item['rank_long'] = rem[2].split(':')[1]
            else:
                item['rank_long'] = ''
            item['time'] = start_time
            yield item
            # print item

    
    
    
    
    