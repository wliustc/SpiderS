# -*- coding: utf-8 -*-
import scrapy
import time
import re
from somefangchan.items import Somefangchan_yingshangItem
class YingshangSpider(scrapy.Spider):
    name = "yingshang"
    allowed_domains = ["bizsearch.winshang.com"]

    def start_requests(self):
        url='http://bizsearch.winshang.com/xiangmu/s0-c0-t0-k0-x0-d0-z0-n0-m0-l0-q0-b0-y0.html'
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Host':'bizsearch.winshang.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_type)

    def get_type(self,response):
        provices=response.xpath("//ul[@class='l-condition']/li[1]/ul/li")
        for i,provice in enumerate(provices):
            if i==0:
                continue
            pro_url=provice.css('a::attr("href")').extract()[0].split('/')[-1].split('-')[0]
            provice_name=provice.css('a::text').extract()[0]
            url='http://bizsearch.winshang.com/xiangmu/'+pro_url+'-c0-t0-k0-x0-d0-z0-n0-m0-l0-q0-b0-y0-pn1.html'
            header={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'bizsearch.winshang.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_item,
                                 meta={'item':{'provice':provice_name}})

    def get_item(self,response):
        datas=response.xpath('//li[@data-id]')
        if not datas:
            return
        for data in datas:
            item = Somefangchan_yingshangItem()
            item['deal_id']=data.css('::attr("data-id")').extract()[0]
            item['provice']=response.meta['item']['provice']
            item['dt']=time.strftime('%Y-%m-%d',time.localtime())
            item['platform']='赢商网'
            item['title']=data.css('h2 a::text').extract()[0]
            item['statics'] = data.xpath('//ul[contains(@class,"l-inf-list")]/li[1]/span[2]/text()').extract()[0]
            item['open_time']= data.xpath('//ul[contains(@class,"l-inf-list")]/li[2]/span[2]/text()').extract()[0]
            item['type']=data.xpath('//ul[contains(@class,"l-inf-list")]/li[3]/span[2]/text()').extract()[0]
            item['mianji'] = data.xpath('//ul[contains(@class,"l-inf-list")]/li[4]/span[2]/text()').extract()[0]
            item['need'] = data.xpath('//ul[contains(@class,"l-inf-list")]/li[5]/span[2]/text()').extract()[0]
            detail_url=data.css('h2 a::attr("href")').extract()[0]
            header={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'biz.winshang.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }
            yield scrapy.Request(detail_url,headers=header, dont_filter=True,callback=self.get_detail,meta={'item':item})

        page_num=response.xpath('//div[@id="AspNetPager1"]/a/text()').extract()
        if page_num and page_num[-2]=='...':
            page_num=response.url.split('/')[-1].split('.')[0].split('-')[-1]
            page_num=int(re.sub('[^0-9]+','',page_num))+1
            url=re.sub('-pn[0-9]+','-pn%s' %page_num,response.url)
            header={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'bizsearch.winshang.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_item,
                                 meta={'item':{'provice':response.meta['item']['provice']}})

    def get_detail(self,response):
        item=response.meta['item']
        item['city']=response.xpath('//ul[@class="d-inf-status"]/li/span[not(@class)]/text()').extract()[-2]
        item['address']=response.xpath('//ul[@class="d-inf-status"]/li/span[not(@class)]/text()').extract()[-1]
        yield item