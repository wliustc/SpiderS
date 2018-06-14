# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
import xlrd
from scrapy import Request
from scrapy.selector import Selector
import sys
from TianYanCha.items import QiDuoWeiItem
reload(sys)
sys.setdefaultencoding('utf8')

class QiduoweiSpider(scrapy.Spider):
    name = "qiduowei"
    allowed_domains = ["qiduowei.com"]
    start_urls = ['http://www.qiduowei.com/']

    def start_requests(self):
        book = xlrd.open_workbook('/home/work/wguan/drugstore/data_drugstore_part1.xlsx')
        sheet = book.sheets()[0]
        nrows = sheet.nrows
        # count = 0
        for i in range(0, nrows):
            company_name = sheet.cell(i, 0).value
            yield Request('http://www.qiduowei.com/search?key=%s' % company_name, callback=self.parse_list,
                          meta={'company_name': company_name,'retry_times':0},dont_filter=True,errback=self.parse_error)
        # company_name = '北京东升天保堂连锁药店有限公司文化园东路店'
        # yield Request('http://www.qiduowei.com/search?key=%s' % company_name, callback=self.parse_list,
        #                   meta={'company_name': company_name},dont_filter=True,errback=self.parse_error)

    def parse_list(self, response):
        meta = response.meta
        meta['retry_times'] = 0
        if response.status != 200:
            yield Request(response.url, callback=self.parse_list, dont_filter=True,meta=meta,errback=self.parse_error)
        else:
            company_name = response.meta['company_name']
            print company_name
            sel = Selector(response)
            company_list = sel.xpath('//div[@class="list-item"]/a')
            if company_list:
                company_name_=''
                for company in company_list:
                    company_name_ = ''.join(company.xpath('@title').extract()).replace('的相关企业工商信息','')
                    print company_name_
                    if company_name_.replace('（','(').replace('）',')')==company_name.replace('（','(').replace('）',')'):
                        url = ''.join(company.xpath('@href').extract())
                        url = urljoin(response.url,url)
                        yield Request(url,callback=self.parse_detail,dont_filter=True,errback=self.parse_error,meta=meta)
                        break
                if company_name_:
                    if company_name_!=company_name:
                    # else:
                        item = QiDuoWeiItem()
                        item['response_body'] = company_name
                        yield item

    def parse_detail(self,response):
        meta = response.meta
        meta['retry_times'] = 0
        if response.status != 200:

            yield Request(response.url, callback=self.parse_detail, dont_filter=True,errback=self.parse_error,meta=meta)
        else:
            content = response.body
            item = QiDuoWeiItem()
            item['response_body'] = content
            yield item

    def parse_error(self,failure):
        url = failure.request.url
        meta = failure.request.meta
        meta['retry_times'] = 0
        if 'search' in url:
            yield Request(url,callback=self.parse_list,dont_filter=True,meta=meta,errback=self.parse_error)
        else:
            yield Request(url, callback=self.parse_detail, dont_filter=True,
                          errback=self.parse_error,meta=meta)

    