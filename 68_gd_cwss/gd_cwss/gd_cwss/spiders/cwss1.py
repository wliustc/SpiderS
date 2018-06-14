# -*- coding: utf-8 -*-
import scrapy
import re
import MySQLdb
from ..items import GdCwssItem
import time
import random
pd_list = []
def random_KEY():
    key = [ 'd3a1add365ef104fcfe6fd01a4131b3c', '626bbdcc1127a60818828c40a5a5c2a3',
            '8d9cba3557fc264c01d2546c4f52afa7', '758878a7e03dac7a5482155ff9daaeda',
            'dc0311f951cc0639b97277d931f326c0', '6b84d51c8195c3827ef02d9fa783eb1f',
            'fad0cc4413f73ef6a31ada1f095de971', '1d503ace4b1c2833b76bd02b4bedcd2d']
    random_key = random.choice(key)
    return random_key


class CwssSpider(scrapy.Spider):
    # download_delay = 1
    name = "cwss1"
    allowed_domains = ["cwss.org", "ditu.amap"]

    def __init__(self, *args, **kwargs):  # 继承并初始化函数
        super(CwssSpider, self).__init__(*args, **kwargs)  # 继承类
        # 周边店铺url
        self.rim_url = 'http://restapi.amap.com/v3/place/around?key={}&location={}&output=xml&offset=100&radius=3000&types=动物医院|宠物医院|动物诊所|宠物诊所'
        # 店铺信息url
        self.homepage_url = 'http://restapi.amap.com/v3/place/detail?id={}&output=xml&key={}'
        #店铺主页url
        self.sy_url = 'http://ditu.amap.com/detail/{}'
        self.start_urls = []
    #连接数据库取出所需字段
    def start_requests(self):
        uid_list = []
        city_id = []
        db = MySQLdb.connect(host='10.15.1.14', user="work", passwd="phkAmwrF", db="pet_cloud", charset="utf8" )
        cursor = db.cursor()
        sql = ("SELECT * FROM `hospital_base_information` where brand='宠颐生'")
        cursor.execute(sql)
        gaodenmap_id = cursor.fetchall()
        cursor.close()
        db.close()
        for i in gaodenmap_id:
            if i[-1] != None:
                uid_list.append(i[-1])
                city_id.append(i[-9])
        print uid_list
        for uuid in zip(uid_list, city_id):
            key = random_KEY()
            url = self.homepage_url.format(uuid[0], key)
            yield scrapy.Request(url, meta={'chong_uid': uuid[0], 'city_id': uuid[1]}, dont_filter=True)

    def parse(self, response):  #解析入口url
        html = response.body
        chong_uid = response.meta['chong_uid']
        city_id = response.meta['city_id']
        gather_data = re.findall('<location>(.*?)</location>', html)
        location = gather_data[0]
        zx_name = re.findall('<name>(.*?)</name>', html)
        #拼接高德API
        key = random_KEY()
        url = self.rim_url.format(key, location)
        yield scrapy.Request(url, meta={'zx_name': zx_name, 'chong_uid': chong_uid, 'city_id': city_id}, callback=self.parse_xml,
                             dont_filter=True)

    # 从高德API入口获取所需数据
    def parse_xml(self, response):

        zx_name = response.meta['zx_name']
        chong_uid = response.meta['chong_uid']
        city_id = response.meta['city_id']
        html = response.body
        uuid = re.findall('<id>(.*?)</id>', html)
        distance = re.findall('<distance>(.*?)</distance>', html)
        name = re.findall('<name>(.*?)</name>', html)
        address = re.findall('<address>(.*?)</address>', html)
        location = re.findall('<location>(.*?)</location>', html)
        data = []
        for x in zip(name, address, location):
            data.append(x)
        for i in zip(uuid, distance, data):
            key = random_KEY()
            url = self.homepage_url.format(i[0], key)
            detail = self.sy_url.format(i[0])
            yield scrapy.Request(url, meta={
                'id': i[0],
                'name': i[2][0],
                'address': i[2][1],
                'location': i[2][2],
                'distance': i[1],
                'zx_name': zx_name,
                'detail_url': detail,
                'chong_uid': chong_uid,
                'city_id': city_id
            }, callback=self.parse_centre, dont_filter=True)


    def parse_centre(self, response): #取出这宠物医院的相关评分
        it = GdCwssItem()
        location = response.meta['location']
        html = response.body
        telephone = re.findall('<tel>(.*?)</tel>', html)
        score = re.findall('<rating>(.*?)</rating>', html)
        if len(telephone) == 0 or len(score) ==0:
            yield it
        else:
            if len(telephone[0]) != 0:
                telephone = telephone[0]
            else: telephone = ''
            if len(score[0]) != 0:
                score = score[0]
            else:score = ''
            it['uid'] = response.meta['id']
            it['telephone'] = telephone
            it['environment_rating'] = score
            it['distance'] = response.meta['distance']
            it['clinic_name'] = response.meta['zx_name']
            it['detail_url'] = response.meta['detail_url']
            it['lat'] = location.split(',')[0]
            it['lng'] = location.split(',')[1]
            it['name'] = response.meta['name']
            it['address'] = response.meta['address']
            it['chong_uid'] = response.meta['chong_uid']
            it['city_id'] = response.meta['city_id']
            it['write_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield it