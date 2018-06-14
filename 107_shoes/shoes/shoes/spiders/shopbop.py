# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy import Selector
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import time
times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
class ShopbopSpider(scrapy.Spider):
    name = "shopbop"
    allowed_domains = []
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ShopbopSpider, self).__init__(*args, **kwargs)
        self.shopbou = 'http://cn.shopbop.com/shoes/br/v=1/13438.htm?baseIndex={}'
        self.pag = 0
    def start_requests(self):
        yield scrapy.Request(url=self.shopbou.format(self.pag),dont_filter=True)
    def parse(self, response):
        html = response.body
        pag =  ''.join(Selector(text=html).xpath('//*[@id="pagination-container-top"]/div[1]/span[6]/text()').extract())
        pag_=''.join(Selector(text=html).xpath('//*[@id="pagination-container-top"]/div[1]/span[3]/@data-number-link').extract())
        pag_=pag_.split('=')
        for i in range(0,int(pag)):
            url = self.shopbou.format(self.pag)
            self.pag+=int(pag_[-1])
            yield scrapy.Request(url,dont_filter=True,callback=self.parse1)

    def parse1(self,response):
        time = {}
        html = response.body
        brand = Selector(text=html).xpath('//*[@class="brand"]/text()').extract()
        title = Selector(text=html).xpath('//*[@class="title"]/text()').extract()
        prince = Selector(text=html).xpath('//*[@data-at="retail-price"]/text()').extract()
        brand_data = ','.join(brand).replace('\n','').replace(' ','').replace('\t','').split(',')
        title_data = ','.join(title).replace('\n','').replace(' ','').replace('\t','').split(',')
        print prince
        for i in zip(brand_data,title_data,prince):
            time['brand'] = i[0]
            time['title'] = i[1]
            time['prince'] = i[2].replace(u'US$\xa0','')
            time['type'] = u'女鞋'
            time['task_time'] = times
            yield time

    