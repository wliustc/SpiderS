# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import time
from scrapy.utils.project import get_project_settings
from scrapy import signals
import web
settings = get_project_settings()


import redis
import json

class DianpingtuanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

class ProxyMiddleware(object):
    # overwrite process request
    # def process_request(self, request, spider):
    #     # Set the location of the proxy
    #
    #     request.meta['proxy'] = "http://122.142.77.85:80"

        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
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
            ua = random.choice(settings.get('USER_AGENT_LIST'))
            request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            if ua:
                request.headers['User-Agent'] = ua
            # request.meta['proxy'] = 'http://1.1.1.1:1'
        # print "******request:%s\t\t\t\turl:%s" % (request.meta['proxy'],request.url)

    def _get_proxy(self, spider):
        domain = getattr(spider, 'allowed_domains', None)
        if domain:
            data = db.query('''select url from t_hh_proxy_list where domain ="{}"
                and valid>0 order by update_time desc'''.format(domain[0]))
            if data:
                proxy_res = []
                for item in data:
                    proxy_res.append(item['url'])
                    # print item['url']
                return proxy_res
        return []


    def redis_conn(self,spider):
        r = redis.Redis(host='117.122.192.50', port=6479, db=0)
        data = r.smembers('proxy:iplist5')
        if data:
            proxy_res = []
            for d in data:
                dd = json.loads(d)
                proxy_res.append('http://'+str(dd['ip']))
            return proxy_res
        return []

    def __get_proxy(self, spider):
        # domain = getattr(spider, 'allowed_domains', None)

        data = db.query('''select ip from t_spider_proxy''')
        if data:
            proxy_res = []
            for item in data:
                proxy_res.append('http://' + item['ip'])
                # print item['url']
            return proxy_res
        return []