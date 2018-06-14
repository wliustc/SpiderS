# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time

import scrapy
import web
from scrapy import Request

from RentalShops58.items import Rentalshops58Item

reload(sys)
sys.setdefaultencoding('utf8')
'''
使用
'''
start_time = time.strftime('%Y-%m-%d', time.localtime())

db = web.database(dbn='mysql', db='58tongcheng', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

header = {
    'Host': 'apphouse.58.com',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Letv X500 Build/DBXCNOP5902605181S)',
    'brand': 'Letv',
    'ua': 'Letv X500',
    'platform': 'android',
    'os': 'android',
    'owner': 'baidu',
    'deviceid': 'b066c2741057e132',
    '58ua': '58app',
    'version': '6.3.6.0',
    'osv': '6.0'
}


# 修改了获取端口，从老版app上获取

class E58Spider(scrapy.Spider):
    name = "e58"

    allowed_domains = ["58.com"]

    def start_requests(self):

        city_region_list = db.query(
            'select distinct city_name,city_id,shangquan_pinyin,shangquan from 58_city_district')
        for city_region in city_region_list:
            # city_pinyin = city_region.get('city_pinyin')
            shangquan_pinyin = city_region.get('shangquan_pinyin')
            if shangquan_pinyin:
                url = 'https://app.58.com/api/list/shangpucz/?tabkey=allcity&action=getListInfo&isNeedAd=1&curVer=7.14.1&ct=filter&os=ios&filterparams={%22filtercate%22:%22shangpucz%22}&appId=3&localname='+shangquan_pinyin+'&page=1'
                yield Request(url=url, callback=self.parse_list,
                              meta={'city_name': str(city_region.get('city_name')), 'city_code': city_region.get('city_id'),
                                    'page_index': 1,
                                    'start_time': start_time, 'region': str(city_region.get('shangquan'))},
                              dont_filter=False)


        # url = 'https://apphouse.58.com/api/list/shangpucz/?tabkey=allcity&action=getListInfo&isNeedAd=1&curVer=7.14.1&ct=filter&os=ios&filterparams={%22filtercate%22:%22shangpucz%22}&appId=3&localname=bj&page=1'
        # yield Request(url, callback=self.parse_list,
        #               meta={'city_name': '北京', 'city_code': 1, 'page_index': 1,
        #                     'start_time': start_time, 'region': 'cbd', 'city_pinyin': 'bj'})

    # 通过城市列表获取详细页信息
    def parse_list(self, response):
        content_json = json.loads(
            response.body.replace('\\', '、').replace('\t', '').replace('\r', '').replace('\n', '').replace('\b',
                                                                                                           '').replace(
                '\f', ''))
        meta = response.meta
        if 'result' in content_json:
            if 'getListInfo' in content_json['result']:
                if 'infolist' in content_json['result']['getListInfo']:
                    info_list = content_json['result']['getListInfo']['infolist']
                    if info_list:
                        for info in info_list:
                            if 'url' in info:
                                url = info['url']
                                # print url
                                page_code = re.findall('shangpu/(\d+)x', url)
                                if page_code:
                                    # print page_code
                                    meta['page_code'] = page_code[0]
                                    meta['date'] = self.tranform_pubtime(info['date'])
                                    # print
                                    url = 'https://apphouse.58.com/api/detail/shangpu/%s?format=json&localname=bj&platform=android&version=6.3.6.0' % \
                                          page_code[0]

                                    yield Request(url, callback=self.parse_detail, meta=meta, dont_filter=False,
                                                  headers=header
                                                  )

                        url = response.url
                        url = url.split('&page=')
                        page_index = meta.get('page_index')
                        page_index = page_index + 1
                        url = url[0] + '&page=%s' % page_index
                        print url
                        meta['page_index'] = page_index
                        yield Request(url, callback=self.parse_list, meta=meta)

    # 解析内容页
    def parse_detail(self, response):
        # print response.body
        print '-----------------------------------------------'
        item = Rentalshops58Item()
        meta = response.meta

        item['detail_url'] = response.url
        content = response.body
        content = content.replace('\\', '').replace('\t', '').replace('\r', '').replace('\n', '').replace('\b',
                                                                                                          '').replace(
            '\f', '')
        # with open('ttt', 'a') as f:
        #     f.write(str(content))
        try:
            content_json = json.loads(content)
        except Exception, e:
            content = json.dumps(content, ensure_ascii=True)
            content_json = json.loads(content)
            if not isinstance(content_json, dict):
                try:
                    content_json = json.loads(content_json)
                except:
                    with open('error_1', 'a') as f:
                        f.writelines(content_json)
        # print content_json
        item['response_body'] = json.dumps(content_json)
        if 'result' in content_json:
            if 'info' in content_json['result']:
                info = content_json['result']['info']
                city_name = response.meta['city_name']
                city_code = response.meta['city_code']
                page_code = response.meta['page_code']
                start_time = response.meta['start_time']
                item['tasktime'] = start_time
                # if city_name:
                item['city'] = city_name
                for i in info:
                    if 'title_area' in i:
                        item['title'] = i['title_area']['title']
                        pubtime = i['title_area']['ext'][0]
                        item['pubtime'] = self.tranform_pubtime(pubtime)
                        item['rent'] = i['title_area']['price']['p'] + i['title_area']['price']['u']
                    if 'desc_area' in i:
                        item['describe'] = i['desc_area']['text'].replace('<br>', '')
                    if 'baseinfo_area' in i:
                        if 'base_area' in i['baseinfo_area']:
                            if 'items' in i['baseinfo_area']['base_area']:
                                base_items = i['baseinfo_area']['base_area']['items']
                                for base_item in base_items:
                                    base_item = base_item[0]
                                    # print base_item
                                    # print base_item['title']
                                    if '面积'.encode('utf8') == base_item['title']:
                                        item['rentable_area'] = base_item['content']
                                    if '类型'.encode('utf8') == base_item['title']:
                                        item['property_type'] = base_item['content']
                                    if '临近'.encode('utf8') == base_item['title']:
                                        item['approach'] = base_item['content']
                        region = ''
                        if 'mapAddress_area' in i['baseinfo_area']:
                            region = i['baseinfo_area']['mapAddress_area']['content']

                            if 'action' in i['baseinfo_area']['mapAddress_area']:
                                item['longitude'] = i['baseinfo_area']['mapAddress_area']['action']['lon']
                                item['latitude'] = i['baseinfo_area']['mapAddress_area']['action']['lat']
                        if not region:
                            region = meta['region']
                        item['region'] = region
                    if 'userinfo_area' in i:
                        item['contact_name'] = i['userinfo_area']['username']
                    if 'image_area' in i:
                        if 'image_list' in i['image_area']:
                            image_l = []
                            for image_list in i['image_area']['image_list']:
                                # print image_list
                                image = str(image_list).split(',')
                                if image:
                                    image_l.append(image[-1])
                            item['pictures'] = image_l
                # yield Request(url='http://%s.58.com/shangpu/%sx.shtml' % (city_code, page_code),
                #               callback=self.parse_phone, meta={'item': item}, dont_filter=False)
                item['contact_phone'] = ''
            others = content_json['result'].get('other')
            if others:
                add_history = others.get('add_history')
                if add_history:
                    item['right_keyword'] = add_history.get('right_keyword')
            yield item

    def tranform_pubtime(self, pubtime):
        pubtime = pubtime.replace('发布：', '')
        if '天前' in pubtime:
            pubtime = int(pubtime.replace('天前', ''))
            pubtime = datetime.datetime.now() + datetime.timedelta(days=-pubtime)
            pubtime = pubtime.strftime('%Y-%m-%d')
        elif '小时前' in pubtime:
            pubtime = int(pubtime.replace('小时前', ''))
            pubtime = datetime.datetime.now() + datetime.timedelta(hours=-pubtime)
            pubtime = pubtime.strftime('%Y-%m-%d')
        elif '分钟前' in pubtime:
            pubtime = int(pubtime.replace('分钟前', ''))
            pubtime = datetime.datetime.now() + datetime.timedelta(minutes=-pubtime)
            pubtime = pubtime.strftime('%Y-%m-%d')
        elif '今天' in pubtime:
            pubtime = datetime.datetime.now().strftime('%Y-%m-%d')
        elif len(pubtime)==5:
            pubtime = datetime.datetime.now().strftime('%Y')+'-' + pubtime.replace('.', '-')
        else:
            pubtime = '20' + pubtime.replace('.', '-')
        return pubtime

    