# -*- coding: utf-8 -*-
import scrapy
import sqlalchemy
import time
from meituan_pet_server.items import MeituanPetAppdealIdItem
from meituan_pet_server.items import MeituanPetAppweizhiItem
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
class AppShopGetSpider(scrapy.Spider):
    name = "app_shop_get"
    allowed_domains = ["i.meituan.com"]

    def start_requests(self):
        url='https://i.meituan.com/'
        yield scrapy.Request(url,headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        },callback=self.get_shop_item,errback=self.error_callback,meta={'timerequest':0})

    def get_shop_item(self,response):
        conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                        connect_args={'charset': 'utf8'})
        cur=conn.connect()
        temp=cur.execute('SELECT distinct `mtshop_id`,`host`,`mtshop_name` FROM tuangou_meituan_shop_info where TO_DAYS(NOW()) - TO_DAYS(`dt`) <= 3;')# where `dt`=DATE(now())
        #SELECT distinct `mtshop_id`,`host`,`mtshop_name` FROM tuangou_meituan_shop_info where TO_DAYS(NOW()) - TO_DAYS(`dt`) <= 3;
        temp=temp.fetchall()
        for i,tmp in enumerate(temp):
            url='https://i.meituan.com/poi/%s' %tmp[0]
            yield scrapy.Request(url,headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Host':'i.meituan.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            },callback=self.goto_shop_item,meta={'cookiejar':i,'item':{'shop_id':tmp[0],'shop_name':tmp[1]},'timerequest':0},errback=self.error_callback)

    def goto_shop_item(self,response):
        try:
            item_weizhi=MeituanPetAppweizhiItem()
            weizhi_data=response.xpath('//div[@class="kv-line-r"]/h6/a/@href').extract()[0]
            weizhi_data=re.search('coord:(?P<name>.+?);',weizhi_data).groupdict()['name']
            lng=weizhi_data.split(',')[1]#经度
            lat=weizhi_data.split(',')[0]#纬度
            item_weizhi['shop_id']=response.meta['item']['shop_id']
            item_weizhi['shop_name'] = response.meta['item']['shop_name']
            item_weizhi['lng'] = lng
            item_weizhi['lat'] = lat
            item_weizhi['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            yield item_weizhi
        except Exception as e:
            self.logger.error('cannot get weizhi %s ' %response.meta['item']['shop_id'],response.url)
        datas=response.xpath('//body/dl[@class="list"]//dd//dd')
        for data in datas:
            item=MeituanPetAppdealIdItem()
            item['shop_id']=response.meta['item']['shop_id']
            item['deal_id']=data.css('a::attr("href")').extract()[0]
            url='http:'+item['deal_id']
            item['deal_id']=item['deal_id'].split('/')[-1].split('.')[0]
            item['title']=data.css('a::attr("title")').extract()[0]
            item['price']=re.sub('[^0-9]+','',data.css('.price .strong::text').extract()[0])
            try:
                item['old_price']=re.sub('[^0-9]+','',data.css('del::text').extract()[0])
            except Exception as e:
                item['old_price'] = 0
            item['text']=data.css('.title::text').extract()[0]
            item['sale']=re.sub('[^0-9]+','',data.css('.statusInfo::text').extract()[0])
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            yield item

    def error_callback(self, failure):
        request = failure.request
        if request.meta['timerequest']>10:
            self.logger.error('qfliu retrytime out %s', request.url)
            return
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            if response.status==404:
                return
            self.logger.error('HttpError on %s ,%s,proxy %s', response.url,response.status,request.meta['proxy'])
            request.meta['timerequest'] += 1
            yield request
        elif failure.check(DNSLookupError):
            self.logger.error('DNSLookupError on %s', request.url)
            request.meta['timerequest'] += 1
            yield request
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('TimeoutError on %s', request.url)
            request.meta['timerequest'] += 1
            yield request
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    