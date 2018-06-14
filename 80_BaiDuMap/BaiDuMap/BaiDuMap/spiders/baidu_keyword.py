# -*- coding: utf-8 -*-
import scrapy
import json
import sys, math
import web
import .test_trans_geo
import re
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
        self.js_url = 'http://api.map.baidu.com/?qt=bda&c={city}&wd=眼镜店&wdn=1&ar={x_y}&rn=50&l=18&pn={pag}&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk83002&ak=E4805d16520de693a3fe707cdc962045'
        self.pag = True
    def start_requests(self):
        sql = '''select province,name,center,areacode from t_xsd_amap where level='district' '''
        for i in db.query(sql):
            x, y = i.get('center').split(',')
            lng, lat = baidu_js.test_trans_geo.trans_geo(float(x), float(y))
            city = i.get('name')
            areacode = i.get('areacode')
            province = i.get('province')
            radius = 50000
            r = Rectangle(lng - radius, lat - radius, lng + radius, lat + radius)
            for i in r.split_rectangle():
                self.pag = True
                pagsiz = 0
                while self.pag:
                    urls = self.js_url.format(city=areacode, x_y=i, pag=pagsiz)
                    pagsiz+=1
                    yield scrapy.Request(urls,meta={'url':urls,'city':city,'province':province,'city_name':areacode},dont_filter=True)

    def parse(self, response):
        html = response.body
        zhPattern = u'[\u4e00-\u9fa5]+'
        province = response.meta['province']
        city = response.meta['city_name']
        citys = response.meta['city']
        content = json.loads(html.split('&&')[1][20:-1]).get('content')
        item = {}
        if len(content) == 0:
            self.pag = False
        if len(content) > 0:
            try:
                for x in content[0]:
                    item['std_tag'] = x.get('std_tag')
                    item['uid'] = x.get('uid')
                    item['tel'] = x.get('tel')
                    item['addr'] = x.get('addr')
                    item['name'] = x.get('name')
                    item['lng'] = x.get('ext').get('detail_info').get('point').get('x')
                    item['lat'] = x.get('ext').get('detail_info').get('point').get('y')
                    item['province'] = province
                    item['city'] = city
                    county = x.get('address_norm')
                    item['county'] = citys
                    if county !=None:
                        match = re.findall(zhPattern, county)
                        county = ''.join(match)
                        item['addr1'] = county
                    else: item['addr1'] =''
                    yield item
            except:
                try:
                    for x in content[1]:
                        item['std_tag'] = x.get('std_tag')
                        item['uid'] = x.get('uid')
                        item['tel'] = x.get('tel')
                        item['addr'] = x.get('addr')
                        item['name'] = x.get('name')
                        item['lng'] = x.get('ext').get('detail_info').get('point').get('x')
                        item['lat'] = x.get('ext').get('detail_info').get('point').get('y')
                        item['province'] = province
                        item['city'] = city
                        county = x.get('address_norm')
                        item['county'] = citys
                        if county != None:
                            match = re.findall(zhPattern, county)
                            county = ''.join(match)
                            item['addr1'] = county
                        else:
                            item['addr1'] = ''
                        yield item
                        # print item
                except:
                    pass


        else:
            self.pag = False



    