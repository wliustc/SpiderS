# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import  HtmlResponse



class NoneedRequest(object):


    def process_request(self, request, spider):
        if 'noneeedrequest' in  request.meta.keys():
            return HtmlResponse(request.url, encoding='utf-8', body=None, request=request)


