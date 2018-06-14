# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

class SecooSpider(scrapy.Spider):
    name = "secoo"
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(SecooSpider,self).__init__(*args,**kwargs)
        self.secoo = 'http://list.secoo.com/undefined/{}#pageTitle'
    def start_requests(self):
        secoo_list = ['1266-0-0-0-0-1-0-0-1-10-0-0-100-0.shtml','1554-0-0-0-0-1-0-0-1-10-0-0-100-0.shtml','1555-0-0-0-0-1-0-0-1-10-0-0-100-0.shtml','834-0-0-0-0-1-0-0-1-10-0-0-100-0.shtml']
        for i in secoo_list:
            url = self.secoo.format(i)
            yield scrapy.Request(url)
    def parse(self, response):
        time ={}
        html =  response.body
        shoes_data = Selector(text=html).xpath('//*[@class="bigList"]/div/ul[@class="showLogo"]/li/a/@title').extract()
        type_ = Selector(text=html).xpath('//*[@id="pageTitle"]/a[2]/h1/text()').extract()
        for i in zip(shoes_data):
            brand = i[0].replace(u'\u2022','*')
            time['brand'] = brand
            time['type'] =type_
            time['source'] = 'http://list.secoo.com'
            # print time
            yield time