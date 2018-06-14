# -*- coding: utf-8 -*-

import sys, math
import web

sys.path.append('../')
import scrapy
from scrapy.http import Request
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 搜索链接
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
        return "(%s,%s;%s,%s)" % (self.min_x, self.min_y, self.max_x, self.max_y)


class BaiduMapSearchLink(scrapy.Spider):
    # name = 'baidumapsearchlinkspider'
    name = 'baiduguangdong'
    total_all = 0

    def __init__(self, code=None, *args, **kwargs):
        super(BaiduMapSearchLink, self).__init__(*args, **kwargs)
        self.code = code

    def start_requests(self):
        # db = web.database(dbn="mysql", host="127.0.0.1", user="root", pw="123456", db="haha", charset="utf8")
        db = web.database(dbn="mysql", host="10.15.1.24", user="writer", pw="hh$writer", db="hillinsight",
                          charset="utf8")
        filedata = []
        if self.code == None:
            sql = '''select province,city from t_decimal_point_baidu_city'''
            res = db.query(sql)
            for r in res:
                province_list = r.get('province') + ':' + r.get('city')
                filedata.append(province_list)
        else:
            prov = self.code
            sql = '''select province,city from t_decimal_point_baidu_citys where city_code='%s' ''' % prov
            res = db.query(sql)
            for r in res:
                province_list = r.get('province') + ':' + r.get('city')
                filedata.append(province_list)
        baseurl = 'http://map.baidu.com/?qt=cur&wd=%s&t=1488192843367&dtype=1'
        search_key_words = ['药店', '医院', '卫生所', '卫生室', '卫生院', '诊所']
        for line in filedata:
            line = line.strip()
            province_citys = line.split(':')
            province = province_citys[0]
            citys_str = province_citys[1]
            citys = citys_str.split(" ")
            for city in citys:
                url = baseurl % (city)
                yield Request(url,
                              meta={'province_name': province, 'city_name': city, 'search_key_words': search_key_words})

    def parse(self, response):
        if response.meta.has_key('retry') and response.meta['retry'] < 0:
            pass
        else:
            json_obj = json.loads(response.body)
            try:
                # 提取城市的code
                print response.url
                city_code = json_obj['content']['code']
                center_geo_str = json_obj['content']['geo'].strip().split('|')[1].split(";")[0]
                center_x = float(center_geo_str.split(',')[0])
                center_y = float(center_geo_str.split(',')[1])
                radius = 500000
                r = Rectangle(center_x - radius, center_y - radius, center_x + radius, center_y + radius)
                povince = response.meta['province_name']
                city = response.meta['city_name']
                search_key_words = response.meta['search_key_words']
                baseurl = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s&c=%s&src=0&wd2=&sug=0&l=12&from=webmap&biz_forward={"scaler":1,"styles":"pl"}&b=%s'
                for keyword in search_key_words:
                    item = {}
                    item['province'] = povince
                    item['city'] = city
                    item['city_code'] = city_code
                    item['keyword'] = keyword
                    url = baseurl % (keyword, city_code, r)
                    yield scrapy.Request(url, meta={'retry': 3, 'item': item, 'rectangle': r}, callback=self.parse2)
            except Exception, e:
                if response.meta.has_key('retry'):
                    yield scrapy.Request(response.url, meta={'retry': response.meta['retry'] - 1}, callback=self.parse,
                                         dont_filter=True)
                else:
                    yield scrapy.Request(response.url, meta={'retry': 3}, callback=self.parse, dont_filter=True)

    def parse2(self, response):
        ci = False
        item = response.meta['item']
        city_code = item['city_code']
        keyword = item['keyword']
        rectg = response.meta['rectangle']
        if response.meta.has_key('retry') and response.meta['retry'] < 0:
            pass
        else:
            try:
                # 判断是否是json 不是意味着可能被封，被强制跳转登陆
                json_obj = json.loads(response.body)
                total_result = int(json_obj['result']['total'])
                page_num = int(math.ceil(float(total_result) / 10))
                # 如果在该区域返回很多记录，那么将该区域进一步切分
                if total_result > 200 and ci == True:
                    baseur0 = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s&c=%s&src=0&wd2=&sug=0&l=12&from=webmap&biz_forward={"scaler":1,"styles":"pl"}&b=%s'
                    rec = str(rectg)
                    x1, y1, x2, y2 = rec.replace(';', ',').replace('(', '').replace(')', '').split(',')
                    r = Rectangle(x1, y1, x2, y2)
                    list_rectg = r.split_rectangle()
                    for r in list_rectg:
                        url = baseur0 % (keyword, city_code, r)
                        yield scrapy.Request(url, meta={'retry': 3, 'item': item, 'rectangle': r}, callback=self.parse2)
                elif total_result > 200:
                    ci = True
                    baseurl = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s&c=%s&src=0&wd2=&sug=0&l=12&from=webmap&biz_forward={"scaler":1,"styles":"pl"}&b=%s'
                    rectg_list = rectg.split_rectangle()
                    for r in rectg_list:
                        url = baseurl % (keyword, city_code, r)
                        yield scrapy.Request(url, meta={'retry': 3, 'item': item, 'rectangle': r}, callback=self.parse2)
                elif total_result > 0 and total_result <= 200:
                    ci = False
                    baseurl = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%s&c=%s&src=0&wd2=&sug=0&l=12&from=webmap&biz_forward={"scaler":1,"styles":"pl"}&b=%s&pn=%s&nn=%s'
                    for pn in range(0, page_num):
                        link = baseurl % (keyword, city_code, rectg, pn, pn * 10)
                        new_item = {}
                        new_item['province'] = item['province']
                        new_item['city'] = item['city']
                        new_item['city_code'] = item['city_code']
                        new_item['keyword'] = item['keyword']
                        new_item['link'] = link
                        # print link
                        # print json.dumps(new_item,ensure_ascii=False)
                        url = link
                        yield scrapy.Request(url, meta={'item': item}, dont_filter=True, callback=self.parse3)
            except Exception as e:
                if response.meta.has_key('retry'):
                    yield scrapy.Request(response.url,
                                         meta={'retry': response.meta['retry'] - 1, 'item': item, 'rectangle': rectg},
                                         callback=self.parse2,
                                         dont_filter=True)
                else:
                    yield scrapy.Request(response.url, meta={'retry': 3, 'item': item, 'rectangle': rectg},
                                         callback=self.parse2, dont_filter=True)

    def parse3(self, response):
        if response.meta.has_key('retry') and response.meta['retry'] < 0:
            pass
        else:
            json_obj = json.loads(response.body)
            try:
                item = response.meta['item']
                contents = json_obj['content']
                for content in contents:
                    item['content'] = content
                    yield item
            except Exception, e:
                if response.meta.has_key('retry'):
                    yield scrapy.Request(response.url, meta={'retry': response.meta['retry'] - 1}, callback=self.parse3,
                                         dont_filter=True)
                else:
                    yield scrapy.Request(response.url, meta={'retry': 3}, callback=self.parse3, dont_filter=True)


