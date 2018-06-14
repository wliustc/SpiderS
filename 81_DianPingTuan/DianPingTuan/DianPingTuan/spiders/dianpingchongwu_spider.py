# -*- coding: utf-8 -*-
import json

import scrapy
import time

import redis
from scrapy.selector import Selector
from scrapy import Request
import sys
import web, re
from scrapy_redis.spiders import RedisSpider
from DianPingTuan.items import PetServicesItem

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
dt = time.strftime('%Y-%m-%d', time.localtime())

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}
redis_ = redis.Redis(host='10.15.1.11', port=6379)

class DianpingtuanSpider(RedisSpider):
    name = "pet_services_spider"
    allowed_domains = ["dianping.com"]
    redis_key = 'dianping:chongwu6'
    # start_urls = ['http://t.dianping.com/citylist']

    def spider_idle(self):
        self.schedule_next_requests()

    def make_requests_from_url(self, url):
        try:
            meta = json.loads(url)
            meta['error_times'] = 0
            detail_url = meta['detail_url']
            return Request(url=str(detail_url), callback=self.parse_detail, meta=meta,
                          headers=header,dont_filter=True,errback=self.parse_failure)
        except Exception,e:
            print e

    def parse(self, response):
        pass



    def parse_detail(self, response):
        item = PetServicesItem()
        # sel = Selector(response)
        content = response.body
        deal_id = ''.join(re.findall('dealGroupId:(\d+),', content))
        # category = ''.join(re.findall("category:'(.*?)'", content))
        title = ''.join(re.findall("shortTitle:'(.*?)'", content))
        #new_price = re.findall('"price":(\d+),', content)
        new_price = re.findall('Price-font buy-bottom-price">&#165;(.*?)</div>', content)
        if new_price:
            new_price = new_price[0]
        else:
            new_price = ''
        #old_price = re.findall('"marketPrice":(\d+),', content)
        old_price = re.findall('<td class="Price-font">[\s\S]*?;([\s\S]*?)</td>', content)
        if old_price:
            old_price = old_price[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t','')
        #sales = re.findall('J_current_join">(\d+)<', content)
        sales = re.findall('<span class="J_dealCount">([\s\S]*?)</span>', content)
        if sales:
            sales = sales[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('份','').replace('\t','')
        start_time = ''.join(re.findall("beginDate:'(.*?)'", content))
        end_time = ''.join(re.findall("endDate:'(.*?)'", content))
        description = ''.join(
            re.findall('summary summary-comments-big J_summary Fix[\s\S]*?<div class="bd">([\s\S]*?)</h2>', content))
        description = re.sub('<.*?>', '', description)
        description = description.replace('\n', '').replace('\r', '').replace(' ', '')
        city_id = response.meta['city_id']
        city_name = response.meta['city_name']
        shop_id = response.meta['shop_id']
        item['dt'] = dt
        item['deal_id'] = deal_id
        item['category'] = '宠物服务'
        item['title'] = title
        item['new_price'] = new_price
        item['old_price'] = old_price
        item['sales'] = sales
        item['start_time'] = start_time
        item['end_time'] = end_time
        item['description'] = description
        item['city_id'] = city_id
        item['shop_id'] = shop_id
        item['city_name'] = city_name
		
        yield item

    def parse_failure1(self, failure):
        meta = failure.request.meta
        meta['retry_times'] = 0
        error_resion = failure.value
        if 'Connection refused' in str(error_resion) or 'timeout' in str(
                error_resion) or 'Could not open CONNECT tunnel with proxy' in str(error_resion):
            url = failure.request.url
            if 'deal' in url:
                yield Request(url, callback=self.parse_detail, errback=self.parse_failure, meta=meta,
                              headers=header)
        else:

            try:
                error_resion = failure.value.response._body
                if 'aboutBox errorMessage' in error_resion:
                    pass
                else:
                    url = failure.request.url
                    if 'deal' in url:
                        yield Request(url, callback=self.parse_detail, errback=self.parse_failure,
                                      meta=meta, headers=header)

            except Exception, e:
                print e

    def parse_failure(self, failure):
        meta = failure.request.meta
        #meta['retry_times'] = 0
        error_times = meta['error_times']
        if error_times<30:
            meta['error_times'] = error_times+1
            error_resion = failure.value
            redis_.hset('dianping:error_resion', str(error_resion)[:38], '1')
            # if 'Connection refused' in str(error_resion) or 'timeout' in str(
            #         error_resion) or 'Could not open CONNECT tunnel with proxy' in str(error_resion):
            url = failure.request.url
            if 'deal' in url:
                yield Request(url, callback=self.parse_detail, errback=self.parse_failure, meta=meta,
                              headers=header,dont_filter=True)

    
    
    
    
    
    
    
    
    