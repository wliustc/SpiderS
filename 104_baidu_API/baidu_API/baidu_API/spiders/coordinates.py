# -*- coding: utf-8 -*-
import scrapy
import web
import re
import json

from gps_coords_convertor import GPSCoordsConvertor
import sys
import random
reload(sys)
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

def random_KEY():
    key = [
        'dc0311f951cc0639b97277d931f326c0',
        '6b84d51c8195c3827ef02d9fa783eb1f',
        'fad0cc4413f73ef6a31ada1f095de971',
        '1d503ace4b1c2833b76bd02b4bedcd2d'
           ]
    random_key = random.choice(key)
    return random_key





class CoordinatesSpider(scrapy.Spider):
    name = 'coordinates'
    allowed_domains = []
    def __init__(self,*args,**kwargs):
        super(CoordinatesSpider,self).__init__(*args,**kwargs)
        self.baidu_url = '''http://api.map.baidu.com/?qt=gc&wd={addr}&cn={city}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk16762&ak=E4805d16520de693a3fe707cdc962045 '''
        self.amap = '''http://restapi.amap.com/v3/geocode/geo?key={key}&address={addr} '''
    def start_requests(self):
        sql = ''' SELECT * FROM `sheet2` '''
        # sql = ''' SELECT id,data_id,legalpersonid,name,reginstitute,addr,companyorgtype,companyorgtype_new,legalpersonname,regstatus,state_new,company_name,businessscope,industry,brand FROM `t_xsd_tianyancha_medicine_city_new` WHERE reginstitute IS NULL '''
        for i in db.query(sql):
            reginstitute = i.get('reginstitute')
            if reginstitute == None:
                url = self.amap.format(key=random_KEY(), addr=reginstitute)
                yield scrapy.Request(url, meta={'data': i}, dont_filter=True, callback=self.parse)
            else:
                url = self.amap.format(key=random_KEY(),addr=reginstitute)
                yield scrapy.Request(url,meta={'data':i},dont_filter=True,callback=self.parse)

    def parse(self,response):
        html = json.loads(response.body)
        item = response.meta.get('data')
        addr = item.get('addr')
        try:
            province = html.get('geocodes')[0].get('province')
            city = html.get('geocodes')[0].get('city')
            district = html.get('geocodes')[0].get('district')
            item['province'] = province
            item['city'] = city
            item['district'] = district
            if district == None:
                district = city
                url = self.baidu_url.format(addr=addr,city=district,)
                yield scrapy.Request(url,meta={'data':item},dont_filter=True,callback=self.baidu_api)
            else:
                url = self.baidu_url.format(addr=addr, city=district, )
                yield scrapy.Request(url, meta={'data': item}, dont_filter=True, callback=self.baidu_api)
        except Exception as e:
            url = self.baidu_url.format(addr=addr,city='')
            yield scrapy.Request(url, meta={'data': item}, dont_filter=True, callback=self.baidu_api)

    def baidu_api(self,response):
        try:
            html = json.loads(response.body.split('&&')[1][20:-1])
        except:
            html = json.loads(response.body)
        try:
            coord = html.get('content').get('coord')
            url = 'http://api.map.baidu.com/?qt=rgc&x={x}&y={y}&dis_poi=100&poi_num=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk83461&ak=E4805d16520de693a3fe707cdc962045'
            url = url.format(x=coord.get('x'), y=coord.get('y'))
            # catalog = html.get('content').get('catalog')
            response.meta.get('data')['mc_lng'] = coord.get('x')
            response.meta.get('data')['mc_lat'] = coord.get('y')
            # response.meta.get('data')['catalog'] = catalog
            yield scrapy.Request(url, meta=response.meta, dont_filter=True, callback=self.address)
        except:
            yield response.meta.get('data')

    def address(self, response):
        item = response.meta.get('data')
        try:
            html = json.loads(response.body.split('&&')[1][20:-1])
            content = html.get('content')
            # item['baidu_addr'] = content.get('address')
            item['city'] = content.get('address_detail').get('city')
            item['district'] = content.get('address_detail').get('district')
            item['province'] = content.get('address_detail').get('province')
            # item['street'] = content.get('address_detail').get('street')
            # item['poi_desc'] = content.get('poi_desc')
            lng, lat = GPSCoordsConvertor.convert_mc_2_gps(float(item.get('mc_lng')), float(item.get('mc_lat')))
            item['lng'] = lng
            item['lat'] = lat
            yield item
        except Exception as e:
            print e








    
    
    
    
    
    
    