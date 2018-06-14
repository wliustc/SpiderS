# -*- coding: utf-8 -*-
import scrapy
import web

import json

import sys
import random
reload(sys)
sys.setdefaultencoding('utf8')

def random_KEY():
    key = [
        'dc0311f951cc0639b97277d931f326c0',
        '6b84d51c8195c3827ef02d9fa783eb1f',
        'fad0cc4413f73ef6a31ada1f095de971',
        '1d503ace4b1c2833b76bd02b4bedcd2d'
           ]
    random_key = random.choice(key)
    return random_key
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')






class CoordinatesSpider(scrapy.Spider):
    name = 'amap_baidu_tianmao'
    allowed_domains = []
    def __init__(self,*args,**kwargs):
        super(CoordinatesSpider,self).__init__(*args,**kwargs)
        self.baidu_url = '''http://api.map.baidu.com/?qt=gc&wd={addr}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk16762&ak=E4805d16520de693a3fe707cdc962045 '''
        self.amap = '''http://restapi.amap.com/v3/geocode/geo?key={key}&address={addr}'''
    def start_requests(self):
            sql = '''SELECT * FROM `t_spider_tianmao_addr`;'''
            for i in db.query(sql):
                addr = i.get('addr')
                url = self.baidu_url.format(addr=addr)
                yield scrapy.Request(url,meta={'data':i},dont_filter=True,callback=self.baidu_api)

    def parse(self,response):

        html = json.loads(response.body)
        item = response.meta.get('data')
        addr = item.get('city')
        try:
            city = html.get('geocodes')[0].get('city')
            province = html.get('geocodes')[0].get('province')
            district = html.get('geocodes')[0].get('district')
            item['baidu_city'] = city
            item['baidu_province'] = province
            yield item
        except:
            url = self.baidu_url.format(addr=addr)
            # yield scrapy.Request(url, meta={'data': item}, dont_filter=True, callback=self.baidu_api)



    def baidu_api(self,response):
        item = response.meta['data']
        try:
            html = json.loads(response.body.split('&&')[1][20:-1])
        except:
            html = json.loads(response.body)
        try:
            coord = html.get('content').get('coord')
            url = 'http://api.map.baidu.com/?qt=rgc&x={x}&y={y}&dis_poi=100&poi_num=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk83461&ak=E4805d16520de693a3fe707cdc962045'
            url = url.format(x=coord.get('x'), y=coord.get('y'))
            # catalog = html.get('content').get('catalog')
            # response.meta.get('data')['mc_lng'] = coord.get('x')
            # response.meta.get('data')['mc_lat'] = coord.get('y')
            # response.meta.get('data')['catalog'] = catalog
            yield scrapy.Request(url, meta={'data':item}, dont_filter=True, callback=self.address)
        except:
            yield item

    def address(self, response):
        item = response.meta.get('data')
        try:
            html = json.loads(response.body.split('&&')[1][20:-1])
            content = html.get('content')
            # item['baidu_addr'] = content.get('address')
            item['A23'] = content.get('address_detail').get('city')
            # item['district'] = content.get('address_detail').get('district')
            item['A24'] = content.get('address_detail').get('province')
            # item['street'] = content.get('address_detail').get('street')
            # item['poi_desc'] = content.get('poi_desc')
            # lng, lat = GPSCoordsConvertor.convert_mc_2_gps(float(item.get('mc_lng')), float(item.get('mc_lat')))
            # item['lng'] = lng
            # item['lat'] = lat
            yield  item

        except Exception as e:
            print e





    