# -*- coding: utf-8 -*-
import scrapy
import web
import re
import json
import urllib
from scrapy import Selector
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class BrandListSpider(scrapy.Spider):
    name = 'brand_list'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(BrandListSpider,self).__init__(*args,**kwargs)
        self.list = 'https://list.tmall.com/search_shopitem.htm?oq={brand}&style=sg&sort=s&user_id={suid}&s={page}'
        self.list_api = 'https://s.taobao.com/search?q={}&tab=mall' #s=44
    def start_requests(self):
        type_list = ['&sort=sale-desc','&sort=renqi-desc']

        sql = '''select suid,title from t_spider_taobao_baili_flagship_shop '''

        for i in db.query(sql):
            suid = i.get('suid')
            title = i.get('title')
            url = self.list_api.format(title)+'&s=4356'
            yield scrapy.Request(url,meta={'suid':suid,'title':title,'url':url},dont_filter=True)
        for x in db.query(sql):
            suid = x.get('suid')
            title = x.get('title')
            for type_ in type_list:
                url = self.list_api.format(title)+type_+'&s=0'
                yield scrapy.Request(url,meta={'suid':suid,'title':title,'url':url},dont_filter=True)
    def parse(self, response):
        html = response.body
        page = re.findall('totalPage":(.*?),"currentPage', html, re.S)
        title = response.meta['title']
        suid = response.meta['suid']
        print '*' * 20, response.meta['url'].decode('utf8')
        if len(page):
            item = {}
            page = page[0]
            html = re.findall('g_page_config = (.*?)};.*?g_srp_loadCss', html, re.S)
            html = html[0]+'}'
            item['data'] = html
            item['suid'] = suid
            item['title'] = title
            yield item
            if int(page) >1:
                s = response.meta['url'].split('&s=')
                pageSize = int(s[1])
                if pageSize == 4356:
                    pageSize = -44
                for i in range(2,int(page)+1):
                    pageSize +=44
                    url = s[0]+'&s='+str(pageSize)
                    print '*'*20,url.decode('utf8')
                    yield scrapy.Request(url,meta={'suid':suid,'title':title,'url':url},dont_filter=True,callback=self.parse_list)
        else:
            url = response.meta['url']
            yield scrapy.Request(url,meta=response.meta,dont_filter=True)


    def parse_list(self,response):
        html = response.body
        title = response.meta['title']
        suid = response.meta['suid']
        item = {}
        try:
            html = re.findall('g_page_config = (.*?)};.*?g_srp_loadCss', html, re.S)
            html = html[0] + '}'
            item['data'] = html
            item['suid'] = suid
            item['title'] = title
            yield item
        except:
            url = response.meta['url']
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse_list)



    
    
    
    