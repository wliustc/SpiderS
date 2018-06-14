# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Selector
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import time
times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
class ShopbopSpider(scrapy.Spider):
    name = "shopbop_nan"
    allowed_domains = []
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ShopbopSpider, self).__init__(*args, **kwargs)
        self.shopbou = 'https://www.eastdane.com/actions/updateFilterOptions.action?department=19186&sortBy.sort=PRIORITY%3ANATURAL&filterContext=19186&tDim=220x390&swDim=18x17&baseIndex={}'
        self.pag = 0
    def start_requests(self):
            yield scrapy.Request(url=self.shopbou.format(self.pag),dont_filter=True)
    def parse(self, response):
        html = json.loads(response.body)
        count = html.get('responseData').get('results').get('metadata').get('totalProductCount')
        pag = html.get('responseData').get('results').get('metadata').get('inStockProductCount')
        pag_ = int(count) / int(pag)
        for i in range(0,int(pag_)+1):
            url = self.shopbou.format(self.pag)
            print url
            self.pag+=int(pag)
            yield scrapy.Request(url,dont_filter=True,callback=self.parse1)

    def parse1(self,response):
        time = {}
        html = json.loads(response.body)
        for i in html.get('responseData').get('results').get('products'):
            title = i.get('shortDescription')
            brand = i.get('brand')
            price = i.get('prices')[0].get('amount').replace(u'\xa0','').replace(u'US$','')
            time['brand'] = brand
            time['title'] = title
            time['prince'] = price
            time['type'] = u'男鞋'
            time['task_time'] = times
            yield time

    
    
    