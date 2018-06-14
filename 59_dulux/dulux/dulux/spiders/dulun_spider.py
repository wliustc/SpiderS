# -*- coding: utf-8 -*-
import scrapy
import datetime
from dulux.items import DuluxItem

class DulunSpiderSpider(scrapy.Spider):
    name = "dulun_spider"
    allowed_domains = ["dulux.com"]
    start_urls = [
        'http://service.dulux.com.cn/search',
    ]

    def __init__(self, *args, **kwargs):
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d")

    def parse(self, response):
        list = response.css('.list li')
        for i in list:
            item = DuluxItem()
            #item["status"] = ""
            item['province'] = i.xpath('@data-province').extract()[0]
            item['name'] = i.xpath('@data-name').extract()[0]
            item['city'] = i.xpath('@data-city').extract()[0]
            #item['gender'] = ""
            item['level'] = i.xpath('@data-type').extract()[0]
            #item['custom'] = ""
            item['time'] = int(self.dt[0:4]) - int(i.xpath('@data-year').re(r'(\d*).*')[0])
            #item['id'] = ""
            item['company'] = 'dulux'
            item['getdate'] = self.dt
            yield item


    
    