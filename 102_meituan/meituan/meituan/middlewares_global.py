# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import time
import web
from scrapy import signals

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

class ProxyMiddleware(object):

    def __init__(self):
        self.proxys = ''

    def process_request(self, request, spider):
        if not self.proxys:
            self.proxys = self.__get_proxy(spider)
        if self.proxys:
            proxy = random.choice(self.proxys)
            if not divmod(int(time.time()), 5)[1]:
                self.proxys = self.__get_proxy(spider)
            request.meta['proxy'] = "%s" % proxy
            request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

    def __get_proxy(self, spider):

        data = db.query('''select ip from t_spider_proxy''')
        if data:
            proxy_res = []
            for item in data:
                proxy_res.append('http://' + item['ip'])
                # print item['url']
            return proxy_res
        return []
