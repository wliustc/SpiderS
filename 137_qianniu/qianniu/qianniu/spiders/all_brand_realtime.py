# -*- coding: utf-8 -*-
import json
import scrapy
import web
from scrapy import Request
from qianniu.items import QianniuItem
import datetime
import time
import redis

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

dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))


class BusinessAdviserSpider(scrapy.Spider):
    name = "all_brand_realtime"
    allowed_domains = ["taobao.com"]

    # start_urls = ['http://taobao.com/']

    def __init__(self, select_date='yesterday', crawl_brand='all', *args, **kwargs):
        super(BusinessAdviserSpider, self).__init__(*args, **kwargs)
        if select_date == 'yesterday':
            self.select_date = self.getYesterday()
        else:
            self.select_date = select_date
        self.crawl_brand = crawl_brand
        # self.cookie = ""

    def start_requests(self):
        # data = db.query('select cookie from t_spider_sycm_cookie')
        r = redis.Redis(host='116.196.71.111', port=52385, db=0)
        data = r.hgetall('cookie')
        # print data
        # data.pop('staccato')
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

                # cate = '流量构成'
                # 获取活动ID
                url = 'https://sycm.taobao.com/datawar/v3/activity/actList/getOngoingActivity.json'
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

                # 实时流量
                url = 'https://sycm.taobao.com/flow/new/live/guide/trend/overview.json?device=0&type=1'
                yield Request(url, callback=self.parse_realtime_flow, headers=header,
                              cookies=cookie_brand,
                              meta={'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

                # 实时概况
                url = 'https://sycm.taobao.com/ipoll/live/refreshRest.json?appId=sycm&topic=tb_user_day_flow'
                yield Request(url, callback=self.parse_realtime_overview_flow, headers=header, cookies=cookie_brand,
                              meta={'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

                # 实时榜单
                url = 'https://sycm.taobao.com/ipoll/live/rank/getHotOfferRank.json?device=0&index=gmv&keywords=null&limit=10&page=1'
                yield Request(url, callback=self.parse_realtime_item_top, headers=header, cookies=cookie_brand,
                              meta={'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

    def parse(self, response):
        content = response.body
        print content
        content_json = json.loads(content)
        code = content_json.get('code')
        # print code
        meta = response.meta
        brand = meta.get('brand')
        cookie_brand = meta.get('cookie_brand')

        if str(code) == '0':
            data = content_json.get('data')
            if data:
                for d in data:
                    activityId = d.get('activityId')
                    # 活动期kpi实时数据
                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/live.json?&dateType=today&activityId=' + str(
                        activityId)
                    yield Request(url, callback=self.parse_act_detail_kpi_core_live, headers=header,
                                  cookies=cookie_brand,
                                  meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d}, dont_filter=True)


                    # 预热期推广引流的数据--无线端
                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/live.json?dateRange=%s|%s&dateType=today&order=desc&orderBy=uv&device=2&activityId=%s' % (
                    self.getYesterday(), self.getYesterday(), activityId)
                    yield Request(url, callback=self.parse_realtime_popularize, headers=header, cookies=cookie_brand,
                                  meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d, 'device': '无线端'},
                                  dont_filter=True)
                    # 预热期pc端的
                    # ﻿https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/live.json?dateRange=2018-05-24%7C2018-05-24&dateType=today&order=desc&orderBy=uv&device=1&activityId=420150&_=1527216826622&token=f4c414a8a
                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/live.json?dateRange=%s|%s&dateType=today&order=desc&orderBy=uv&device=1&activityId=%s' % (
                    self.getYesterday(), self.getYesterday(), activityId)
                    yield Request(url, callback=self.parse_realtime_popularize, headers=header, cookies=cookie_brand,
                                  meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d, 'device': 'PC端'},
                                  dont_filter=True)

                    actStatus = d.get('actStatus')
                    if str(actStatus) == '2':
                        # 活动期
                        # 活动期商品库存数据
                        url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=%s&itemType=0&device=1&keyword=&pageSize=10&page=1&order=desc&orderBy=itemPayAmt' % str(
                            activityId)
                        yield Request(url, callback=self.parse_act_item_live, headers=header,
                                      cookies=cookie_brand,
                                      meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d}, dont_filter=True)

                        url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=%s&itemType=0&device=1&keyword=&pageSize=20&page=1&order=desc&orderBy=itemPayAmt' % str(
                            activityId)
                        yield Request(url, callback=self.parse_data, headers=header,
                                      cookies=cookie_brand,
                                      meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d,'activityId':activityId, 'orderby': 'itemPayAmt'}, dont_filter=True)

                        indexcode_list = ['actItmPayAmt', 'payAmt', 'payCnt', 'actItmPayCnt', 'payByrCnt',
                                          'actItmPayByrCnt', 'uv']
                        for indexcode in indexcode_list:
                            url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=%s&dateType=today&dateRange=%s|%s&indexCode=%s' % (
                            activityId, dt, dt, indexcode)
                            yield Request(url, callback=self.parse_act_detail_hour_live, headers=header,
                                          cookies=cookie_brand,
                                          meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d,
                                                'indexcode': indexcode}, dont_filter=True)
                    elif str(actStatus) == '1':
                        # 预热期
                        # 预热期商品库存数据
                        # https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=372134&itemType=0&device=1&keyword=&pageSize=10&page=1&order=desc&orderBy=cartCnt&_=1525855353610&token=30cf5cd92
                        url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=%s&itemType=0&device=1&keyword=&pageSize=10&page=1&order=desc&orderBy=cartCnt' % str(
                            activityId)
                        yield Request(url, callback=self.parse_act_item_live, headers=header,
                                      cookies=cookie_brand,
                                      meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d}, dont_filter=True)

                        url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=%s&itemType=0&device=1&keyword=&pageSize=20&page=1&order=desc&orderBy=cartCnt' % str(
                            activityId)
                        yield Request(url, callback=self.parse_data, headers=header,
                                      cookies=cookie_brand,
                                      meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d,'activityId':activityId, 'orderby':'cartCnt'}, dont_filter=True)

                        indexcode_list = ['preheatCartByrCnt', 'preheatCartItmCnt', 'preCltByrCnt', 'preheatCltItmCnt',
                                          'preheatUv']
                        for indexcode in indexcode_list:
                            url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=%s&dateType=today&dateRange=%s|%s&indexCode=%s' % (
                                activityId, dt, dt, indexcode)
                            yield Request(url, callback=self.parse_act_detail_hour_live, headers=header,
                                          cookies=cookie_brand,
                                          meta={'brand': brand, 'cookie_brand': cookie_brand, 'd': d,
                                                'indexcode': indexcode}, dont_filter=True)

        else:
            try:
                msg = content_json.get('msg')
                if 'login' not in msg:
                    meta = response.meta
                    url = response.url
                    yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                                  meta=meta, dont_filter=True)
            except Exception:
                # print e
                # print response.body
                pass

    def parse_act_detail_kpi_core_live(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_act_detail_kpi_core_live'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
    def parse_data(self, response):

        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_data'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
                #recordCount = data.get('data')
                #if recordCount:
                #    count = recordCount.get('recordCount')
                #    if count:
                #        num = int(round(float(count / 20)))
                for i in xrange(2, 4):
                    url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListLive.json?activityId=%s&itemType=0&device=1&keyword=&pageSize=20&page=%s&order=desc&orderBy=%s' % (str(
                        meta.get('activityId')), str(i), meta.get('orderby'))
                    yield Request(url, callback=self.parse_act_item, headers=header,
                                  cookies=meta.get('cookie_brand'),
                                  meta={'brand': meta.get('brand'), 'cookie_brand': meta.get('cookie_brand'), 'd': meta.get('d'),
                                        'activityId': meta.get('activityId'), 'orderby': meta.get('orderby')}, dont_filter=True)
    def parse_act_item(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_data'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    def parse_act_item_live(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_act_item_live'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def parse_realtime_flow(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_realtime_flow'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    def parse_realtime_overview_flow(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        cookie_brand = meta.get('cookie_brand')
        brand = meta.get('brand')
        # meta['cate'] = 'parse_realtime_overview'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                url = 'https://sycm.taobao.com/ipoll/live/refreshRest.json?appId=sycm&topic=tb_user_day_payamt'
                yield Request(url, callback=self.parse_realtime_overview_payamt, headers=header, cookies=cookie_brand,
                              meta={'brand': brand, 'cookie': cookie_brand, 'flow_content': data}, dont_filter=True)

    def parse_realtime_overview_payamt(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_realtime_overview_flow_payamt'
        # brand = meta.get('brand')
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item['meta'] = meta
                yield item

    def parse_realtime_item_top(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_realtime_item_top'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    def parse_act_detail_hour_live(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_act_detail_hour_live'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    def parse_realtime_popularize(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        meta = response.meta
        meta['cate'] = 'parse_realtime_popularize'
        if str(code) == '0':
            data = content_json.get('data')
            if data:
                item = QianniuItem()
                item['content'] = data
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item


    