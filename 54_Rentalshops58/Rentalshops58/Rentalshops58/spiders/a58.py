# -*- coding: utf-8 -*-
import scrapy
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


class A58Spider(scrapy.Spider):
    name = "58"
    allowed_domains = ["58.com"]
    start_urls = [
        'http://www.58.com/changecity.aspx',
        # 'https://app.58.com/api/list/shangpuzushou?tabkey=allcity&action=getListInfo&localname=qd&format=json&page=1'
        # 'https://app.58.com/api/detail/shangpu/29240168165687?v=1&format=json&localname=am&platform=android&version=7.7.2'
    ]

    # def make_requests_from_url(self, url):
    #     return Request(url, callback=self.parse_detail, dont_filter=False,
    #                    meta={'city_code': 'am', 'city_name': '澳门','page_code':'29240168165687'})

    # 通过城市列表获得各城市的列表
    def parse(self, response):
        sel = Selector(response)
        city_list = sel.xpath('//dl[@id="clist"]/dd[not(@class)]/a')
        for city in city_list:
            city_name = city.xpath('text()').extract()
            city_code = re.findall('http://(.*?)\.58\.com', city.xpath('@href').extract()[0])
            if city_code:
                if city_code[0] != 'g':
                    city_code = city_code[0]
                    # print city_code[0], city_name[0]
                    yield Request(
                        url='https://app.58.com/api/list/shangpuzushou?tabkey=allcity&action=getListInfo&localname=%s&format=json&page=' % (
                            city_code),
                        callback=self.parse_list,
                        meta={'city_name': city_name, 'city_code': city_code, 'page_index': 1}, dont_filter=True)
                    # yield Request(urljoin(city,'shangpucz/pn1'),callback=self.parse_rental_shop)

    # 通过城市列表获取详细页信息
    def parse_list(self, response):
        content_json = json.loads(response.body)
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
                                    callback=self.parse_detail, meta=meta, dont_filter=True)
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
                            dont_filter=True)

    # 解析内容页
    def parse_detail(self, response):
        item = Rentalshops58Item()
        content_json = json.loads(response.body)
        # print content_json
        if 'result' in content_json:
            if 'info' in content_json['result']:
                info = content_json['result']['info']
                city_name = response.meta['city_name']
                city_code = response.meta['city_code']
                page_code = response.meta['page_code']
                if city_name:
                    item['city'] = city_name[0]
                for i in info:
                    if 'title_area' in i:
                        item['title'] = i['title_area']['title']
                        item['pubtime'] = i['title_area']['ext'][0]
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
                        if 'mapAddress_area' in i['baseinfo_area']:
                            item['region'] = i['baseinfo_area']['mapAddress_area']['content']
                            if 'action' in i['baseinfo_area']['mapAddress_area']:
                                item['longitude'] = i['baseinfo_area']['mapAddress_area']['action']['lon']
                                item['latitude'] = i['baseinfo_area']['mapAddress_area']['action']['lat']
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
                yield Request(url='http://%s.58.com/shangpu/%sx.shtml' % (city_code, page_code),
                              callback=self.parse_phone, meta={'item': item}, dont_filter=True)

    # 通过page_code和city_code获取联系人电话
    def parse_phone(self, response):
        item = response.meta['item']
        sel = Selector(response)
        phone = sel.xpath('//span[@class="phone"]/text()').extract()
        if phone:
            phone = ''.join(phone).replace('\r', '').replace('\t', '').replace('\n', '').strip()
            item['contact_phone'] = phone
        yield item
