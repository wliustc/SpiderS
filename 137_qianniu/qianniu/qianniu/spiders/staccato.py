# -*- coding: utf-8 -*-
import json
import scrapy
import web
from scrapy import Request
from qianniu.items import QianniuItem
import datetime
import time
import redis
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


class BusinessAdviserSpider(scrapy.Spider):
    name = "staccato"
    allowed_domains = ["taobao.com"]

    # start_urls = ['http://taobao.com/']

    def __init__(self, select_date='yesterday', *args, **kwargs):
        super(BusinessAdviserSpider, self).__init__(*args, **kwargs)
        if select_date == 'yesterday':
            self.select_date = self.getYesterday()
        else:
            self.select_date = select_date
        self.cookie = ""

    def start_requests(self):
        # data = db.query('select cookie from t_spider_sycm_cookie')
        r = redis.Redis(host='116.196.71.111', port=52385, db=0)
        data =r.hget('cookie','staccato')
        if data:
            self.cookie = data
        print self.cookie
        cookie_list = self.cookie.split(';')
        self.cookie = {}
        if cookie_list:
            for cookie in cookie_list:
                cookies = cookie.split('=')
                print cookies
                if len(cookies) == 2:
                    key = cookies[0]
                    val = cookies[1]
                    self.cookie[key.strip()] = val.strip()
        # self.cookie = {cookie_list[0]:cookie_list[1]}
        print self.cookie
        month = (self.select_date, self.select_date)

        # cate = '退款率'
        # url = 'https://sycm.taobao.com/qos/claim/general/guide.json?dateType=day&dateRange=%s|%s' % month
        # yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
        #               meta={'cate': cate}, dont_filter=True)

        cate = '流量构成'
        # url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&date=1&' \
        #       'dateId=1006960&dateType=dynamic&desc=&filter=[6,7]&id=137977&' \
        #       'itemId=null&name=crawl_use_tmall&owner=user&show=[{%22id%22:1014477}' \
        #       ',{%22id%22:1014478},{%22id%22:1007563},{%22id%22:1006969},' \
        #       '{%22id%22:1006964},{%22id%22:1016014},{%22id%22:1006968}]'
        url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&' \
              'date=%s,%s&dateId=1006960&dateType=static&filter=[6,7]&' \
              'show=[{"id":1014477},{"id":1014478},{"id":1007563},{"id":1006969},' \
              '{"id":1006964},{"id":1016014},{"id":1006968}]' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate}, dont_filter=True)

        cate = '交易总览'
        url = 'https://sycm.taobao.com/bda/tradinganaly/overview/get_summary.json?' \
              'dateRange=%s|%s&dateType=recent1&device=0' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month}, dont_filter=True)

        cate = '交易'
        # url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&date=1&' \
        #       'dateId=1006960&dateType=dynamic&desc=&filter=[6,7]&id=137978&' \
        #       'itemId=null&name=crawl_use_overview&owner=user&show=[{%22id%22:' \
        #       '1014486},{%22id%22:1014480},{%22id%22:1016045},{%22id%22:1016013},' \
        #       '{%22id%22:1007104},{%22id%22:1007107},{%22id%22:1007105},{%22id%22:' \
        #       '1016030},{%22id%22:1007108},{%22id%22:1016007}]'
        url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&' \
              'date=%s,%s&dateId=1006960&dateType=static&desc=&' \
              'filter=[6,7]&name=&owner=user&show=[{"id":1014486},{"id":1014480},' \
              '{"id":1016045},{"id":1016013},{"id":1007104},{"id":1007107},' \
              '{"id":1007105},{"id":1016030},{"id":1007108},{"id":1016007}]' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate}, dont_filter=True)

        cate = '商品效果'
        url = 'https://sycm.taobao.com/bda/items/effect/getItemsEffectDetail.json?' \
              'dateRange=%s|%s&dateType=recent1&device=0&orderDirection=false&' \
              'orderField=itemPv&page=1&pageLimit=10&type=0' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month}, dont_filter=True)

        cate = '评价内容分析'
        url = 'https://sycm.taobao.com/qos/review/analyse/content.json?dateType=day' \
              '&dateRange=%s|%s&cateId=0&cateFlag=-1&brandId=0&imprEmotion=2' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month, 'imprEmotion': '负面评价'}, dont_filter=True)
        url = 'https://sycm.taobao.com/qos/review/analyse/content.json?dateType=day' \
              '&dateRange=%s|%s&cateId=0&cateFlag=-1&brandId=0&imprEmotion=1' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month, 'imprEmotion': '正面评价'}, dont_filter=True)

        cate = '维权总览'
        url = 'https://sycm.taobao.com/qos/claim/general/guide.json?dateType=day&' \
              'dateRange=%s|%s' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month}, dont_filter=True)

        cate = '流量来源无线'
        # url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?dateRange={}|{}&dateType=recent1&order=desc&orderBy=uv&indexCode=uv%2CcrtByrCnt%2CcrtRate&device=2'.format(
        # self.getYesterday(), self.getYesterday())
        url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?' \
              'dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&indexCode=uv,' \
              'crtByrCnt,crtRate&device=2' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month,'device':'无线端'}, dont_filter=True)

        cate = '流量来源PC'
        # url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?dateRange={}|{}&dateType=recent1&order=desc&orderBy=uv&indexCode=uv%2CcrtByrCnt%2CcrtRate&device=1'.format(
        # self.getYesterday(), self.getYesterday())
        url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?' \
              'dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&indexCode=uv,' \
              'crtByrCnt,crtRate&device=1' % month
        yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                      meta={'cate': cate, 'month': month,'device':'PC端'}, dont_filter=True)

    def parse(self, response):
        content = response.body
        content_json = json.loads(content)
        code = content_json.get('code')
        if str(code) == '0':
            item = QianniuItem()
            item['content'] = response.body
            item['meta'] = response.meta
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield item
        else:
            try:
                msg = content_json.get('msg')
                if 'login' not in msg:
                    meta = response.meta
                    url = response.url
                    yield Request(url, callback=self.parse, headers=header, cookies=self.cookie,
                                  meta=meta, dont_filter=True)
            except Exception,e:
                print e
                print response.body

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")
