# -*- coding: utf-8 -*-
import datetime
import scrapy
import time

from RentalShops58.items import Rentalshops58Item
from scrapy.selector import Selector
from scrapy import Request
from urlparse import urljoin
from scrapy.log import logger

import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

start_time = time.strftime('%Y-%m-%d', time.localtime())

class A58Spider(scrapy.Spider):
    name = "58"

    allowed_domains = ["58.com"]
    # start_urls = [
    #     'http://www.58.com/changecity.aspx',
        # 'https://app.58.com/api/list/shangpuzushou?tabkey=allcity&action=getListInfo&localname=qd&format=json&page=1'
        # 'https://app.58.com/api/detail/shangpu/29371420528456?v=1&format=json&localname=bj&platform=android&version=7.7.2'
    # ]

    # def make_requests_from_url(self, url):
    #     return Request(url, callback=self.parse_detail, dont_filter=False,
    #                    meta={'city_code': '济宁', 'city_name': ['济宁'], 'page_code': '28430067354823','start_time':start_time})

    def start_requests(self):
        with open('/home/work/wguan/data/58_city_district.csv','r') as f:
            city_region_list = f.readlines()
        #with open('/tmp/58_city_district.csv','r') as f:
         #   city_region_list = f.readlines()
        for city_region in city_region_list:
            city_region = city_region.replace('\r\n','').replace('"','').split(',')
            # print city_region
            #url = 'https://app.58.com/api/list/shangpucz?tabkey=allcity&action=getListInfo&curVer=7.7.2&ct=filter&localname='+city_region[1]+'&os=android&format=json&filterParams={%22filterLocal%22%3A%22'+city_region[3]+'%22}&page=1'
            url = 'https://app.58.com/api/list/shangpucz?tabkey=allcity&action=getListInfo&curVer=7.13.1&ct=filter&appId=1&localname='+city_region[1]+'&os=android&format=json&geotype=baidu&v=1&filterParams={%22filtercate%22:%22shangpu%22,%22filterLocal%22:%22'+city_region[3]+'%22}&page=1'
            print url
            yield Request(url=url,callback=self.parse_list,
                        meta={'city_name': str(city_region[0]), 'city_code': city_region[1], 'page_index': 1,
                              'start_time': start_time,'region':str(city_region[2])}, dont_filter=False)

    # https://app.58.com/api/list/shangpucz?tabkey=allcity&action=getListInfo&curVer=7.7.2&ct=filter&localname=tongcheng&os=android&format=json&filterParams={%22filterLocal%22%3A%22%22}&page=2


    # 通过城市列表获得各城市的列表
    def parse(self, response):

        sel = Selector(response)
        # city_list = sel.xpath('//dl[@id="clist"]/dd[not(@class)]/a')
        city_list = sel.xpath('//dl[@id="clist"]/dd/a')
        for city in city_list:
            city_name = city.xpath('text()').extract()
            city_code = re.findall('http://(.*?)\.58\.com', city.xpath('@href').extract()[0])
            if city_code:
                if city_code[0] != 'g':
                    city_code = city_code[0]
                    # print city_code[0], city_name[0]
                    # if city_code in ['bj','sh','cq','tj']:
                    #     print city_code
                    yield Request(
                        # url='https://app.58.com/api/list/shangpuzushou?tabkey=allcity&action=getListInfo&localname=%s&format=json&page=' % (
                        #     city_code),
                        url='https://app.58.com/api/list/shangpucz?tabkey=allcity&action=getListInfo&localname=%s&format=json&page=' % (
                            city_code),
                        callback=self.parse_list,
                        meta={'city_name': city_name, 'city_code': city_code, 'page_index': 1,
                              'start_time': start_time}, dont_filter=False)
                    # yield Request(urljoin(city,'shangpucz/pn1'),callback=self.parse_rental_shop)

    # 通过城市列表获取详细页信息
    def parse_list(self, response):
        content_json = json.loads(response.body.replace('\\', '、').replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('\f',''))
        meta = response.meta
        if 'result' in content_json:
            if 'getListInfo' in content_json['result']:
                if 'infolist' in content_json['result']['getListInfo']:
                    info_list = content_json['result']['getListInfo']['infolist']
                    for info in info_list:
                        if 'url' in info:
                            url = info['url']
                            page_code = re.findall('shangpu/(\d+)x', url)
                            if page_code:
                                # print page_code
                                meta['page_code'] = page_code[0]
                                yield Request(
                                    url='https://app.58.com/api/detail/shangpu/%s?v=1&format=json'
                                        '&localname=%s&platform=android&version=7.7.2' % (page_code[0],
                                                                                          response.meta['city_code']),
                                    callback=self.parse_detail, meta=meta, dont_filter=False)
                if 'lastPage' in content_json['result']['getListInfo']:
                    if not content_json['result']['getListInfo']['lastPage']:
                        page_index = meta['page_index']
                        page_index += 1
                        # logger.log(1,'city %s page %s' % (meta['city_nam'],page_index))
                        meta['page_index'] = page_index
                        # yield Request(
                        #     url=urljoin(response.url,'&page=%s' % page_index),meta=meta)
                        url_list = response.url
                        url_list_no_pag = re.sub('&page=.*', '', url_list)
                        yield Request(
                            url=url_list_no_pag + '&page=%s' % page_index, callback=self.parse_list, meta=meta,
                            dont_filter=False)

    # 解析内容页
    def parse_detail(self, response):
        item = Rentalshops58Item()
        meta = response.meta
        item['detail_url'] = response.url
        content = response.body
        content = content.replace('\\','').replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('\f','')
        # with open('ttt', 'a') as f:
        #     f.write(str(content))
        try:
            content_json = json.loads(content)
        except Exception,e:
            content = json.dumps(content,ensure_ascii=True)
            content_json = json.loads(content)
            if not isinstance(content_json,dict):
                content_json = content_json.replace('\\','').replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('\f','')
                content_json = json.loads(content_json)
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
                #yield Request(url='http://%s.58.com/shangpu/%sx.shtml' % (city_code, page_code),
                  #            callback=self.parse_phone, meta={'item': item}, dont_filter=False)
                item['contact_phone'] = ''
            others = content_json['result'].get('other')
            if others:
                add_history = others.get('add_history')
                if add_history:
                    item['right_keyword'] = add_history.get('right_keyword')
            yield item

    # 通过page_code和city_code获取联系人电话
    def parse_phone(self, response):
        item = response.meta['item']
        sel = Selector(response)
        phone = sel.xpath('//span[@class="phone"]/text()').extract()
        if phone:
            phone = ''.join(phone).replace('\r', '').replace('\t', '').replace('\n', '').strip()
            item['contact_phone'] = phone

        yield item

    def tranform_pubtime(self,pubtime):
        pubtime =pubtime.replace('发布：','')
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
        else:
            pubtime='20' + pubtime.replace('.', '-')
        return pubtime
    
    
    
    
    
    
    
    
    
    
    