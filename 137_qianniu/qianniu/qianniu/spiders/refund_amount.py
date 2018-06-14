# -*- coding: utf-8 -*-
import json
import scrapy
import web
from scrapy import Request
from qianniu.items import QianniuItem
import datetime
import time
import redis
import re
# 思加图定制生意参谋爬虫

# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

header = {
    'Host': 'sycm.taobao.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'origin': 'https://sycm.taobao.com',
    'Connection': 'keep-alive'
}
r = redis.Redis(host='116.196.71.111', port=52385, db=0)
# begin = '2018-02-07'
# begin = '2018-05-12'
class RefundAmountSpider(scrapy.Spider):
    name = 'refund_amount'
    allowed_domains = ['taobao.com']
    # start_urls = ['http://taobao.com/']

    def __init__(self, select_date='yesterday', crawl_brand='all', *args, **kwargs):
        super(RefundAmountSpider, self).__init__(*args, **kwargs)
        if select_date == 'yesterday':
            self.select_date = self.getYesterday()
        else:
            self.select_date = select_date
        self.crawl_brand = crawl_brand

    def start_requests(self):
        # data = db.query('select cookie from t_spider_sycm_cookie')

        data = r.hgetall('cookie')
        # print data
        # data.pop('staccato')
        # month = (begin, begin)
        month = (self.select_date, self.select_date)
        if data:
            for brand, val in data.items():
                if self.crawl_brand == 'all':
                    pass
                else:
                    crawl_brand_list = self.crawl_brand.split(',')
                    if brand in crawl_brand_list:
                        pass
                    else:
                        continue

                cookie_val_list = val.split('@@@@@@@@')

                if len(cookie_val_list) == 1:
                    cookie_val = cookie_val_list[0]
                else:
                    cookie_val = cookie_val_list[1]
                cookie_list = cookie_val.split(';')
                cookie_dic = {}
                if cookie_list:
                    for cookie in cookie_list:
                        cookies = cookie.split('=')
                        # print cookies
                        if len(cookies) == 2:
                            key = cookies[0]
                            val = cookies[1]
                            cookie_dic[key.strip()] = val.strip()
                cookie_brand = cookie_dic
                cate = '首页整体看板'
                # ﻿https://sycm.taobao.com/portal/coreIndex/getShopMainIndexes.json?dateRange=2018-02-07|2018-02-07&dateType=day&device=0
                url = 'https://sycm.taobao.com/portal/coreIndex/getShopMainIndexes.json?dateRange=%s|%s&dateType=day&device=0' % month
                yield Request(url, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'brand': brand, 'cookie_brand': cookie_brand},
                              dont_filter=True)

    def parse(self, response):
        try:

            content = response.body
            # print content
            content_json = json.loads(content)
            content_json = content_json.get('content')
            code = content_json.get('code')
            print code
            meta = response.meta
            if str(code) == '0':
                item = QianniuItem()
                item['content'] = response.body
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
            else:
                # print content
                try:
                    msg = content_json.get('msg')
                    if 'login' in msg:
                        # hset如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。如果字段已经存在于哈希表中，旧值将被覆盖。
                        r.hset('cookie_logou', meta.get('brand'), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                except Exception, e:
                    print e
                    # print response.body
                    pass
        except:
            print '*******' * 10
            meta = response.meta
            url = response.url
            yield Request(url, callback=self.parse, headers=header, cookies=meta.get('cookie_brand'),
                          meta=meta, dont_filter=True)

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def  time_zhaunhuan(self, start_time, end_time):
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        delta = end - start
        return delta.days, start
