# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import time

class B2cMallSpider(scrapy.Spider):
    name = 'B2c_mall'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(B2cMallSpider,self).__init__(*args,**kwargs)
        self.mall_url = 'http://www.ccxpet.com/Home'
        self.url ='http://www.ccxpet.com{list_pag}'
        self.sub_title_list = 'http://www.ccxpet.com/Product/{code}'
        self.sub_title_pag = 'http://www.ccxpet.com/Product/{code}?pageIndex={pag}'
    def start_requests(self):
        url = self.mall_url
        yield scrapy.Request(url,dont_filter=True)
    def parse(self, response):
        html = response.body
        title = Selector(text=html).xpath('//*[@id="cateMenu"]/a/text()').extract()
        href = Selector(text=html).xpath('//*[@id="cateMenu"]/a/@href').extract()
        for i in zip(title,href):
            url = self.url.format(list_pag=i[1])
            yield scrapy.Request(url,meta={'menu':i,'url':url},dont_filter=True,callback=self.b2c_list)

    def b2c_list(self,response):
        html = response.body
        menu = response.meta.get('menu')
        sub_title = Selector(text=html).xpath('//*[@class="catelist"]/@title').extract()
        sub_code = Selector(text=html).xpath('//*[@class="catelist"]/@cateid').extract()
        for i in zip(sub_title,sub_code):
            url = self.sub_title_list.format(code=i[1])
            yield scrapy.Request(url,meta={'menu':menu,'sub':i,'url':url},dont_filter=True,callback=self.sub_list)
    def sub_list(self,response):
        html = response.body
        menu = response.meta.get('menu')
        sub = response.meta.get('sub')
        pag = Selector(text=html).xpath('//*[@id="ProductListDiv"]/div/div/p/a/text()').extract()
        if len(pag):
            if len(pag) >3:
                for i in range(int(pag[-3])):
                    url = self.sub_title_pag.format(code=sub[1],pag=i)
                    yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.details)
            else:
                for i in range(int(pag[0])):
                    url = self.sub_title_pag.format(code=sub[1],pag=i)
                    yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.details)
        else:
            price = Selector(text=html).xpath('//*[@id="J_lazyload"]/li/a/h4/em/text()').extract()
            href = Selector(text=html).xpath('//*[@id="J_lazyload"]/li/a/@href').extract()
            for i in zip(price,href):
                url = self.url.format(list_pag=i[1])
                yield scrapy.Request(url,meta={'menu':menu,'sub':sub,'price':i},dont_filter=True,callback=self.b2c_price)

    def details(self,response):
        html = response.body
        price = Selector(text=html).xpath('//*[@id="J_lazyload"]/li/a/h4/em/text()').extract()
        href = Selector(text=html).xpath('//*[@id="J_lazyload"]/li/a/@href').extract()
        for i in zip(price, href):
            url = self.url.format(list_pag=i[1])
            response.meta['price'] = i
            yield scrapy.Request(url, meta=response.meta, dont_filter=True,callback=self.b2c_price)


    def b2c_price(self,response):
        item = {}
        html = response.body
        menu = response.meta.get('menu')
        sub = response.meta.get('sub')
        price = response.meta.get('price')
        b2c_name = ''.join(Selector(text=html).xpath('//*[@class="title"]/div[@class="title_1"]/span/text()').extract())
        sales = ''.join(Selector(text=html).xpath('//*[@id="buy_count"]/text()').extract())
        comments = ''.join(Selector(text=html).xpath('//*[@id="comment_count"]/text()').extract())
        code = ''.join(Selector(text=html).xpath('//*[@id="hdProductId"]/@value').extract())
        brand = b2c_name.split(' ')[0]
        item['tag'] = u'B2C商城'
        item['menu'] = menu[0]
        item['sub_title'] = sub[0]
        item['brand'] = brand
        item['b2c_name'] = b2c_name
        item['comments'] = comments
        item['sales'] = sales
        item['code'] = code
        item['price'] = price[0]
        item['b2c_type'] = ''
        item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
        yield item

        # print menu[0],sub[0],price[0],brand,b2c_name,code,sales,comments
