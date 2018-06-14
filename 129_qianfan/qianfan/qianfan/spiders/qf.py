# -*- coding: utf-8 -*-
import datetime
import scrapy
import json,urllib
from scrapy import Request
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

class QfSpider(scrapy.Spider):
    name = "qf"
    allowed_domains = ["qianfan.analysys.cn"]
    # start_urls = ['http://qianfan.analysys.cn/']

    def start_requests(self):
        data = db.query('select distinct cateId from t_spider_qianfan_category;')
        for d in data:
            cateid = d.get('cateId')
            date_ = '2017/08/01'
            url = 'http://qianfan.analysys.cn/qianfan/category/appIndexs?categoryId='+cateid+'&statDate='+date_
            print url
            yield Request(url, callback=self.parse_list, meta={'date_': date_})
        # url = 'http://qianfan.analysys.cn/qianfan/category/appIndexs?categoryId=1071073&statDate=2017/08/01'
        # yield Request(url,callback=self.parse_list,meta={'date_':'2017/08/01'})

    def start_requests1(self):
        url = 'http://qianfan.analysys.cn/qianfan/category/list?queryType=-1'
        yield Request(url,callback=self.parse_category)

    # 采集千帆分类
    def parse_category(self, response):
        content = json.loads(response.body)
        datas = content.get('datas')
        categorys = datas.get('categorys')
        if categorys:
            for category in categorys:
                # print category
                cateName = category.get('cateName')
                categorys_child = category.get('categorys')
                if categorys_child:
                    for category_child in categorys_child:
                        item = {}
                        item['isDisplay'] = category_child.get('isDisplay')
                        item['cateId'] = category_child.get('cateId')
                        item['cateName'] = category_child.get('cateName')
                        item['cateDesc'] = category_child.get('cateDesc')
                        item['orderNum'] = category_child.get('orderNum')
                        item['parentCateId'] = category_child.get('parentCateId')
                        item['rootCategoryId'] = category_child.get('rootCategoryId')
                        item['newCategory'] = category_child.get('newCategory')
                        item['status'] = category_child.get('status')
                        item['createdDate'] = category_child.get('createdDate')
                        db.insert('t_spider_qianfan_category', **item)

    def parse_list(self,response):
        content = json.loads(response.body)
        datas = content.get('datas')
        appIndexList = datas.get('appIndexList')
        if appIndexList:
            for appindex in appIndexList:
                item = {}
                for key,value in appindex.items():
                    if not value:
                        value = ''
                    item[key] = value
                item['dateValue'] = datas.get('dateValue').get('value')
                db.insert('t_spider_qianfan_yuedu',**item)
                yield item
            meta = response.meta
            date_ = meta['date_']
            now = datetime.datetime.strptime(date_, '%Y/%m/%d')
            date_1 = (now.replace(day=1) - datetime.timedelta(1)).replace(day=1)
            date_1 = date_1.strftime('%Y/%m/%d')
            url = response.url.replace(date_,date_1)
            print url
            meta['date_'] = date_1
            meta['retry_times'] = 0
            yield Request(url,callback=self.parse_list,meta=meta)
    
    
    