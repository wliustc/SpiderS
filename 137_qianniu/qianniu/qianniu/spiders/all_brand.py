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
r = redis.Redis(host='116.196.71.111', port=52385, db=0)

class BusinessAdviserSpider(scrapy.Spider):
    name = "all_brand"
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


                cate = '流量构成'
                url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&' \
                      'date=%s,%s&dateId=1006960&dateType=static&filter=[6,7]&' \
                      'show=[{"id":1014477},{"id":1014478},{"id":1007563},{"id":1006969},' \
                      '{"id":1006964},{"id":1016014},{"id":1006968}]' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '交易总览'
                url = 'https://sycm.taobao.com/bda/tradinganaly/overview/get_summary.json?' \
                      'dateRange=%s|%s&dateType=recent1&device=0' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '交易'
                url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&' \
                      'date=%s,%s&dateId=1006960&dateType=static&desc=&' \
                      'filter=[6,7]&name=&owner=user&show=[{"id":1014486},{"id":1014480},' \
                      '{"id":1016045},{"id":1016013},{"id":1007104},{"id":1007107},' \
                      '{"id":1007105},{"id":1016030},{"id":1007108},{"id":1016007},{"id":1006965},{"id":1007558},{"id":1007557},{"id":1007109}]' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '商品效果'
                url = 'https://sycm.taobao.com/bda/items/effect/getItemsEffectDetail.json?' \
                      'dateRange=%s|%s&dateType=recent1&device=0&orderDirection=false&' \
                      'orderField=itemPv&pageLimit=2000&type=0&page=1' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'brand': brand, 'cookie_brand': cookie_brand}, dont_filter=True)

                cate = '评价内容分析'
                url = 'https://sycm.taobao.com/qos/review/analyse/content.json?dateType=day' \
                      '&dateRange=%s|%s&cateId=0&cateFlag=-1&brandId=0&imprEmotion=2' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'imprEmotion': '负面评价', 'brand': brand,'cookie_brand':cookie_brand},
                              dont_filter=True)
                url = 'https://sycm.taobao.com/qos/review/analyse/content.json?dateType=day' \
                      '&dateRange=%s|%s&cateId=0&cateFlag=-1&brandId=0&imprEmotion=1' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'imprEmotion': '正面评价', 'brand': brand,'cookie_brand':cookie_brand},
                              dont_filter=True)

                cate = '维权总览'
                url = 'https://sycm.taobao.com/qos/claim/general/guide.json?dateType=day&' \
                      'dateRange=%s|%s' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '流量来源无线'
                url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?' \
                      'dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&indexCode=uv,' \
                      'crtByrCnt,crtRate&device=2' % month
                url = 'https://sycm.taobao.com/flow/new/shop/source/tree.json?' \
                      'dateType=day&dateRange=%s|%s&device=2' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'device': '无线端', 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '流量来源PC'
                url = 'https://sycm.taobao.com/flow/new/overview/shopFlowSourceTop.json?' \
                      'dateRange=%s|%s&dateType=day&order=desc&orderBy=uv&indexCode=uv,' \
                      'crtByrCnt,crtRate&device=1' % month
                url = 'https://sycm.taobao.com/flow/new/shop/source/tree.json?' \
                      'dateType=day&dateRange=%s|%s&device=1' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'device': 'PC端', 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

                cate = '天猫日报缺失'
                url = 'https://sycm.taobao.com/adm/execute/preview.json?app=op&' \
                      'date=%s,%s&dateId=1006960&dateType=static&desc=&filter=[6,7]&' \
                      'id=null&itemId=null&name=&owner=user&show=[{"id":1007557},' \
                      '{"id":1014506},{"id":1014507},{"id":1014479},{"id":1007562},' \
                      '{"id":1006967},{"id":1006966},{"id":1007106},{"id":1011649},' \
                      '{"id":1011647},{"id":1011648}]' % month
                yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                              meta={'cate': cate, 'month': month, 'brand': brand,'cookie_brand':cookie_brand}, dont_filter=True)

    def parse(self, response):
        try:
            content = response.body
            # print content
            content_json = json.loads(content)
            code = content_json.get('code')
            # print code
            meta = response.meta
            if str(code) == '0':
                item = QianniuItem()
                item['content'] = response.body
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

                if meta.get('cate') == '商品效果':
                    url = response.url
                    url_list = url.split('&page=')
                    if url_list[1] == '1':
                        item_json = json.loads(response.body)
                        data = item_json.get('data')
                        if data:
                            recordCount = data.get('recordCount')
                            # recordCount = 6033
                            if recordCount:
                                page_num, page_mod = divmod(int(recordCount), 2000)
                                # print page_num, page_mod
                                if page_mod > 0:
                                    page_num = page_num + 1
                                # print page_num

                                for i in xrange(2, page_num + 1):
                                    url_xg = url_list[0] + '&page=%s' % i
                                    # print url_xg
                                    yield Request(url_xg, callback=self.parse, headers=header, cookies=meta.get('cookie_brand'),
                                                  meta={'cate': meta.get('cate'), 'month': meta.get('month'),
                                                        'brand': meta.get('brand')}, dont_filter=True)


            else:
                # print content
                try:
                    msg = content_json.get('msg')
                    if 'login' in msg:
                        #r.hset('cookie_logou',meta.get('brand'),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        pass

                except Exception ,e:
                    print e
                    # print response.body
                    pass
        except:
            print '*******' * 10
            meta = response.meta
            url = response.url
            #yield Request(url, callback=self.parse, headers=header, cookies=meta.get('cookie_brand'),
            #              meta=meta, dont_filter=True)



    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    
    
    
    