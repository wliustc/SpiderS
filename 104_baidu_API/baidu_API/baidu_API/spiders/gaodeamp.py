# -*- coding: utf-8 -*-
import json
import sys

import scrapy
import web
from coordTransform_utils import *
# from test_trans_geo import trans_geo

reload(sys)
sys.setdefaultencoding('utf8')
import random
def random_KEY():
    key = [
        'dc0311f951cc0639b97277d931f326c0',
        '6b84d51c8195c3827ef02d9fa783eb1f',
        'fad0cc4413f73ef6a31ada1f095de971',
        '1d503ace4b1c2833b76bd02b4bedcd2d'
           ]
    random_key = random.choice(key)
    return random_key


class GaodeampSpider(scrapy.Spider):
    name = "gaodeamp"
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(GaodeampSpider,self).__init__(*args,**kwargs)
        self.amap = 'http://restapi.amap.com/v3/geocode/geo?key={key}&address={addr}'

    def start_requests(self):
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        #db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

        sql = ''' select * from t_xsd_chemist_core_data limit 100 ''' ###更改
        data = db.query(sql)
        for i in data:
            addr = i.get('name')
            url = self.amap.format(key=random_KEY(),addr=addr)
            yield scrapy.Request(url,meta={'data':i},dont_filter=True)
            # url = 'http://restapi.amap.com/v3/geocode/geo?key=fad0cc4413f73ef6a31ada1f095de971&address=%E4%B8%80%E6%A0%A1%E8%A5%BF'
            # yield scrapy.Request(url,dont_filter=True)

    def parse(self, response):
        html = json.loads(response.body)
        if html.get('status') != '1' and html.get('status') !='0':
            addr = response.meta.get('data').get('addr')
            url = self.amap.format(key=random_KEY(),addr=addr)
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse)
        else:
            time = response.meta['data']
            if html.get('count') == '0' and response.meta.get('data').get('retry') !=1:
                addr = response.meta.get('data').get('addr')
                url = self.amap.format(key=random_KEY(),addr=addr)
                response.meta['data']['retry'] = 1
                yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse)
            else:
                try:
                    location = html.get('geocodes')[0].get('location')
                    x,y = location.split(',')
                    convert = gcj02_to_bd09(float(x),float(y))
                    if len(html.get('geocodes')) !=0:
                        province = html.get('geocodes')[0].get('province')
                        if type(province) is not list:
                            # time['province'] = html.get('geocodes')[0].get('province')
                            time['province'] = province
                        city = html.get('geocodes')[0].get('city')
                        if type(city) is not list:
                            # time['city'] = html.get('geocodes')[0].get('city')
                            time['city'] = city
                        district = html.get('geocodes')[0].get('district')
                        if type(district) is not list:
                            time['district'] = district
                        # time['district'] = html.get('geocodes')[0].get('district')
                        time['baidu_lat'] = convert[0]
                        time['baidu_lng'] = convert[1]
                        time['lat'] = x
                        time['lng'] = y
                        yield time
                except:
                    yield time

    
    