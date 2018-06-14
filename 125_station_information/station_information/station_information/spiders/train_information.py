# -*- coding: utf-8 -*-
from urlparse import urljoin

import redis
import scrapy
import time
from scrapy import Request
from scrapy.selector import Selector
import re
from station_information.items import TrainInfomationItem
import sys, web
import json

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

task_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

header = {
    'Host': 'kyfw.12306.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

Cookie = {
    'JSESSIONID':'C04CE74442F1EA5982BB9236042F83CA',
    'route':'6f50b51faa11b987e576cdb301e545c4',
    'BIGipServerotn':'1173357066.38945.0000',
    'RAIL_EXPIRATION':'1506015170620',
    'RAIL_DEVICEID':'gKMIfHv29OG6Twt-njA0avO0IiVrM3NPLGJNxY_aeirMFT-j5dn4vY9Ag-CMmq88T7_BAwZllbmshHeyD50bLNCPaol7kk2xXkKaExOgti4TNYEr8Es6oZIzKQoesQ3HrmEfTVIsX0ChEfYmdPytBP-0nAqrXO8l',
    'BIGipServerpassport':'837288202.50215.0000',
    'current_captcha_type':'C'
}

redis_conn = redis.Redis(host='10.15.1.11', port=6379, db=0)

class StationSpider(scrapy.Spider):
    name = "train_information"
    allowed_domains = ["12306.cn"]

    # start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9026']

    def start_requests(self):
        data = db.query('select distinct abbreviation_12306 from t_spider_12306_station;')
        data_list = []
        for d in data:
            data_list.append(d.get('abbreviation_12306'))
        for dl in data_list:
            for dj in data_list:
                url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
                time.strftime('%Y-%m-%d', time.localtime(time.time())), dl, dj)
                yield Request(url, callback=self.parse, meta={'search_start': dl, 'search_end': dj, 'url': url},
                              headers=header, dont_filter=True,cookies=Cookie)
                # dl = 'BJP'
                # dj = 'SHH'
                # url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=' \
                #       '%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
                #           task_date, dl, dj)
                # yield Request(url, callback=self.parse, meta={'search_start': dl, 'search_end': dj})

    def parse(self, response):
        content = response.body
        meta = response.meta
        try:
            content_json = json.loads(content)
            data = content_json.get('data')

            if data:
                result = data.get('result')
                if result:
                    for r in result:
                        r_list = r.split('|')
                        train_number = r_list[2]
                        if redis_conn.hsetnx('train_number', train_number, ''):
                            train_start = r_list[4]
                            train_end = r_list[5]
                            meta['train_number'] = train_number
                            meta['train_start'] = train_start
                            meta['train_end'] = train_end
                            url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=' \
                                  '%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s' % (
                                      train_number, train_start, train_end, task_date)
                            meta['url'] = url
                            yield Request(url, callback=self.parse_train, meta=meta, headers=header, dont_filter=True,cookies=Cookie)
        except:
            url = meta['url']
            yield Request(url, callback=self.parse, meta=meta, headers=header, dont_filter=True,cookies=Cookie)

    def parse_train(self, response):
        meta = response.meta
        try:
            content_json = json.loads(response.body)
            data = content_json.get('data')

            if data:
                data = data.get('data')
                for d in data:
                    item = TrainInfomationItem()
                    item['search_start'] = meta['search_start']
                    item['search_end'] = meta['search_end']
                    item['train_number'] = meta['train_number']
                    item['train_start'] = meta['train_start']
                    item['train_end'] = meta['train_end']
                    for key, val in d.items():
                        item[key] = val
                    yield item
        except:
            url = meta['url']
            yield Request(url, callback=self.parse_train, meta=meta, headers=header, dont_filter=True,cookies=Cookie)
