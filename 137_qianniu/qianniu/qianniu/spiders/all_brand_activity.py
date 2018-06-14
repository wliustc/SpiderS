# -*- coding: utf-8 -*-
import json
import scrapy
import web
from scrapy import Request
from qianniu.items import QianniuItem
import datetime
import time
import redis
import sys
import re

# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
reload(sys)
sys.setdefaultencoding('utf-8')
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
    name = "all_brand_activity"
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
                url = 'https://sycm.taobao.com/datawar/activityConfig/getActivityListBy.json?activityStatus=-1&activityType=-1&activityStartType=all&keyword=&orderBy=activityStart&order=desc&page=1&pageSize=2000000&activitySeason=-1&activityCycle=-1'
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
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
                data = data.get('data')
                if data:
                    data = data.get('data')
                    if data:
                        for d in data:
                            # activity_name = d.get('activityName')
                            # activity_name = activity_name.encode('utf-8')
                            preheatStart = d.get('preheatStart')
                            activityId = d.get('id')
                            preheatEnd = d.get('preheatEnd')
                            activityEnd = d.get('activityEnd')
                            activityStatus = d.get('activityStatus')
                            activityStart = d.get('activityStart')
                            preheatStart = preheatStart.encode('utf-8')
                            preheatEnd = preheatEnd.encode('utf-8')
                            yesterday = self.getYesterday()
                            if preheatStart and preheatEnd:
                                Start4 = ''
                                End4 = ''
                                Start4_time = re.search(r'\d+-\d+-\d+', preheatStart)
                                if Start4_time:
                                    Start4 = Start4_time.group()
                                End4_time = re.search(r'\d+-\d+-\d+', preheatEnd)
                                if End4_time:
                                    End4 = End4_time.group()
                                if End4 >= yesterday:
                                    days, start_time = self.time_zhuanhua(Start4, yesterday)
                                    for i in range(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        # print type(start_time)
                                        time = str(time)
                                        preheat_time = re.search(r'\d+-\d+-\d+', time)
                                        if preheat_time:
                                            preheat_time = preheat_time.group()
                                            if preheat_time:
                                                # 预热期kpi实时数据
                                                # https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=2018-04-24|2018-04-24&dateType=day&activityId=3
                                                # 61133&status=1&dateType=day&dateRange=2018-04-24%7C2018-04-24&_=1524824318467&token=42a15fd0e
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=' + str(
                                                    preheat_time) + '|' + str(
                                                    preheat_time) + '&dateType=day&activityId=' + str(
                                                    activityId) + '&status=1&dateType=day&dateRange=' + str(
                                                    preheat_time) + '%7C' + str(preheat_time)
                                                yield scrapy.Request(url, callback=self.parse_act_detail_kpi_core_live,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time},
                                                                     dont_filter=True)
                                                # 预热期的推广引流的数据---pc端的数据
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=1&activityId=%s' % (
                                                    preheat_time, preheat_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time,
                                                                           'device': 'PC端'}, dont_filter=True)
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=2&activityId=%s' % (
                                                    preheat_time, preheat_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time,
                                                                           'device': '无线端'}, dont_filter=True)
                                                indexcode_list = ['preheatCartByrCnt', 'preheatCartItmCnt',
                                                                  'preCltByrCnt',
                                                                  'preheatCltItmCnt',
                                                                  'preheatUv']

                                                for indexcode in indexcode_list:
                                                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=' + str(
                                                        activityId) + '&dateType=day&dateRange=' + str(
                                                        preheat_time) + '%7C' + str(
                                                        preheat_time) + '&dateType2=null&dateRange2=null&indexCode=' + indexcode
                                                    yield scrapy.Request(url, callback=self.parse_act_detail_hour_live,
                                                                         headers=header, cookies=cookie_brand,
                                                                         meta={'brand': brand,
                                                                               'cookie_brand': cookie_brand, 'd': d,
                                                                               'indexcode': indexcode,
                                                                               'activity_time': preheat_time},
                                                                         dont_filter=True)
                            if activityEnd and activityStart:
                                Start1 = ''
                                End1 = ''
                                Start1_time = re.search(r'\d+-\d+-\d+', activityStart)
                                if Start1_time:
                                    Start1 = Start1_time.group()
                                End1_time = re.search(r'\d+-\d+-\d+', activityEnd)
                                if End1_time:
                                    End1 = End1_time.group()
                                if End1 >= yesterday:
                                    days, start_time = self.time_zhuanhua(Start1, yesterday)
                                    for i in range(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        time = str(time)
                                        activity_time = re.search(r'\d+-\d+-\d+', time)
                                        if activity_time:
                                            activity_time = activity_time.group()
                                            if activity_time:
                                                # 活动期kpi实时数据
                                                # https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=2018-04-26|2018-04-26&dateType=day
                                                # &activityId=361133&status=2&dateType=day&dateRange=2018-04-26%7C2018-04-26&_=1524824395040&token=42a15fd0e
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=' + str(
                                                    activity_time) + '|' + str(
                                                    activity_time) + '&dateType=day&activityId=' + str(
                                                    activityId) + '&status=2&dateType=day&dateRange=' + str(
                                                    activity_time) + '%7C' + str(activity_time)
                                                yield scrapy.Request(url, callback=self.parse_act_detail_kpi_core_live,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time},
                                                                     dont_filter=True)
                                                # 推广引流的数据
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=1&activityId=%s' % (
                                                    activity_time, activity_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time,
                                                                           'device': 'PC端'}, dont_filter=True)
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=2&activityId=%s' % (
                                                    activity_time, activity_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time,
                                                                           'device': '无线端'}, dont_filter=True)

                                                indexcode_list = ['actItmPayAmt', 'payAmt', 'payCnt', 'actItmPayCnt',
                                                                  'payByrCnt',
                                                                  'actItmPayByrCnt', 'uv']

                                                for indexcode in indexcode_list:
                                                    # https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=293791&dateType=day&dateRange=2017-12-12%7C2017-12-12
                                                    # &dateType2=null&dateRange2=null&indexCode=actItmPayCnt&activity2Id=null&_=1524823284933&token=42a15fd0e
                                                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=' + str(
                                                        activityId) + '&dateType=day&dateRange=' + str(
                                                        activity_time) + '%7C' + str(
                                                        activity_time) + '&dateType2=null&dateRange2=null&indexCode=' + indexcode
                                                    yield scrapy.Request(url, callback=self.parse_act_detail_hour_live,
                                                                         headers=header,
                                                                         cookies=cookie_brand,
                                                                         meta={'brand': brand,
                                                                               'cookie_brand': cookie_brand, 'd': d,
                                                                               'indexcode': indexcode,
                                                                               'activity_time': activity_time},
                                                                         dont_filter=True)

                            if activityStatus == 3:
                                if preheatStart and preheatEnd:
                                    Start2 = ''
                                    End2 = ''
                                    start2_time = re.search(r'\d+-\d+-\d+', preheatStart)
                                    if start2_time:
                                        Start2 = start2_time.group()
                                    End2_time = re.search(r'\d+-\d+-\d+', preheatEnd)
                                    if End2_time:
                                        End2 = End2_time.group()
                                    days, start_time = self.time_zhuanhua(Start2, End2)
                                    for i in range(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        # print type(start_time)
                                        time = str(time)
                                        preheat_time = re.search(r'\d+-\d+-\d+', time)
                                        if preheat_time:
                                            preheat_time = preheat_time.group()
                                            if preheat_time:
                                                # 预热期kpi实时数据
                                                # https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=2018-04-24|2018-04-24&dateType=day&activityId=3
                                                # 61133&status=1&dateType=day&dateRange=2018-04-24%7C2018-04-24&_=1524824318467&token=42a15fd0e
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=' + str(
                                                    preheat_time) + '|' + str(
                                                    preheat_time) + '&dateType=day&activityId=' + str(
                                                    activityId) + '&status=1&dateType=day&dateRange=' + str(
                                                    preheat_time) + '%7C' + str(preheat_time)
                                                yield scrapy.Request(url, callback=self.parse_act_detail_kpi_core_live,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time},
                                                                     dont_filter=True)
                                                # 预热期的推广引流的数据---pc端的数据
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=1&activityId=%s' % (
                                                    preheat_time, preheat_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time,
                                                                           'device': 'PC端'}, dont_filter=True)
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=2&activityId=%s' % (
                                                    preheat_time, preheat_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'preheat_time': preheat_time,
                                                                           'device': '无线端'}, dont_filter=True)
                                                indexcode_list = ['preheatCartByrCnt', 'preheatCartItmCnt',
                                                                  'preCltByrCnt',
                                                                  'preheatCltItmCnt',
                                                                  'preheatUv']

                                                for indexcode in indexcode_list:
                                                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=' + str(
                                                        activityId) + '&dateType=day&dateRange=' + str(
                                                        preheat_time) + '%7C' + str(
                                                        preheat_time) + '&dateType2=null&dateRange2=null&indexCode=' + indexcode
                                                    yield scrapy.Request(url, callback=self.parse_act_detail_hour_live,
                                                                         headers=header, cookies=cookie_brand,
                                                                         meta={'brand': brand,
                                                                               'cookie_brand': cookie_brand, 'd': d,
                                                                               'indexcode': indexcode,
                                                                               'activity_time': preheat_time},
                                                                         dont_filter=True)

                            if activityStatus == 3:
                                # print '1111'
                                if activityEnd and activityStart:
                                    Start3 = ''
                                    End3 = ''
                                    start3_time = re.search(r'\d+-\d+-\d+', activityStart)
                                    if start3_time:
                                        Start3 = start3_time.group()
                                    End3_time = re.search(r'\d+-\d+-\d+', activityEnd)
                                    if End3_time:
                                        End3 = End3_time.group()
                                    days, start_time = self.time_zhuanhua(Start3, End3)
                                    for i in range(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        time = str(time)
                                        activity_time = re.search(r'\d+-\d+-\d+', time)
                                        if activity_time:
                                            activity_time = activity_time.group()
                                            if activity_time:
                                                # 活动期kpi实时数据
                                                # https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=2018-04-26|2018-04-26&dateType=day
                                                # &activityId=361133&status=2&dateType=day&dateRange=2018-04-26%7C2018-04-26&_=1524824395040&token=42a15fd0e
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/kpi/coreIndex/offline.json?dateRange=' + str(
                                                    activity_time) + '|' + str(
                                                    activity_time) + '&dateType=day&activityId=' + str(
                                                    activityId) + '&status=2&dateType=day&dateRange=' + str(
                                                    activity_time) + '%7C' + str(activity_time)
                                                yield scrapy.Request(url, callback=self.parse_act_detail_kpi_core_live,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time},
                                                                     dont_filter=True)
                                                # 推广引流的数据
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=1&activityId=%s' % (
                                                    activity_time, activity_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time,
                                                                           'device': 'PC端'}, dont_filter=True)
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/detail/guide/chl/offline.json?dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&device=2&activityId=%s' % (
                                                    activity_time, activity_time, activityId)
                                                yield scrapy.Request(url, callback=self.parse_realtime_popularize,
                                                                     headers=header,
                                                                     cookies=cookie_brand,
                                                                     meta={'brand': brand, 'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time,
                                                                           'device': '无线端'}, dont_filter=True)

                                                indexcode_list = ['actItmPayAmt', 'payAmt', 'payCnt', 'actItmPayCnt',
                                                                  'payByrCnt',
                                                                  'actItmPayByrCnt', 'uv']

                                                for indexcode in indexcode_list:
                                                    # https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=293791&dateType=day&dateRange=2017-12-12%7C2017-12-12
                                                    # &dateType2=null&dateRange2=null&indexCode=actItmPayCnt&activity2Id=null&_=1524823284933&token=42a15fd0e
                                                    url = 'https://sycm.taobao.com/datawar/v3/activity/detail/effect/hour.json?activityId=' + str(
                                                        activityId) + '&dateType=day&dateRange=' + str(
                                                        activity_time) + '%7C' + str(
                                                        activity_time) + '&dateType2=null&dateRange2=null&indexCode=' + indexcode
                                                    yield scrapy.Request(url, callback=self.parse_act_detail_hour_live,
                                                                         headers=header,
                                                                         cookies=cookie_brand,
                                                                         meta={'brand': brand,
                                                                               'cookie_brand': cookie_brand, 'd': d,
                                                                               'indexcode': indexcode,
                                                                               'activity_time': activity_time},
                                                                         dont_filter=True)

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

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

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

    def time_zhuanhua(self, preheatStart, preheatEnd):
        preheatEnd = datetime.datetime.strptime(preheatEnd, '%Y-%m-%d')
        preheatStart = datetime.datetime.strptime(preheatStart, '%Y-%m-%d')
        delta = preheatEnd - preheatStart
        return delta.days, preheatStart


