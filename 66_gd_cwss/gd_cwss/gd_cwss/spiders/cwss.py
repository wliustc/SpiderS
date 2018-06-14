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
    allowed_domains = [ "ditu.amap.com"]


    def __init__(self, *args, **kwargs):  # 继承并初始化函数
        super(CwssSpider, self).__init__(*args, **kwargs)  # 继承类
        # 周边店铺url
        self.rim_url = 'http://restapi.amap.com/v3/place/around?key=758878a7e03dac7a5482155ff9daaeda&location={}&output=xml&offset=100&radius=3000&types=动物医院|宠物医院|动物诊所|宠物诊所'
        # 店铺主页url
        self.homepage_url = 'http://ditu.amap.com/detail/{}'
        self.ID_api_url = 'http://restapi.amap.com/v3/place/detail?id={}&output=xml&key=758878a7e03dac7a5482155ff9daaeda'
        self.pet = 0
        self.pets = 0
        # 获取坐标
        self.xy_url = 'http://ditu.amap.com/detail/get/detail?id={}'
        self.start_urls = []


    #连接数据库取出所需字段
    def start_requests(self):
        uid_list = []
        city_id = []
        db = MySQLdb.connect(host='10.15.1.14', user="work", passwd="phkAmwrF", db="pet_cloud", charset="utf8" )
        cursor = db.cursor()
        sql = ("SELECT gaodemap_id,city_id FROM `hospital_base_information` where brand='宠颐生'")
        cursor.execute(sql)
        gaodenmap_id = cursor.fetchall()
        cursor.close()
        db.close()
        for i in gaodenmap_id:
            if i[0] != None:
                uid_list.append(i[0])
                city_id.append(i[1])
        for uuid in zip(uid_list, city_id):
            url = self.homepage_url.format(uuid[0])
            yield scrapy.Request(url, meta={'chong_uid': uuid[0], 'city_id': uuid[1], 'url': url}, dont_filter=True)


    def parse(self, response):  #解析入口url(主页URL)
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            if 'verify' in response.url:
                yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True)
            else:
                html = response.body
                chong_uid = response.meta['chong_uid']
                city_id = response.meta['city_id']
                #使用scrapy自带的选择器进行数据解析
                gather_data = Selector(text=html).xpath('/html/body/comment()').extract()
                if len(gather_data) != 0:
                    gather_re = re.findall('<span pointX="(.*?)" pointY="(.*?)" .*? ', gather_data[0])
                    if len(gather_re) > 0:
                        location = gather_re[0][0] + ',' + gather_re[0][1]
                        zx_name = re.findall('.*? name="(.*?)" .*?', gather_data[0])
                        if len(zx_name) != 0:
                            url = self.rim_url.format(location)
                            yield scrapy.Request(url, meta={'zx_name': zx_name[0], 'chong_uid': chong_uid, 'city_id': city_id}, callback=self.parse_xml,dont_filter=True)
                    else:
                        url = self.ID_api_url.format(chong_uid)
                        yield scrapy.Request(url, meta={'chong_uid': chong_uid, 'city_id': city_id, 'url': url},
                                             dont_filter=True, callback=self.id_api)
                else:
                    url = self.ID_api_url.format(chong_uid)
                    yield scrapy.Request(url, meta={'chong_uid': chong_uid, 'city_id': city_id, 'url': url},
                                         dont_filter=True, callback=self.id_api)

    def id_api(self, response): #解析入口url(api URL)
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.id_api, meta=response.meta, dont_filter=True)
        else:
            html = response.body
            chong_uid = response.meta['chong_uid']
            city_id = response.meta['city_id']
            gather_data = re.findall('<location>(.*?)</location>', html)
            if len(gather_data) > 0:
                location = gather_data[0]
                zx_name = re.findall('<name>(.*?)</name>', html)[0]
                url = self.rim_url.format(location)
                yield scrapy.Request(url, meta={'zx_name': zx_name, 'chong_uid': chong_uid, 'city_id': city_id},
                                     callback=self.parse_xml, dont_filter=True)
            else:
                yield scrapy.Request(response.meta['url'], callback=self.id_api, meta=response.meta, dont_filter=True)

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


    def parse_centre(self, response): #取出这宠物医院的相关评分
        # items = []
        if 'verify' in response.url:

            yield scrapy.Request(response.meta['url'],callback=self.parse_centre, meta=response.meta, dont_filter=True)
        else:
            location = response.meta['location']
            html = response
            if html.xpath('//span[@class="telephone_2"]'):
                telephone = html.xpath('//span[@class="telephone_2"]/text()').extract()[0]
            else:telephone = ''
            if html.xpath('//span[@class="score"]'):
                score = html.xpath('//span[@class="score"]/text()').extract()[0]
            else:score = ''
            if html.xpath('//div[@class="detail_description"]//span[3]'):
                service = html.xpath('//div[@class="detail_description"]//span[3]/text()').extract()[0]
                if re.findall('[\d].[\d]+|[\d]', service):
                    service_re = re.findall('[\d].[\d]+|[\d]', service)[0]
                else:service_re = ''
            else:service_re = ''
            it = GdCwssItem()
            it['service_rating'] = service_re
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

    