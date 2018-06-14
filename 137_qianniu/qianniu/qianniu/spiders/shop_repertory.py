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


class ShopRepertorySpider(scrapy.Spider):
    name = 'shop_repertory'
    allowed_domains = ['taobao.com']

    # start_urls = ['http://taobao.com/']

    def __init__(self, select_date='yesterday', crawl_brand='all', *args, **kwargs):
        super(ShopRepertorySpider, self).__init__(*args, **kwargs)
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
                            # activityName = d.get('activityName')
                            preheatStart = d.get('preheatStart')
                            activityId = d.get('id')
                            preheatEnd = d.get('preheatEnd')
                            activityEnd = d.get('activityEnd')
                            activityStatus = d.get('activityStatus')
                            activityStart = d.get('activityStart')
                            preheatStart = preheatStart.encode('utf-8')
                            preheatEnd = preheatEnd.encode('utf-8')
                            activityEnd = activityEnd.encode('utf-8')
                            activityStart = activityStart.encode('utf-8')
                            if activityStatus == 3:
                                if preheatStart and preheatEnd:
                                    days, start_time = self.time_zhuanhua(preheatStart, preheatEnd)
                                    for i in xrange(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        # print type(start_time)
                                        time = str(time)
                                        preheat_time = re.search(r'\d+-\d+-\d+', time)
                                        if preheat_time:
                                            preheat_time = preheat_time.group()
                                            # month = (preheat_time, preheat_time)
                                            if preheat_time:
                                                # activityId= '415749'
                                                # preheat_time = '2018-04-14'
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListOffline.json?activityId=' + str(
                                                    activityId) + '&itemType=0&device=1&keyword=&dateType=day&dateRange=' + str(
                                                    preheat_time) + '%7C' + str(
                                                    preheat_time) + '&pageSize=20&page=1&order=desc&orderBy=cartCnt'
                                                yield scrapy.Request(url, callback=self.parse_data,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'url': url, 'brand': brand,
                                                                           'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': preheat_time, 'orderby':'cartCnt', 'activityId':activityId},
                                                                     dont_filter=True)
                                if activityEnd and activityStart:
                                    days, start_time = self.time_zhuanhua(activityStart, activityEnd)
                                    for i in xrange(0, days + 1):
                                        time = start_time + datetime.timedelta(days=i)
                                        time = str(time)
                                        activity_time = re.search(r'\d+-\d+-\d+', time)
                                        if activity_time:
                                            activity_time = activity_time.group()
                                            if activity_time:
                                                # https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListOffline.json?activityId=311334&itemType=0&device=1&keyword=&dateType=day&dateRange=2018-01-28%7C2018-01-28&pageSize=10&page=1&order=desc&orderBy=itemPayAmt
                                                url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListOffline.json?activityId=' + str(
                                                    activityId) + '&itemType=0&device=1&keyword=&dateType=day&dateRange=' + str(
                                                    activity_time) + '%7C' + str(
                                                    activity_time) + '&pageSize=20&page=1&order=desc&orderBy=itemPayAmt'
                                                yield scrapy.Request(url, callback=self.parse_data,
                                                                     headers=header, cookies=cookie_brand,
                                                                     meta={'url': url, 'brand': brand,
                                                                           'cookie_brand': cookie_brand,
                                                                           'd': d, 'activity_time': activity_time,'orderby':'itemPayAmt', 'activityId':activityId},
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

    def parse_data(self, response):
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
                count = data.get('recordCount')
                if count:
                    num = int(round(float(count / 20)))
                    for i in xrange(2, num + 2):
                        url = 'https://sycm.taobao.com/datawar/v3/activity/itemCoreIndex/getItemListOffline.json?activityId=' + str(
                            meta.get('activityId')) + '&itemType=0&device=1&keyword=&dateType=day&dateRange=' + str(
                            meta.get('activity_time')) + '%7C' + str(
                            meta.get('activity_time')) + '&pageSize=20&page=' + str(i) + '&order=desc&orderBy=' + meta.get('orderby')
                        yield scrapy.Request(url, callback=self.parse_act_item_live,
                                             headers=header, cookies=meta.get('cookie_brand'),
                                             meta={'url': url, 'brand': meta.get('brand'),
                                                   'cookie_brand': meta.get('cookie_brand'),
                                                   'd': meta.get('d'), 'activityId':meta.get('activityId'), 'activity_time': meta.get('activity_time'), 'orderby':meta.get('orderby')},
                                             dont_filter=True)


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
        preheatEnd = datetime.datetime.strptime(preheatEnd, '%Y-%m-%d %H:%M:%S')
        preheatStart = datetime.datetime.strptime(preheatStart, '%Y-%m-%d %H:%M:%S')
        delta = preheatEnd - preheatStart
        return delta.days, preheatStart

