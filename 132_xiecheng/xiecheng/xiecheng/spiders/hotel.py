# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request
from xiecheng.items import XiechengItem

header = {
    'Host': 'hotels.ctrip.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

m_header = {
    'Host': 'm.ctrip.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
}
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class HotelSpider(scrapy.Spider):
    name = "hotel"
    allowed_domains = ["ctrip.com"]
    start_urls = ['http://ctrip.com/']

    def start_requests1(self):
        city_dic = {
            # '1':'beijing',
            # '17':'hangzhou',
            # '2':'shanghai',
            # '12':'nanjing',
            '144': 'jinan',
            # '4':'chongqing',
            # '477':'wuhan',
            # '30':'shenzhen'
        }
        for key, val in city_dic.items():
            for page in [1, 2, 3, 4]:
                url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx?' \
                      'StartTime=2017-11-15&cityId=%s&star=5&page=%s' % (key, page)
                yield Request(url, callback=self.parse, headers=header)

    def start_requests(self):
        inDay = "2017-11-15"
        outDay = "2017-11-16"
        idx = 1
        url = 'https://m.ctrip.com/restapi/soa2/10932/hotel/Product/domestichotelget?'
        #         body ='''{"biz":1,"contrl":3,"facility":0,"faclist":[],"key":"","keytp":0,"pay":0,"querys":[],"couponlist":[]
        # ,"setInfo":{"cityId":"144","inDay":"2017-10-31","outDay":"2017-11-01"},"sort":{"dir":1,"idx":6,"ordby"
        # :0,"size":10},"qbitmap":0,"alliance":{"aid":"4897","sid":"130026","ouid":"","ishybrid":0},"head":{"cid"
        # :"09031051411389841448","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","extension"
        # :[{"name":"pageid","value":"212093"},{"name":"webp","value":0},{"name":"referrer","value":""},{"name"
        # :"protocal","value":"https"}]},"contentType":"json"}'''



        # city_dic = {
        #     '1': 'beijing',
        #     '17': 'hangzhou',
        #     '2': 'shanghai',
        #     '12': 'nanjing',
        #     '144': 'jinan',
        #     '4': 'chongqing',
        #     '477': 'wuhan',
        #     '30': 'shenzhen'
        # }
        data = db.query('select distinct cityId,seo from t_spider_xiecheng_city;')
        query_list = [
            '''"querys":[{"type":2,"val":"5","qtype":2}],''',
            '''"faclist":[9],'''
        ]
        for d in data:
            key = d.get('cityId')
            val = d.get('seo')
            for query in query_list:
                body = '''{"setInfo":{"cityId":"%s","inDay":"%s","outDay":"%s"},
                %s
                "sort":{"dir":1,"idx":%s,"ordby":0,"size":100},
                "head":{"ctok":"","cver":"1.0","lang":"01","sid":"8888",
                {"name":"webp","value":0},{"name":"protocal","value":"https"}]},
                "contentType":"json"}''' % (key, inDay, outDay, query, idx)
                m_header['Referer'] = 'https://m.ctrip.com/webapp/hotel/%s%s/?days=1&atime=%s' % (
                    val, key, inDay.replace('-', ''))
                print m_header['Referer']
                print body
                yield scrapy.Request(url, callback=self.parse, method="POST", body=body,
                                     meta={'body': body, 'idx': idx, 'city_code': key, 'city_name': val,
                                           'query': query}, headers=m_header)

    def parse1(self, response):
        content = json.loads(response.body)
        hotelPositionJSON = content.get('hotelPositionJSON')
        print hotelPositionJSON

        if hotelPositionJSON:
            print len(hotelPositionJSON)
            for hotel in hotelPositionJSON:
                print hotel.get('name')

    def parse(self, response):
        # print response.body
        content = json.loads(response.body)
        htlInfos = content.get('htlInfos')
        if htlInfos:
            idx = response.meta['idx']
            city_code = response.meta['city_code']
            city_name = response.meta['city_name']
            query = response.meta['query']
            print '----------%s-----------%s-----------%s' % (city_name, idx, len(htlInfos))
            for htlInfo in htlInfos:
                name = htlInfo.get('baseInfo').get('name')
                addr = htlInfo.get('baseInfo').get('addr')
                id = htlInfo.get('baseInfo').get('id')
                cityId = htlInfo.get('baseInfo').get('cityId')
                star = htlInfo.get('activeinfo').get('star')
                location = htlInfo.get('baseInfo').get('location')
                url = 'https://m.ctrip.com/restapi/soa2/10933/hotel/Product/hotelintroduction?'
                body = '''{"id":"%s","pgsource":1,"head":{"ctok":"","cver":"1.0",
                "lang":"01","sid":"8888","syscode":"09","extension":[{"name":
                "protocal","value":"https"}]},"contentType":"json"}''' % id
                yield Request(url, callback=self.parse_phone, headers=m_header,
                              method="POST", body=body,
                              meta={'name': name, 'location': location, 'addr': addr,
                                    'cityId': cityId, 'id': id,
                                    'star': star, 'query': response.meta['query'],
                                    'city_code': response.meta['city_code'],
                                    'city_name': response.meta['city_name']})
                # pass
            if len(htlInfos) == 100:
                body = response.meta['body']
                # idx = response.meta['idx']
                body = body.replace('"idx":%s,' % idx, '"idx":%s,' % (int(idx) + 1))
                idx += 1
                url = response.url
                yield scrapy.Request(url, callback=self.parse, method="POST", body=body,
                                     meta={'body': body, 'idx': idx, 'city_code': city_code, 'city_name': city_name,
                                           'query': query}, headers=response.request.headers)

    def parse_phone(self, response):
        content = response.body
        tels = re.findall('telno":"(.*?)"', content)
        if tels:
            tels = ''.join(tels)
        else:
            tels = ''
        item = XiechengItem()
        item['name'] = response.meta['name']
        item['location'] = response.meta['location']
        item['addr'] = response.meta['addr']
        item['cityId'] = response.meta['cityId']
        item['hotel_id'] = response.meta['id']
        item['star'] = response.meta['star']
        item['tels'] = tels
        item['city_code'] = response.meta['city_code']
        item['city_name'] = response.meta['city_name']
        if 'querys' in response.meta['query']:
            type_query = '5星'
        else:
            type_query = '健身房'
        item['type_query'] = type_query
        yield item
