# -*- coding: utf-8 -*-
import re

import scrapy
import json

import time
from scrapy import Request
from PhysicalEducation.items import AiRuiDetailItem
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

time_name = {50: '2017年3月', 49: '2017年2月', 48: '2017年1月', 47: '2016年12月', 46: '2016年11月', 45: '2016年10月', 44: '2016年9月',
             43: '2016年8月', 42: '2016年7月', 41: '2016年6月', 40: '2016年5月', 39: '2016年4月', 38: '2016年3月', 37: '2016年2月',
             36: '2016年1月'}


class AiRuiDetailSpider(scrapy.Spider):
    name = "airui_detail"
    allowed_domains = ["iresearch.com.cn"]

    def start_requests(self):

        data = db.query('select distinct Appid from t_spider_airui_index')
        print data
        for d in data:
            # print d.Appid
            for i in xrange(50, 35, -1):
                url = 'http://index.iresearch.com.cn/app/attrlist/?aid=%s&tid=%s&typeid=0' % (d.Appid,i)
                yield Request(url, self.parse, meta={'Appid': d.Appid, 'TimeName': i})

    def parse(self, response):
        json_content = json.loads(response.body)
        List = json_content.get('List')
        if List:
            for ll in List:
                item = AiRuiDetailItem()
                item['Appid'] = response.meta['Appid']
                item['RootType'] = ll.get('RootType')
                item['TypeName'] = ll.get('TypeName')
                item['Proportion'] = ll.get('Proportion')
                item['task_time'] = dt
                item['TimeName'] = time_name.get(response.meta['TimeName'])
                yield item
