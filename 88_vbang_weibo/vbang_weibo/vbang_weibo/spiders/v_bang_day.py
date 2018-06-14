# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json
from vbang_weibo.items import VbangItem

class VBangSpider(scrapy.Spider):
    name = "v_bang_day"
    allowed_domains = ["v6.bang.weibo.com"]

    def start_requests(self):
        yield scrapy.Request('http://v6.bang.weibo.com/czv/domainlist',
             headers={
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding':'gzip, deflate, sdch',
             'Accept-Language':'zh-CN,zh;q=0.8',
             'Connection':'keep-alive',
             'Host':'v6.bang.weibo.com',
             'Upgrade-Insecure-Requests':'1',
             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        },
        dont_filter=True
        )
        pass

    def parse(self, response):
        datas=response.xpath('//ul[@class="clearfix"]//a')
        for data in datas:
            kind=data.xpath('text()').extract()[0]
            link='http://v6.bang.weibo.com'+data.xpath('@href').extract()[0].split('?')[0]
            date=['?period=week','?period=month','?period=day']
            for tmp in date:
                url=link+tmp
                yield scrapy.Request(url,callback=self.request_link,dont_filter=True,
                             headers={
                             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                             'Accept-Encoding':'gzip, deflate, sdch',
                             'Accept-Language':'zh-CN,zh;q=0.8',
                             'Cache-Control':'max-age=0',
                             'Connection':'keep-alive',
                             'Host':'v6.bang.weibo.com',
                             'Referer':'http://v6.bang.weibo.com/czv/domainlist?luicode=40000050',
                             'Upgrade-Insecure-Requests':'1',
                             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                              },
                            meta={'item':{'kind':kind}})

    def request_link(self,response):
        data=response.xpath('//script')[7].extract()
        data=re.findall('\([\s\S]+[)]',data)[0]
        data=json.loads(data.strip('()'))
        day=data['data']['tab_data'][0]
        day['domainId']=data['data']['domainId']
        day['kind']=response.meta['item']['kind']
        day['url']=response.url
        req=[x for x in self.request_day(day)]
        for i in req:
            yield i

    def paser_item(self,response):
        data=response.body
        data=json.loads(data)
        if data['msg']=='success':
            for temp in data['data']['rankData']:
                item=VbangItem()
                item['name']=temp['screen_name']
                item['weibo_uid'] = temp['uid']
                item['user_type'] = str(temp['user_type'])
                item['desc'] = temp['desc']
                item['seq'] = str(temp['seq'])
                item['kind'] = response.meta['item']['kind']
                item['dt'] =time.strftime('%Y-%m-%d',time.localtime(time.time()))
                yield item

    def request_day(self,temp):
        domainId=temp['domainId']
        day=temp['time_text']    #05.15
        day=re.sub('\.','',day)
        year=time.strftime('%Y',time.localtime(time.time()))
        day=year+day
        # #20170515
        for i in range(1, 6):

            yield scrapy.FormRequest(
                'http://v6.bang.weibo.com/aj/wemedia/rank?ajwvr=6&__rnd=' + str(int(time.time() * 1000)),
                headers={
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'v6.bang.weibo.com',
                    'Origin': 'http://v6.bang.weibo.com',
                    'Referer': 'http://v6.bang.weibo.com/czv/kexue?luicode=40000050',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                formdata={
                    'type': '3',
                    'period': 'day',
                    'date': str(day),
                    'pagesize': '20',
                    'page': str(i),
                    'domainId': str(domainId),
                    '_t': '0',
                },
                callback = self.paser_item,
                dont_filter=True,
                meta={'item':{'kind':temp['kind']}})
    
    