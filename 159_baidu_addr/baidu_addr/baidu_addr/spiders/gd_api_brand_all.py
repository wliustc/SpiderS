# -*- coding: utf-8 -*-
#高德搜索 types为搜索类型
import scrapy
import re
import json
# from ..items import GdCwssItem
from scrapy.selector import Selector
import random
import time
import web
#db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def random_KEY():
    # key = [ 'd3a1add365ef104fcfe6fd01a4131b3c', '626bbdcc1127a60818828c40a5a5c2a3',
    #         '8d9cba3557fc264c01d2546c4f52afa7', '758878a7e03dac7a5482155ff9daaeda',
    #         'dc0311f951cc0639b97277d931f326c0', '6b84d51c8195c3827ef02d9fa783eb1f',
    #         'fad0cc4413f73ef6a31ada1f095de971', '1d503ace4b1c2833b76bd02b4bedcd2d']
    key = ['dc0311f951cc0639b97277d931f326c0','6b84d51c8195c3827ef02d9fa783eb1f','fad0cc4413f73ef6a31ada1f095de971','1d503ace4b1c2833b76bd02b4bedcd2d']
    random_key = random.choice(key)
    return random_key

class CwssSpider(scrapy.Spider):
    # download_delay = 10
    name = "api_brand_all"
    allowed_domains = [ "ditu.amap.com"]


    def __init__(self, *args, **kwargs):  # 继承并初始化函数
        super(CwssSpider, self).__init__(*args, **kwargs)  # 继承类
        # self.rim_url = 'http://restapi.amap.com/v3/place/text?key={key}&types=060900&city={city}&children=1&page={pag}&offset=50&page=1&extensions=all'
        self.rim_url = 'http://restapi.amap.com/v3/place/text?key={key}&city={city}&keywords={keyword}&children=1&page={pag}&offset=50&page=1&extensions=all'
        self.start_urls = []


    #连接数据库取出所需字段
    def start_requests(self):
        # city_list = ['北京市','上海市','深圳市','广州市','天津市','西安市','成都市','重庆市','郑州市','武汉市','太原市','大连市','青岛市','兰州市','长沙市','杭州市','金华市','苏州市','无锡市','镇江市','南京市','合肥市','南宁市','南昌市','东莞市','佛山市','台州市']
        brand_list = ['和睦家','维世达','国际医疗中心','百汇医疗','和合益生','卓正医疗','联合医务','优合诊所','强森医疗','企鹅医生','蓝卡诊所','邻家好医','华润凤凰UCC','吕医生','正广兴','正安中医']
        # for br in city_list:
        sql = '''select province,name,adcode from t_xsd_amap where level="district" '''
        # sql = '''select province,name,adcode from t_xsd_amap where name="{}"  '''.format(br)
        for i in db.query(sql):
            province = i.get('province')
            name = i.get('name')
            adcode = i.get('adcode')
            ak = random_KEY()
            for dd in brand_list:
                url = self.rim_url.format(key=ak,city=name,pag=1,keyword=dd)
                yield scrapy.Request(url,meta={'url':url,'province':province,'name':name,'adcode':adcode,'pag':1,'keyword':dd})
    def parse(self, response):  #解析入口url
        if response.status != 200:
            yield scrapy.Request(response.meta['url'],callback=self.parse, meta=response.meta, dont_filter=True)
        if json.loads(response.body).get('infocode') != '10000':
            url = self.rim_url.format(ke=random_KEY(), city=response.meta.get('name'), pag=response.meta.get('pag'),keyword=response.meta.get('keyword'))
            yield scrapy.Request(url, callback=self.api_pag, meta=response.meta, dont_filter=True)
        else:
            html = json.loads(response.body)
            count = html.get('count')
            count = int(count) / 50
            if count == 0:
                item = {}
                for i in html.get('pois'):
                    item['uid'] = ''.join(i.get('id'))
                    item['type'] = ''.join(i.get('type'))
                    item['typecode'] = ''.join(i.get('typecode'))
                    item['name'] = ''.join(i.get('name'))
                    item['addr'] = ''.join(i.get('address'))
                    item['location'] = ''.join(i.get('location'))
                    item['tel'] = ''.join(i.get('tel'))
                    item['cityname'] = ''.join(i.get('cityname'))
                    item['adname'] = ''.join(i.get('adname'))
                    item['business_area'] = ''.join(i.get('business_area'))
                    item['rating'] = ''.join(i.get('biz_ext').get('rating'))
                    item['adcode'] = ''.join(i.get('adcode'))
                    item['pname'] = ''.join(i.get('pname'))
                    item['type'] = ''.join(i.get('type'))
                    item['typecode'] = ''.join(i.get('typecode'))
                    keyword_ = response.meta.get('keyword')
                    if keyword_ in item['name']:
                        yield item
            else:
                adcode = response.meta.get('adcode')
                name = response.meta.get('name')
                keyword = response.meta.get('keyword')
                count+=1
                for i in range(1,count+1):
                    ak = random_KEY()
                    url = self.rim_url.format(key=ak,city=name,pag=i,keyword=keyword)
                    yield scrapy.Request(url,meta={'adcode':name,'pag':i,'keyword':keyword},dont_filter=True,callback=self.api_pag)
    def api_pag(self,response):
        if response.status != 200:
            url = self.rim_url.format(ke=random_KEY(),city=response.meta.get('name'),pag=response.meta.get('pag'),keyword=response.meta.get('keyword'))
            yield scrapy.Request(url,callback=self.api_pag, meta=response.meta, dont_filter=True)
        if json.loads(response.body).get('infocode') != '10000':
            url = self.rim_url.format(ke=random_KEY(), city=response.meta.get('name'), pag=response.meta.get('pag'),keyword=response.meta.get('keyword'))
            yield scrapy.Request(url, callback=self.api_pag, meta=response.meta, dont_filter=True)
        else:
            item = {}
            html = json.loads(response.body)
            for i in html.get('pois'):
                item['uid'] = ''.join(i.get('id'))
                item['name'] = ''.join(i.get('name'))
                item['addr'] = ''.join(i.get('address'))
                item['location'] = ''.join(i.get('location'))
                item['tel'] = ''.join(i.get('tel'))
                item['cityname'] = ''.join(i.get('cityname'))
                item['adname'] = ''.join(i.get('adname'))
                item['business_area'] = ''.join(i.get('business_area'))
                item['rating'] = ''.join(i.get('biz_ext').get('rating'))
                item['adcode'] = ''.join(i.get('adcode'))
                item['pname'] = ''.join(i.get('pname'))
                item['type'] = ''.join(i.get('type'))
                item['typecode'] = ''.join(i.get('typecode'))
                keyword_ = response.meta.get('keyword')
                if keyword_ in item['name']:
                    yield item







    
    
    