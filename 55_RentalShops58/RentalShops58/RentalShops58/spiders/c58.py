# -*- coding: utf-8 -*-
import datetime
import scrapy
import time

from RentalShops58.items import RentalshopsC58Item
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
    name = "c58"

    allowed_domains = ["58.com"]

    # start_urls = [
    #     'http://www.58.com/changcity.aspx',
    # 'https://app.58.com/api/list/shangpuzushou?tabkey=allcity&action=getListInfo&localname=qd&format=json&page=1'
    # 'https://app.58.com/api/detail/shangpu/27004461771323?v=1&format=json&localname=bj&platform=android&version=7.7.2'
    # ]

    # def make_requests_from_url(self, url):
    #     return Request(url, callback=self.parse_detail, dont_filter=False,
    #                    meta={'city_code': '济宁', 'city_name': ['济宁'], 'page_code': '28430067354823','start_time':start_time,'region':'111'})
    #
    def start_requests(self):
        with open('/home/work/wguan/data/58_city_district.csv', 'r') as f:
            city_region_list = f.readlines()
        for city_region in city_region_list:
            city_region = city_region.replace('\r\n', '').replace('"', '').split(',')
            print city_region
            url = 'https://app.58.com/api/list/shangpucz?tabkey=allcity&action=getListInfo&curVer=7.7.2&ct=filter&localname=' + \
                  city_region[1] + '&os=android&format=json&filterParams={%22filterLocal%22%3A%22' + city_region[
                      3] + '%22}&page=1'
            print url
            yield Request(url=url, callback=self.parse_list,
                          meta={'city_name': str(city_region[0]), 'city_code': city_region[1], 'page_index': 1,
                                'start_time': start_time, 'region': str(city_region[2])}, dont_filter=False)

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
        content_json = json.loads(
            response.body.replace('\\', '、').replace('\t', '').replace('\r', '').replace('\n', '').replace('\b',
                                                                                                           '').replace(
                '\f', ''))
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
        item = RentalshopsC58Item()
        item['city_name'] = response.meta['city_name']
        item['city_code'] = response.meta['city_code']
        item['region'] = response.meta['region']
        item['start_time'] = response.meta['start_time']
        item['body_content'] = response.body.replace('\\', '').replace('\t', '').replace('\r', '').replace('\n', '').replace(
            '\b', '').replace('\f', '').replace(' ','')
        item['detail_url'] = response.url
        yield item

    