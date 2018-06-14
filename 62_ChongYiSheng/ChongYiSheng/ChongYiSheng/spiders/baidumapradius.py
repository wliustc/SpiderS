# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
from scrapy import Request
from urlparse import urljoin
import re, json
from scrapy.selector import Selector
from ChongYiSheng.items import BaiDuMapRadiusItem
from scrapy.loader.processors import MapCompose
import sys
from mysqlUtil import Mysql

reload(sys)
sys.setdefaultencoding('utf8')

ChongYiSheng_list = [
    ['47', '宠颐生沈阳爱克威分院', '6124971', '3969', '31971fe2143ce6d2583ac806', 41.7895, 123.433,210100],
    ['48', '宠颐生沈阳瑞嘉分院', '23618362', '4331', 'fc244b885df5d9eb3010af51', 41.7721, 123.394,210100],
    ['133', '宠颐生盘锦益友分院', '6007930', '3438', '37c1f5349c2b2d80af31e5a6', 41.1439, 122.09,211100],
    ['139', '宠颐生北京爱之都分院', '4663168', '2082', 'd52831f90c1803a72ffaa7e2', 39.8123, 116.446,110000],
    ['140', '宠颐生北京爱福分院', '16092628', '1503', '53cebd509d13ab612a02e1e5', 39.7847, 116.333,110000],
    ['141', '宠颐生北京爱佳分院', '1772629', '3064', '37d60a4657fdce601e1d11f2', 39.7493, 116.339,110000],
    ['142', '宠颐生成都宠福来分院', '43615785', '3788', 'f41c898455582cb2eaf8532d', 30.6858, 104.034,510100],
    ['143', '萌家人成都九里堤分院', '67985395', '1863', '91c07762ffcab1e7471a32d5', 30.6987, 104.064,510100],
    ['144', '萌家人成都牛市口分院', '27452514', '1875', '43dc0c1f24826608932ca3e7', 30.6419, 104.112,510100],
    ['145', '萌家人成都高新一分院', '77333775', '1879', '52d1b4cf3b26b2598c55ec25', 30.5643, 104.084,510100],
    ['157', '宠颐生北京京冠分院', '36848655', '8582', '680fb703eb4c829c8ab988be', 39.8903, 116.461,110000],
    ['158', '宠颐生北京爱之源分院', '13949683', '8597', '19778600e4f0020fd12dd626', 39.7955, 116.346,110000]
]

ChongYiShengUid_list = ['31971fe2143ce6d2583ac806', 'fc244b885df5d9eb3010af51', '37c1f5349c2b2d80af31e5a6',
                        'd52831f90c1803a72ffaa7e2',
                        '53cebd509d13ab612a02e1e5', '37d60a4657fdce601e1d11f2', 'f41c898455582cb2eaf8532d',
                        '91c07762ffcab1e7471a32d5',
                        '43dc0c1f24826608932ca3e7', '52d1b4cf3b26b2598c55ec25', '680fb703eb4c829c8ab988be',
                        '19778600e4f0020fd12dd626']

item_list = [
    'uid',
    'address',
    'name',
    'lat',
    'lng',
    'telephone',
    'detail_info',
    'distance',
    'detail_url',
    # 'price',
    'service_rating',
    'environment_rating'
]

task_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

keyword_list = ['宠', '宠物', '动物']


