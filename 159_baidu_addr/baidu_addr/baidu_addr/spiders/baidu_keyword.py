# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import web
import re
from  gps_coords_convertor import *
#db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

reload(sys)
sys.setdefaultencoding('utf8')

class Rectangle():
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def split_rectangle(self):
        center_x, center_y = self.get_center_position()
        r1 = Rectangle(self.min_x, self.min_y, center_x, center_y)
        r2 = Rectangle(self.min_x, center_y, center_x, self.max_y)
        r3 = Rectangle(center_x, center_y, self.max_x, self.max_y)
        r4 = Rectangle(center_x, self.min_y, self.max_x, center_y)
        result = []
        result.append(r1)
        result.append(r2)
        result.append(r3)
        result.append(r4)
        return result

    def get_center_position(self):
        len_x, len_y = self.get_width_height()
        offset_x = len_x / 2.0
        offset_y = len_y / 2.0
        center_x = self.min_x + offset_x
        center_y = self.min_y + offset_y
        return (center_x, center_y)

    def get_width_height(self):
        len_x = (self.max_x - self.min_x)
        len_y = (self.max_y - self.min_y)
        return (len_x, len_y)

    def __str__(self):
        list_s ="({x}%2C{y}%3B{x1}%2C{y1})"
        return list_s.format(x=self.min_x, y=self.min_y, x1=self.max_x, y1=self.max_y)
# pag = True
class BaiduKeywordSpider(scrapy.Spider):
    name = "baidu_keyword"
    allowed_domains = ["baidu_keyword.org"]
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(BaiduKeywordSpider,self).__init__(*args,**kwargs)
        # self.js_url = 'http://api.map.baidu.com/?qt=bda&c={city}&wd=体育用品店%24%24%24%24体育用品&wdn=3&ar={x_y}&rn=50&l=18&pn={pag}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk43546&ak=E4805d16520de693a3fe707cdc962045'
        # self.js_url = 'http://api.map.baidu.com/?qt=bda&c={city}&wd=美的空调&wdn=1&ar={x_y}&rn=50&l=18&pn={pag}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk43546&ak=E4805d16520de693a3fe707cdc962045'
        self.js_url = 'http://api.map.baidu.com/?qt=bda&c={city}&wd=眼科医院&wdn=1&ar={x_y}&rn=50&l=18&pn={pag}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk83002&ak=E4805d16520de693a3fe707cdc962045'
        self.city_js = 'http://api.map.baidu.com/?qt=rgc&x={x}&y={y}&dis_poi=100&poi_num=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk83461&ak=E4805d16520de693a3fe707cdc962045'

        self.pag = True
    def start_requests(self):
        sql = '''select province,name,center,areacode from t_xsd_amap where level='district' '''
        for i in db.query(sql):
            x, y = i.get('center').split(',')
            lng, lat = GPSCoordsConvertor.convert_gps_2_mc(float(x), float(y))
            city = i.get('name')
            areacode = i.get('areacode')
            province = i.get('province')
            radius = 50000
            r = Rectangle(lng - radius, lat - radius, lng + radius, lat + radius)
            for i in r.split_rectangle():
                self.pag = True
                pagsiz = 0
                urls = self.js_url.format(city=areacode, x_y=i, pag=pagsiz)
                yield scrapy.Request(urls,meta={'url':urls,'city':city,'province':province,'city_name':areacode,'pagsiz':pagsiz,'x_y':i},dont_filter=True)

    def parse(self, response):
        html = response.body
        ad = GPSCoordsConvertor()
        province = response.meta['province']
        city = response.meta['city_name']
        citys = response.meta['city']
        content = json.loads(html.split('&&')[1][20:-1]).get('content')

        if content:
            areacode = response.meta['city_name']
            x_y = response.meta['x_y']
            pagsiz = response.meta['pagsiz'] + 1
            response.meta['pagsiz'] = pagsiz
            urls = self.js_url.format(city=areacode, x_y=x_y, pag=pagsiz)
            yield scrapy.Request(urls,dont_filter=True,meta=response.meta,callback=self.parse)
        if content != None and len(content) > 0:
            try:
                for x in content[0]:
                    items = {}
                    try:
                        item = {}
                        item['std_tag'] = x.get('std_tag')
                        item['uid'] = x.get('uid')
                        item['tel'] = x.get('tel')
                        item['addr'] = x.get('addr')
                        item['name'] = x.get('name')
                        item['mc_lng'] = x.get('ext').get('detail_info').get('point').get('x')
                        item['mc_lat'] = x.get('ext').get('detail_info').get('point').get('y')
                        lng,lat = ad.convert_mc_2_gps(float(item['mc_lng']),float(item['mc_lat']))
                        item['lng'] = lng
                        item['lat'] = lat
                        item['province'] = province
                        item['city'] = city
                        item['county'] = citys
                        url = self.city_js.format(x=item['mc_lng'],y=item['mc_lat'])
                        yield scrapy.Request(url,meta={'data':item},dont_filter=True,callback=self.address)
                    except:
                        items['std_tag'] = x.get('std_tag')
                        items['uid'] = x.get('uid')
                        items['tel'] = x.get('tel')
                        items['addr'] = x.get('addr')
                        items['name'] = x.get('name')
                        items['province'] = province
                        items['city'] = city
                        items['county'] = citys
                        items['url'] = response.url
                        yield items
            except:
                try:
                    for x in content[1]:
                        items ={}
                        try:
                            item = {}
                            item['std_tag'] = x.get('std_tag')
                            item['uid'] = x.get('uid')
                            item['tel'] = x.get('tel')
                            item['addr'] = x.get('addr')
                            item['name'] = x.get('name')
                            item['mc_lng'] = x.get('ext').get('detail_info').get('point').get('x')
                            item['mc_lat'] = x.get('ext').get('detail_info').get('point').get('y')
                            lng, lat = ad.convert_mc_2_gps(float(item['mc_lng']), float(item['mc_lat']))
                            item['lng'] = lng
                            item['lat'] = lat
                            item['province'] = province
                            item['city'] = city
                            item['county'] = citys
                            url = self.city_js.format(x=item['mc_lng'], y=item['mc_lat'])
                            yield scrapy.Request(url, meta={'data': item}, dont_filter=True, callback=self.address)
                        except:
                            items['std_tag'] = x.get('std_tag')
                            items['uid'] = x.get('uid')
                            items['tel'] = x.get('tel')
                            items['addr'] = x.get('addr')
                            items['name'] = x.get('name')
                            items['province'] = province
                            items['city'] = city
                            items['county'] = citys

                            yield items
                except Exception as e:
                    pass


        else:
            self.pag = False


    def address(self, response):
        item = response.meta.get('data')
        try:
            html = json.loads(response.body.split('&&')[1][20:-1])
            content = html.get('content')
            item['city'] = content.get('address_detail').get('city')
            item['district'] = content.get('address_detail').get('district')
            item['province'] = content.get('address_detail').get('province')
            yield  item


        except Exception as e:
            print e
    
    
    
    
    