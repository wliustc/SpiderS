# -*- coding: utf-8 -*-
import json
import scrapy
import web
from scrapy import Request
from qianniu.items import QianniuItem
import datetime
import time
import redis
import math

# 一周维权数据
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


class BusinessAdviserSpider(scrapy.Spider):
    name = "all_brand_safequard_legal_right"
    allowed_domains = ["taobao.com"]

    # start_urls = ['http://taobao.com/']

    def __init__(self, crawl_brand='all', *args, **kwargs):
        super(BusinessAdviserSpider, self).__init__(*args, **kwargs)

        self.crawl_brand = crawl_brand
        # self.cookie = ""

    def start_requests(self):
        data = r.hgetall('cookie')
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
                # 获取分类ID
                url = 'https://sycm.taobao.com/qos/common/cate.json?'
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

    def parse(self, response):
        try:
            content = response.body
            # print content
            content_json = json.loads(content)
            code = content_json.get('code')
            # print code
            meta = response.meta
            if str(code) == '0':
                data = content_json.get('data')
                if data:
                    for d in data:
                        if str(d[3]) == '1':
                            cateid = d[1]
                            catename = d[2]
                            # 通过cateid，获取维权分析最近30天的数据
                            month = self.caculate_date()
                            month = month[0].split(',')
                            url = 'https://sycm.taobao.com/qos/claim/analysis/' \
                                  'items.json?dateType=recent30&dateRange=%s|%s' \
                                  '&cateId=%s&cateFlag=1&pageSize=20&orderBy=' \
                                  'rfdSucCnt&order=desc&page=1' % (
                            month[0], month[1], cateid)
                            yield Request(url, callback=self.parse_item, headers=header,
                                          cookies=meta.get('cookie_brand'),
                                          meta={'brand': meta.get('brand'), 'cookie_brand': meta.get('cookie_brand'),
                                                'catename': catename,'cateid':cateid,'month':month}, dont_filter=True)


            else:
                # print content
                try:
                    msg = content_json.get('msg')

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

    def parse_item(self, response):
        meta = response.meta
        item_json = json.loads(response.body)
        data = item_json.get('data')
        if data:
            item = QianniuItem()
            item['content'] = data
            item['meta'] = meta
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield item
            url = response.url
            url_list = url.split('&page=')
            if url_list[1] == '1':
                item_json = json.loads(response.body)
                data = item_json.get('data')
                if data:
                    recordCount = data.get('recordCount')
                    if recordCount:
                        page_num, page_mod = divmod(int(recordCount), 20)
                        # print page_num, page_mod
                        if page_mod > 0:
                            page_num = page_num + 1
                        # print page_num

                        for i in xrange(2, page_num + 1):
                            url_xg = url_list[0] + '&page=%s' % i
                            # print url_xg
                            yield Request(url_xg, callback=self.parse_item, headers=header, cookies=meta.get('cookie_brand'),
                                          meta={'month': meta.get('month'),
                                                'brand': meta.get('brand'),'catename': meta.get('catename'),'cateid':meta.get('cateid')}, dont_filter=True)

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def caculate_date(self, day_num=30):
        date_list = []
        the_date = datetime.datetime.now()
        # date_fmt = datetime.datetime.strptime('日期', '%Y-%m-%d') # 输入日期计算
        yesterday = (the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        before = (the_date - datetime.timedelta(days=day_num)).strftime('%Y-%m-%d')
        date_set = '%s,%s' % (before, yesterday)
        date_list.append(date_set)
        return date_list
