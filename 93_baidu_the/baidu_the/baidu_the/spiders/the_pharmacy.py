# -*- coding: utf-8 -*-
import scrapy
import xlrd
import sys
import json
import random
import web
import re
#百度周边范围jl抓取
reload(sys)
sys.setdefaultencoding('utf8')
def random_KEY():
    key = ['x6PQSfEZcr4xGaBM9VzZSV8rlvSEjhw5',
        '3yiDZf0G8LEaKd7qnNLBp9IPnpCPbRqI',
            'AfUfBIQUlvvhWT0cANYmzIWCmtuBIsFC',
            'Ma9iCTQK9o9Ps9rMjUPnyvNU5lNtWQuI',
            'i4u77Zl3BXUUEdIa5yt6DZwM99kd5Fnn',
            'av4o1sHL8bzueZFI6aT3bKwZw5QSGudq',
           '8njBf12x6RALpUGDd26rjt7IeqdqnWum ',
           'VDOXFBW9pkWCYf6Q9h1nR7vH9E68Sta2',
           '42b8ececa9cd6fe72ae4cddd77c0da5d',
           'MgBALVVeCd8THVBi6gPdvsvG',
           'lQoOHT6YByf7rTYGBEttGX2pWhCtfIQs',
           '4095d36deb0128e339ec5c9e2c533a21',
           'C17de36331be78b32a19cb854e9a2f30',
           'IDvNBsejl9oqMbPF316iKsXR',
           'FbzOyQ4YujPrZsxiQKoB07aB',
           '7OV3ewXplRwrOHTzXIm9gxqG1jGjzMzl',
           '4baaf5b7fe334d5d22562fed0263ad08',
           '8cprupV34TG3GIxu6CnRE5Ua',
           'LXtbxUBZfNBXjuwrAljAiHIo',
           ]
    random_key = random.choice(key)
    return random_key


# x6PQSfEZcr4xGaBM9VzZSV8rlvSEjhw5
def lists():
    the_list = []
    The_pharmacy = xlrd.open_workbook(r'C:\Users\zhangbo\Desktop\20170214.xlsx')
    sheet = The_pharmacy.sheets()[0]
    my_queues = sheet.col_values(1)[1:]
    my_queues1 = sheet.col_values(16)[1:]
    my_queues2 = sheet.col_values(17)[1:]
    for i in zip(my_queues, my_queues1, my_queues2):
        the_list.append(i)
    return the_list

class ThePharmacySpider(scrapy.Spider):
    name = "the_pharmacy"
    allowed_domains = ["the_pharmacy.org"]
    def __init__(self, *args, **kwargs):
        super(ThePharmacySpider,self).__init__(*args, **kwargs)
        self.rim_api = 'http://api.map.baidu.com/place/v2/search?query=%E5%8C%BB%E9%99%A2$%E8%AF%8A%E6%89%80$%E5%8D%AB%E7%94%9F%E7%AB%99$%E8%8D%AF%E5%BA%97&scope=2&output=json&location={}&radius=300&filter=sort_name:distance|sort_rule:1&ak={}'
        self.zhuanhuan = 'http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=json&address={addr}&city={city}&ak={key}'
        self.start_urls = []

    def start_requests(self,the=None):
        if the !=None:
            for i in the:
                name = i[0]
                location = i[2]+','+i[1]
                key = random_KEY()
                url = self.rim_api.format(location,key)
                yield scrapy.Request(url,meta={'name': name, 'location': location},dont_filter=True)
        else:
            key = random_KEY()
            db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
            sql = ''' select * from t_spider_hospital_info '''
            data = db.query(sql)
            for hosp in data:
                city = hosp.get('city')
                hospital = hosp.get('hospital')
                level_name = hosp.get('level_name')
                address = hosp.get('address')
                tel_info = hosp.get('tel_info')
                type_info = hosp.get('type')
                province = hosp.get('province')
                addr = city+hospital
                url = self.zhuanhuan.format(city=province,addr=addr,key=key)
                yield scrapy.Request(url,meta={'city':city,'hospital':hospital,'level_name':level_name,'address':address,'tel_info':tel_info,'type':type_info,'province':province},callback=self.parse1)
    def parse(self, response):
        item = {}
        location = response.meta['location']
        item['content'] = response.meta['name'], json.loads(response.body)
        if item['content'][1]['status'] == 302:
            key = random_KEY()
            url = self.rim_api.format(location,key)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta=response.meta)
        else:
            item['content'] = response.meta['name'], json.loads(response.body)
            print item
            yield item
    def parse1(self, response):
        html = response.body
        item = {}

        if len(re.findall('"status":(.*?),"result"',html)) != 0:
            state = re.findall('"status":(.*?),"result"',html)
            if state[0] == '1':
                pass
            if state[0] !='0' and state[0] !='1':
                key = random_KEY()
                city = response.meta['city']
                hospital = response.meta['hospital']
                addr = city + hospital
                url = self.zhuanhuan.format(city=city, addr=addr, key=key)
                yield scrapy.Request(url, meta=response.meta, dont_filter=True, callback=self.parse1)

            else:
                html = re.findall('({.*?})', html)[0]

                lng = re.findall('"lng":(.*?),', html)[0]
                lat = re.findall('"lat":(.*?)}', html)[0]
                item['city'] = response.meta['city']
                item['hospital'] = response.meta['hospital']
                item['level_name'] = response.meta['level_name']
                item['address'] = response.meta['address']
                item['tel_info'] = response.meta['tel_info']
                item['type_info'] = response.meta['type']
                item['province'] = response.meta['province']
                item['lng'] = lng
                item['lat'] = lat
                print item
                yield item
        elif re.findall('\d+',html)[0]=='302':
            key = random_KEY()
            city = response.meta['city']
            hospital = response.meta['hospital']
            addr = city + hospital
            url = self.zhuanhuan.format(city=city, addr=addr, key=key)
            yield scrapy.Request(url, meta=response.meta, dont_filter=True, callback=self.parse1)



    