# -*- coding: utf-8 -*-
import scrapy
import json
import web
from ..items import *
import time

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



class H5TaobaoSpider(scrapy.Spider):
    name = 'baili_id_picture'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(H5TaobaoSpider,self).__init__(*args,**kwargs)
        self.h5_url = 'https://{brand}.m.tmall.com/shop/shop_auction_search.do?sort=s&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp&p={pag}'
    def start_requests(self):
        sql = '''select shop_url from t_spider_taobao_baili_flagship_shop '''
        for i in db.query(sql):
            brand = i.get('shop_url')
            brand = brand.split('//')[1].split('.')[0]
            url = self.h5_url.format(brand=brand,pag=1)
            yield scrapy.Request(url,dont_filter=True,meta={'brand':brand,'url':url})
    def parse(self, response):
        brand = response.meta.get('brand')
        item = TaobaoBaidliItem()
        html = response.body
        try:
            html = json.loads(html[8:-1])
            pag = html.get('total_page')
            item['brand']= html.get('shop_title')
            for i in html.get('items'):
                item['dataid'] = i.get('item_id')
                item['merchandise_url'] = 'https://detail.tmall.com/item.htm?id='+str(i.get('item_id'))
                item['picture_url'] = 'https:'+i.get('img')
                item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
            if int(pag) >1:
                for i in range(2,int(pag)+1):
                    url = self.h5_url.format(pag=i,brand=brand)
                    yield scrapy.Request(url,callback=self.parse_pag,dont_filter=True,meta={'url':url})
        except:
            url = response.meta.get('url')
            yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta=response.meta)
    def parse_pag(self,response):
        item = TaobaoBaidliItem()
        # item = {}
        html = response.body
        try:
            html = json.loads(html[8:-1])
            item['brand'] = html.get('shop_title')
            for i in html.get('items'):
                item['dataid'] = i.get('item_id')
                item['merchandise_url'] = 'https://detail.tmall.com/item.htm?id='+str(i.get('item_id'))
                item['picture_url'] = 'https:'+i.get('img')
                item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
        except:
            url = response.meta.get('url')
            yield scrapy.Request(url, callback=self.parse_pag, dont_filter=True, meta=response.meta)










    
    
    
    
    
    
    