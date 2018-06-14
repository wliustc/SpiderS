# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy import Request
from LePu.items import LepuItem

class LepuSpider(scrapy.Spider):
    name = "lepu"
    allowed_domains = ["lepu.cn"]
    # start_urls = ['http://www.lepu.cn/shop/']
    # start_urls = ['http://m.lepu.cn/shop/list/']

    def start_requests(self):
        url = 'http://api.lepu.cn/shop/search/?page=1&keyword=&wide=&&page=1'
        yield Request(url,callback=self.parse)

    def parse(self,response):
        # with open('fffff','a') as f:
        #     f.write(response.body)
        content = response.body
        content_json = json.loads(content)
        data = content_json.get('data')
        if data:
            total = data.get('total')
            pagesize = 25
            if total % total != 0:
                page = total / pagesize + 1
            else:
                page = total / pagesize
            for i in xrange(1,page+1):
                yield Request(url='http://www.lepu.cn/shop/p%s/'%i,callback=self.parse_list,dont_filter=True)



    def parse_list(self, response):
        if response.status!=200:
            yield Request(response.url,callback=self.parse_failure,dont_filter=True)
        else:
            sel = Selector(response)
            shop_links = sel.xpath('//div[@class="item_midle fl"]/div/h2/a/@href').extract()
            for shop_link in shop_links:
                yield Request(shop_link.replace('www','m'),callback=self.parse_detail,errback=self.parse_failure)


    def parse_detail(self,response):
        if response.status!=200:
            yield Request(response.url,callback=self.parse_detail,errback=self.parse_failure,dont_filter=True)
        else:
            item = LepuItem()
            content = response.body
            if 'Lightspeed System' in content:
                yield Request(response.url, callback=self.parse_detail, errback=self.parse_failure,dont_filter=True)
            # print content
            else:
                item['response_body'] = content
                yield item


    def parse_failure(self,failure):
        url = failure.request.url
        if 'detail' in url:
            yield Request(url, callback=self.parse_detail, errback=self.parse_failure,dont_filter=True)
        elif 'shop' in url:
            yield Request(url, callback=self.parse, errback=self.parse_failure,dont_filter=True)
        print
        pass
    