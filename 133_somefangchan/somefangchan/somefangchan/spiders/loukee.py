# -*- coding: utf-8 -*-
import scrapy
import re
import time
from somefangchan.items import Somefangchan_yingshangItem
class LoukeeSpider(scrapy.Spider):
    name = "loukee"
    allowed_domains = ["http://www.loukee.com"]
    start_urls = [{'url':'http://www.loukee.com/list/1','type':'写字楼'},
                  {'url':'http://www.loukee.com/list/2','type':'蜂巢办公'},
                  {'url':'http://www.loukee.com/list/3','type':'创意园'}]

    def start_requests(self):
        header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Host':'www.loukee.com',
        'Referer':'http://www.loukee.com/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        for start_url in self.start_urls:
            yield scrapy.Request(start_url['url'],headers=header,dont_filter=True,callback=self.get_distract_list,meta={'item':
                                    {'type':start_url['type'],'city':'上海'}})

    def get_distract_list(self,response):
        distract_lists=response.css('#ddDistrict a')
        header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Host':'www.loukee.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',

        }
        for distract_list in distract_lists:
            if distract_list.css('::text').extract()[0]=='不限':
                continue
            url='http://www.loukee.com'+distract_list.css('::attr("href")').extract()[0]
            item=response.meta['item']
            item['distract']=distract_list.css('::text').extract()[0]
            yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_page_num,meta={'item':item})

    def get_page_num(self,response):
        try:
        	num=int(re.sub('[^0-9]+','',response.css('.record-count::text').extract()[0]))
        except Exception as e:
            return
        num=bool(num%10)+num//10
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'www.loukee.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        for i in range(1,num+1):
            url=response.url+'&pn=%s' %i
            yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_detail,meta={'item':response.meta['item']})


    def get_detail(self,response):
        temp=response.meta['item']
        datas=response.css('div.l_sub.fl')
        for data in datas:
            item=Somefangchan_yingshangItem()
            item.update(temp)
            url='http://www.loukee.com'+data.css('h2 a::attr("href")').extract()[0]
            item['deal_id']=url.split('/')[-1]
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'www.loukee.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_item,meta={'item':item})

    def get_item(self,response):
        item=response.meta['item']
        if item['type']=='蜂巢办公':
            item['title'] = response.css(".main-title h1::text").extract()[0]
            item['address'] = response.xpath('//div[@class="addr"]/h2/text()').extract()[0]
            item['price'] = response.css('.avgprice h2::text').extract()[0]+response.css('.avgprice em::text').extract()[0]
            try:
            	item['connect_phone'] = response.css('.space .title::text').extract()[0]
            except Exception as e:
                pass
        else:
            item['title']=response.css(".title h1::text").extract()[0]
            item['address']=response.xpath('//div[@class="con_cs"]/dl/dd[1]/span/text()').extract()[0]
            item['connect_phone']=response.css('.sphone::text').extract()[0]
            item['price']=response.css('.price span::text').extract()[0]+response.css('.price em::text').extract()[0]
            try:
            	item['developer']=response.xpath('//div[@class="con_cs"]/dl/dd[3]/span/text()').extract()[0]
            except Exception as e:
                pass
            item['mianji']=response.xpath('//div[@class="con_cs"]/dl/dd[5]/span/text()').extract()[0]
        item['provice']='上海市'
        item['dt'] = time.strftime('%Y-%m-%d',time.localtime())
        item['platform']='楼客'
        yield item
    
    
    
    
    
    
    