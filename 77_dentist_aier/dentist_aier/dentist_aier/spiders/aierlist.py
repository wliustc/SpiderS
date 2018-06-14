# -*- coding: utf-8 -*-
import scrapy
from dentist_aier.items import YankeaierItem

class AierlistSpider(scrapy.Spider):
    name = "aierlist"
    allowed_domains = ["www.aierchina.com"]

    def start_requests(self):
        for i in range(1,90):
            url=''
            if i==1:
                url='http://www.aierchina.com/technical/zhuanjia/index.html'
            else:
                url='http://www.aierchina.com/technical/zhuanjia/list_%s.html' %(i)
            yield  scrapy.Request(url)

    def parse(self, response):
        if ('retry' in response.meta.keys()) and response.meta['retry'] < 0:
            yield {}
        else:
            try:
                lis = response.xpath('//*[@id="gyaierquanw"]/div[1]/div/div[2]/ul/li')
                for li in lis:
                    link=''.join(li.xpath('./ul/li[1]/a/@href')[0].extract())
                    yield scrapy.Request(link,callback=self.parse_detial,dont_filter=True)
            except Exception as e:
                print (e,'exception..................',response.url)
                if ('retry' in response.meta.keys()):
                    yield scrapy.Request(response.url, meta={'retry': response.meta['retry'] - 1}, callback=self.parse,
                                         dont_filter=True)
                else:
                    yield scrapy.Request(response.url, meta={'retry': 3}, callback=self.parse, dont_filter=True)

    def parse_detial(self, response):
        item=YankeaierItem()
        if ('retry' in response.meta.keys()) and response.meta['retry'] < 0:
            yield {}
        else:
            try:
                name = ''.join(response.xpath('//*[@id="gyaierquanw"]/div[1]/div/div[1]/ul/li[1]/text()').extract())
                hospital_name = ''.join(
                    response.xpath('//*[@id="gyaierquanw"]/div[1]/div/div[1]/ul/li[2]/span[1]/text()').extract())
                zhicheng = ''.join(''.join(response.xpath(
                    '//*[@id="gyaierquanw"]/div[1]/div/div[1]/ul/li[2]/span[2]/text()').extract()).split())
                professional = ''.join(''.join(
                    response.xpath('//*[@id="gyaierquanw"]/div[1]/div/div[1]/ul/li[3]/text()').extract()).split())
                summary = ''.join(
                    ''.join(response.xpath('//*[@id="gyaierquanw"]/div[1]/div/div[2]//text()').extract()).split())[4:]
                item['name'] = name  # 医生姓名
                item['hospital_detial'] = hospital_name  #
                item['zhicheng'] = zhicheng
                item['professional'] = professional
                item['summary'] = summary
                item['hospital']='爱尔眼科'
                item['url'] = response.url
                yield item
            except Exception as e:
                print(e, 'exception..................', response.url)
                if ('retry' in response.meta.keys()):
                    yield scrapy.Request(response.url, meta={'retry': response.meta['retry'] - 1}, callback=self.parse,
                                         dont_filter=True)
                else:
                    yield scrapy.Request(response.url, meta={'retry': 3}, callback=self.parse, dont_filter=True)

    