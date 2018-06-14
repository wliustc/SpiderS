# -*- coding: utf-8 -*-
import scrapy
import re
import time
from boqi_shop.items import BoqiShopItem

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/59.0.3071.115 Safari/537.36'
}

cookies = {
    'userSessId': '89fbde9180206d2e392f9f36ed6c69d0',
    'PHPSESSID': '89fbde9180206d2e392f9f36ed6c69d0',
    '__jsluid': '5000dd0114346f5785d72f8e0ed34999',
    'cityId': '11',
    'UM_distinctid': '15ffd437e7a9ac-044452b4675fe-17386d57-1aeaa0-15ffd437e7b9b6',
    'cityName': '%E5%8C%97%E4%BA%AC; CNZZDATA1265019045=1466115468-1511781716-%7C1512458782',
    'NTKF_T2D_CLIENTID': 'guest1ACD1BDD-6793-160E-7A88-FD438054CBAE',
    'nTalk_CACHE_DATA': '{uid:kf_9481_ISME9754_guest1ACD1BDD-6793-16,tid:1512461734466517}'
}

cookies2 = {
    'PHPSESSID':'89fbde9180206d2e392f9f36ed6c69d0',
    '__jsluid':'5000dd0114346f5785d72f8e0ed34999',
    'userSessId':'89fbde9180206d2e392f9f36ed6c69d0',
    'cityId':'11',
    'UM_distinctid':'15ffd437e7a9ac-044452b4675fe-17386d57-1aeaa0-15ffd437e7b9b6',
    '_jzqc':'1',
    'NTKF_T2D_CLIENTID':'guest1ACD1BDD-6793-160E-7A88-FD438054CBAE',
    'cityName':'%E5%8C%97%E4%BA%AC',
    'CNZZDATA1265019045':'1466115468-1511781716-%7C1512983835',
    'viewedids':'8890%2C8890',
    '_qzja':'1.312373434.1512468424515.1512468424516.1512985651460.1512468618469.1512985651460..0.0.3.2',
    '_qzjc':'1',
    '_qzjto':'1.1.0',
    '_jzqa':'1.880723968230560900.1512468424.1512468424.1512985651.2',
    '_jzqckmp':'1',
    '_qzjb':'1.1512985651460.1.0.0.0',
    'nTalk_CACHE_DATA':'{uid:kf_9481_ISME9754_guest1ACD1BDD-6793-16,tid:1512985651988566}',
    '_jzqb':'1.1.10.1512985651.1'
}

class Boqi_Spider(scrapy.Spider):

    name = 'boqi_spider'

    def start_requests(self):
        url_list = ['http://shop.boqii.com/dog/', 'http://shop.boqii.com/cat/']
        for url in url_list:
            yield scrapy.Request(url, headers=headers, callback=self.category_parse, dont_filter=True, cookies=cookies)

    def category_parse(self, response):
        content = response.body
        pattern1 = re.search('<div class="channel_left_menu">([\s\S]*?)</div>', content)
        cate_con = pattern1.group(1)
        pattern2 = re.compile('<a target="_blank" href="(.*?)"[\s\S]*?>([\s\S]*?)<')
        cate_list = re.findall(pattern2, cate_con)
        for cate in cate_list:
            category1_name = cate[1].strip()
            url = cate[0]
            yield scrapy.Request(url, callback=self.category2_parse, headers=headers,
                                 meta={'category1_name': category1_name}, dont_filter=True, cookies=cookies)

    def category2_parse(self, response):
        content = response.body
        # print content
        category1_name = response.meta['category1_name']
        # pat = '<span>'+category1_name+'</span>[\s\S]*?<div class="goodsCateSub">([\s\S]*?)'
        pattern1 = re.search('<span>'+category1_name+'</span>[\s\S]*?<div class="goodsCateSub">([\s\S]*?)</div>', content)
        cate2_con = pattern1.group(1)
        # print cate2_con
        pattern2 = re.compile('<a href="(.*?)" title="([\s\S]*?)"')
        cate2_list = re.findall(pattern2, cate2_con)
        # print cate2_list
        for cate2 in cate2_list:
            category2_name = cate2[1]
            url = cate2[0]
            yield scrapy.Request(url, headers=headers, callback=self.list_parse,
                                 meta={'category1_name': category1_name, 'category2_name': category2_name},
                                 dont_filter=True, cookies=cookies)

    def list_parse(self, response):
        content = response.body
        category1_name = response.meta['category1_name']
        category2_name = response.meta['category2_name']
        pattern1 = re.compile('<div class="product_list_container">[\s\S]*?<a href="(.*?)"')
        url_list = re.findall(pattern1, content)
        for url in url_list:
            yield scrapy.Request(url, headers=headers, callback=self.detail_parse,
                                 meta={'category1_name': category1_name, 'category2_name': category2_name}, dont_filter=
                                 True, cookies=cookies2)
        pattern2 = re.search('< </a><a href="(.*?)" title="下一页" class="next_page"', content)
        if pattern2:
            url_next = pattern2.group(1)
            yield scrapy.Request(url_next, headers=headers, callback=self.list_parse,
                                 meta={'category1_name': category1_name, 'category2_name': category2_name},
                                 dont_filter=True, cookies=cookies)

    def detail_parse(self, response):
        content = response.body
        items = BoqiShopItem()
        category1_name = response.meta['category1_name']
        category2_name = response.meta['category2_name']
        pattern1 = re.search('id="gePrice" value="(.*?)"', content)
        items['price'] = pattern1.group(1)
        pattern2 = re.search('已　　售：</dt>[\s\S]*?">(.*?)件', content)
        items['sales_num'] = pattern2.group(1)
        pattern3 = re.search('所属品牌：</dt>[\s\S]*?">([\s\S]*?)<', content)
        items['brand'] = pattern3.group(1)
        pattern4 = re.search('商品编号：</dt>[\s\S]*?>(.*?)<', content)
        items['goods_id'] = pattern4.group(1)
        items['category1_name'] = category1_name
        items['category2_name'] = category2_name
        items['url'] = response.url
        items['collect_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        yield items

    
    
    