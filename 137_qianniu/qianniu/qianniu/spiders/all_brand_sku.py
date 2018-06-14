# coding=utf8

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

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')


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
    name = "all_brand_sku"
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
        r = redis.Redis(host='116.196.71.111', port=52385, db=0)
        data = db.query('select sign from t_spider_table_sign where '
                        'spider_name="all_brand" and dt="%s";' % self.getSignday())
        if data:
            sign = data[0].get('sign')
            if sign:
                if self.crawl_brand == 'all':
                    data = r.hgetall('cookie')
                    brand_list = []
                    crawl_brand_list_temp = []
                    if data:
                        for brand, val in data.items():
                            brand_list.append(brand)
                    # 2018-01-16为标准，即18个品牌全部都在
                    data_brand = db.query("select distinct "
                                          "brand from t_spider_sycm_staccato_items_sku "
                                          "where data_dt='%s';" % self.select_date)
                    if data_brand:
                        for d in data_brand:
                            crawl_brand_list_temp.append(d.get('brand'))
                        # 差集
                        li = set(brand_list) - set(crawl_brand_list_temp)
                        li = list(li)
                        if len(li) == 0:
                            self.crawl_brand = ''
                        else:
                        	self.crawl_brand = ','.join(li)
                    else:
                        # 差集
                        #li = set(brand_list) - set(crawl_brand_list_temp)
                        #li = list(li)
                        #if len(li) == 0:
                        #   self.crawl_brand = ''
                        #else:
                        self.crawl_brand = ','.join(brand_list)
                if self.crawl_brand:
                    
                    data = r.hgetall('cookie')
                    print data
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

                            item_brand = db.query('select id from t_spider_sycm_staccato_items_effect where dt="%s" and brand="%s" and itemStatus=1;' % (self.select_date,brand))
                            if item_brand:
                                for ib in item_brand:
                                    goods_id = ib.get('id')

                                    cate = 'SKU'
                                    url = 'https://sycm.taobao.com/bda/items/itemanaly/sku/' \
                                          'getSalesDetails.json?dateRange=%s|%s&dateType=day' \
                                          '&device=0&itemId=%s&order=desc&' \
                                          'orderBy=skuNewAddCartItemCnt&page=1&pageLimit=50' % (month[0],month[1],goods_id)
                                    yield Request(url, callback=self.parse, headers=header, cookies=cookie_brand,
                                                  meta={'cate': cate, 'brand': brand,'goods_id':goods_id,'cookie_brand':cookie_brand}, dont_filter=True)


    def parse(self, response):
        try:
            content = response.body
            print content
            content_json = json.loads(content)
            code = content_json.get('code')
            print code
            meta = response.meta
            if str(code) == '0':
                item = QianniuItem()
                item['content'] = response.body
                item['meta'] = meta
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                # item['dt'] = self.getSignday()
                item['data_dt'] = self.select_date
                yield item
        except:
            url = response.url
            meta = response.meta
            yield Request(url, callback=self.parse, headers=header, cookies=meta.get('cookie_brand'),
                          meta=meta,
                          dont_filter=True)

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def getSignday(self):
        select_date1 = self.select_date
        select_date2 = datetime.datetime.strptime(select_date1, "%Y-%m-%d") + datetime.timedelta(days=1)
        return select_date2.strftime("%Y-%m-%d")
    
    
    
    
    
    
    