class BaiDuMapSpider(scrapy.Spider):
    name = "baidumapradius"
    allowed_domains = ["baidu.com"]

    # start_urls = ['http://dianping.com/']

    def __init__(self, method='yesterday', *args, **kwargs):
        super(BaiDuMapSpider, self).__init__(*args, **kwargs)
        self.method = method
        self.mysql = Mysql('10.15.1.14', 3306, 'work', 'phkAmwrF', 'pet_cloud', 'utf8')

    def start_requests(self):
        sql_sel ='''select id,clinic_name,dianping_id,system_id,baidumap_id,
        lat,lng,city_id from hospital_base_information where lat is not null and lng is not null;
        '''
        ChongYiSheng_list_new = self.mysql.getAll(sql_sel)
        list_all = ChongYiSheng_list
        for informations_list in ChongYiSheng_list_new:
            information_list = {}
            # informations_list = ll.replace('\n', '').split(',')
            if len(informations_list) > 4:
                information_list['id'] = informations_list['id']
                information_list['clinic_name'] = informations_list['clinic_name']
                information_list['dianping_id'] = informations_list['dianping_id']
                information_list['system_id'] = informations_list['system_id']
                information_list['chong_uid'] = informations_list['baidumap_id']
                information_list['lat'] = informations_list['lat']
                information_list['lng'] = informations_list['lng']
                information_list['city_id'] = informations_list['city_id']
                yield Request(
                    url='http://api.map.baidu.com/place/v2/search?query=动物医院$动物诊所$宠物医院$宠物诊所&'
                        'scope=2&output=json&location=%s,%s&radius=3000&page_size=100'
                        '&ak=AfUfBIQUlvvhWT0cANYmzIWCmtuBIsFC' %
                        (information_list['lat'], information_list['lng']),
                    callback=self.parse, meta={'information_list': information_list})

    # http://api.map.baidu.com/place/v2/search?query=动物医院$动物诊所$宠物医院$宠物诊所&scope=2&output=json&location=41.7895,123.433&radius=3000&filter=sort_name:distance|sort_rule:1&ak=AfUfBIQUlvvhWT0cANYmzIWCmtuBIsFC



    def parse(self, response):
        information_list = response.meta['information_list']
        content = response.body
        # print content
        json_content = json.loads(content)
        results = json_content.get('results')
        if results:
            for result in results:
                item = BaiDuMapRadiusItem()
                # print result
                for key, value in result.items():
                    if isinstance(value, dict):
                        for key_inner, value_inner in value.items():
                            if key_inner in item_list:
                                item[key_inner] = value_inner
                    else:
                        if key in item_list:
                            item[key] = value
                item['clinic_name'] = information_list['clinic_name']
                item['chong_uid'] = information_list['chong_uid']
                item['city_id'] = information_list['city_id']
                item['write_time'] = task_time
                # 要求去掉本品牌内医院的过滤
                if item['uid'] not in ChongYiShengUid_list:
                # item['name']
                # if self.is_exist(item['name']):
                    yield item
            # 添加自身医院
            item = BaiDuMapRadiusItem()
            item['uid'] = information_list['chong_uid']
            item['name'] = information_list['clinic_name']
            item['lat'] = information_list['lat']
            item['lng'] = information_list['lng']
            item['telephone'] = ''
            item['distance'] = 0
            item['detail_url'] = 'http://api.map.baidu.com/place/detail?uid=%s&output=html&source=placeapi_v2' % information_list['chong_uid']
            item['service_rating'] = 0
            item['environment_rating'] = 0
            item['clinic_name'] = information_list['clinic_name']
            item['chong_uid'] = information_list['chong_uid']
            item['city_id'] = information_list['city_id']
            item['write_time'] = task_time
            yield item

    def is_exist(self, str_):
        for word in keyword_list:
            if word in str_:
                return True
        return False
















        # uid = result.get('uid')
        # item['uid'] = uid
        # address = result.get('address')
        # item['address'] = address
        # clinic_name = result.get('name')
        # item['clinic_name'] = clinic_name
        # location = result.get('location')
        # lat = ''
        # lng = ''
        # if location:
        #     lat = location.get('lat')
        #     lng = location.get('lng')
        # item['lat'] = lat
        # item['lng'] = lng
        # telephone = location.get('telephone')
        # item['telephone'] = telephone
        # detail_info = result.get('detail_info')
        # distance = ''
        # detail_url = ''
        # price = ''
        # service_rating = ''
        # environment_rating = ''
        # if detail_info:
        #     distance = detail_info.get('distance')
        #     detail_url = detail_info.get('detail_url')
        #     price = detail_info.get('price')
        #     service_rating = detail_info.get('service_rating')
        #     environment_rating = detail_info.get('environment_rating')
        # item['distance'] = distance
        # item['detail_url'] = detail_url
        # item['price'] = price
        # item['service_rating'] = service_rating
        # item['environment_rating'] = environment_rating
        #
        # yield item
