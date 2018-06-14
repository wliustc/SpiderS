# -*- coding: utf-8 -*-
import scrapy
import re
import time
import dbManager
import json

_shop_id = re.compile(r'shop/(\d+)/review_more')
_comment_shop_id = re.compile(r'[?&]shop_id=(\d+)')
_comment_topic_id = re.compile(r'review/(\d+)')
_pageno = re.compile(r'[?&]pageno=(\d+)')
_time = re.compile(r'(\d{2}-\d{2}-\d{2} \d{2}:\d{2})')

def _normalize_word(_unicode):
    _unicode = _unicode.strip()
    _unicode = re.sub(r' ', '', _unicode) # 删除空格
    _unicode = re.sub(r'&nbsp;', ' ', _unicode) # 删除空格
    return _unicode


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["dianping.com"]
    def __init__(self, *args, **kwargs):
        self.list_url = 'http://www.dianping.com/shop/{}/review_more?pageno={}'
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        shopids = dbManager.get_shops()
        # shopids = ['24931872']
        self.start_urls = []
        for i in shopids:
            self.start_urls.append(self.list_url.format(i,'1'))
        self.comment_url = 'http://www.dianping.com/review/{}?shop_id={}'

    def parse(self, response):
        comment_list = response.selector.xpath('//a[@mainnoteid]/@mainnoteid').extract()
        shop_id = _shop_id.search(response.url).group(1)
        if comment_list:
            for i in comment_list:
                yield scrapy.Request(self._contact_url(i,shop_id), callback=self._parse_comment)
            page = _pageno.search(response.url).group(1)
            page = str(int(page) +1)
            yield scrapy.Request(self.list_url.format(shop_id,page), callback=self.parse)
        dbManager._set_is_crawl(shop_id)

    def _parse_comment(self,response):
        shop_id = _comment_shop_id.search(response.url).group(1)
        topic_id = _comment_topic_id.search(response.url).group(1)
        users_info = response.selector.xpath("//cite/a[contains(@class,'B')][contains(@href,'member')]")
        content_info = response.xpath("//div[contains(@class,'contList-con')]").xpath("string(.)").extract()
        push_time = response.xpath("//ul[contains(@class,'contList-fn')]/li[1]/text()").extract()
        users_names = users_info.xpath('text()').extract()
        users_id = users_info.xpath('substring-after(@href,"/member/")').extract()
        for idx,uid in enumerate(users_id):
            tmp = {}
            tmp['tid'] = topic_id
            tmp['shop_id'] = shop_id
            tmp['uid'] = uid
            tmp['uname'] = users_names[idx]
            tmp['content'] = json.dumps([content_info[idx]])
            tmp['floor'] = idx
            pushTime = _time.search(push_time[idx]).group(1)
            tmp['push_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(pushTime,'%y-%m-%d %H:%M'))
            tmp['scan_time'] = self.time
            yield tmp

    def _contact_url(self,c_id,shop_id):
        return self.comment_url.format(c_id,shop_id)