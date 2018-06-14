import sys
for line in sys.stdin:
    print line

# -*- coding: utf-8 -*-
import scrapy
import re
import MySQLdb
from ..items import GdCwssItem
from scrapy.selector import Selector
import time

pd_list = []


class CwssSpider(scrapy.Spider):
    # download_delay = 10
    name = "cwss"
    allowed_domains = ["ditu.amap.com"]

    def __init__(self, *args, **kwargs):  # 继承并初始化函数
        super(CwssSpider, self).__init__(*args, **kwargs)  # 继承类
        # 周边店铺url
        self.rim_url = 'http://restapi.amap.com/v3/place/around?key=758878a7e03dac7a5482155ff9daaeda&location={}&output=xml&offset=100&radius=3000&types=动物医院|宠物医院|动物诊所|宠物诊所'
        # 店铺主页url
        self.homepage_url = 'http://ditu.amap.com/detail/{}'
        self.pet = 0
        self.pets = 0
        # 获取坐标
        self.xy_url = 'http://ditu.amap.com/detail/get/detail?id={}'
        self.start_urls = []

    # 连接数据库取出所需字段


    def start_requests(self):
        uid_list = []
        city_id = []
        db = MySQLdb.connect(host='10.15.1.14', user="work", passwd="phkAmwrF", db="pet_cloud", charset="utf8")
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
            url = self.homepage_url.format(uuid[0])
            yield scrapy.Request(url, meta={'chong_uid': uuid[0], 'city_id': uuid[1], 'url': url}, dont_filter=True)

    def parse(self, response):  # 解析入口url
        if 'verify' in response.url:
            self.pet += 1

            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            html = response.body
            chong_uid = response.meta['chong_uid']
            city_id = response.meta['city_id']
            # 使用scrapy自带的选择器进行数据解析
            gather_data = Selector(text=html).xpath('/html/body/comment()[1]').extract()[0]
            gather_re = re.findall('<span pointX="(.*?)" pointY="(.*?)" .*? name="(.*?)" .*?></span>', gather_data)
            location = gather_re[0][0] + ',' + gather_re[0][1]
            # 拼接高德API
            url = self.rim_url.format(location)
            yield scrapy.Request(url, meta={'zx_name': gather_re[0][2], 'chong_uid': chong_uid, 'city_id': city_id},
                                 callback=self.parse_xml,
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
            url = self.xy_url.format(i[0])
            detail = self.homepage_url.format(i[0])
            yield scrapy.Request(detail, meta={
                'url': detail,
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

    def parse_centre(self, response):  # 取出这宠物医院的相关评分
        # items = []
        if 'verify' in response.url:
            self.pets += 1

            yield scrapy.Request(response.meta['url'], callback=self.parse_centre, meta=response.meta, dont_filter=True)
        else:
            location = response.meta['location']
            html = response
            if html.xpath('//span[@class="telephone_2"]'):
                telephone = html.xpath('//span[@class="telephone_2"]/text()').extract()[0]
            else:
                telephone = ''
            if html.xpath('//span[@class="score"]'):
                score = html.xpath('//span[@class="score"]/text()').extract()[0]
            else:
                score = ''
            if html.xpath('//div[@class="detail_description"]//span[3]'):
                service = html.xpath('//div[@class="detail_description"]//span[3]/text()').extract()[0]
                if re.findall('[\d].[\d]+|[\d]', service):
                    service_re = re.findall('[\d].[\d]+|[\d]', service)[0]
                else:
                    service_re = ''
            else:
                service_re = ''
            it = GdCwssItem()
            it['uid'] = response.meta['id']
            it['telephone'] = telephone
            it['environment_rating'] = score
            it['service_rating'] = service_re
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

