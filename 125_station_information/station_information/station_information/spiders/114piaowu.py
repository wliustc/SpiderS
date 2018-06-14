# coding=utf8

# -*- coding: utf-8 -*-
from urlparse import urljoin

import redis
import scrapy
import time
from scrapy import Request
from scrapy.selector import Selector
from station_information.items import StationInformationItem
import sys, web

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

task_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))



redis_conn = redis.Redis(host='10.15.1.11', port=6379, db=0)

class StationSpider(scrapy.Spider):
    name = "114"
    allowed_domains = ["114piaowu.com"]

    def start_requests(self):
        urls = [
            'http://checi.114piaowu.com/C_1',
            'http://checi.114piaowu.com/D_1',
            'http://checi.114piaowu.com/G_1',
            'http://checi.114piaowu.com/K_1',
            'http://checi.114piaowu.com/L_1',
            'http://checi.114piaowu.com/Q_1',
            'http://checi.114piaowu.com/S_1',
            'http://checi.114piaowu.com/T_1',
            'http://checi.114piaowu.com/Y_1',
            'http://checi.114piaowu.com/Z_1',
            'http://checi.114piaowu.com/1_1',
            'http://checi.114piaowu.com/2_1',
            'http://checi.114piaowu.com/3_1',
            'http://checi.114piaowu.com/4_1',
            'http://checi.114piaowu.com/5_1',
            'http://checi.114piaowu.com/6_1',
            'http://checi.114piaowu.com/7_1',
            'http://checi.114piaowu.com/8_1',
            'http://checi.114piaowu.com/9_1',

        ]
        for url in urls:
            print url
            yield Request(url,callback=self.parse)


    def parse(self, response):
        sel = Selector(response)
        checicx_list = sel.xpath('//div[@class="checicx"]/ul/li/a/@href').extract()
        if checicx_list:
            for checicx in checicx_list:
                # print checicx
                url = urljoin(response.url,checicx)
                yield Request(url,callback=self.parse_station)

            next_page = sel.xpath('//div[@class="page"]/a[last()-1]')
            if ''.join(next_page.xpath('text()').extract()) == '>':
                next_page = ''.join(next_page.xpath('@href').extract())
                next_page = urljoin(response.url,next_page)
                print next_page
                yield Request(next_page, callback=self.parse)

    def parse_station(self,response):
        item = StationInformationItem()
        item['content'] = response.body
        yield item
