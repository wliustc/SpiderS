# -*- coding: utf-8 -*-
import json

import scrapy
import time
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
import sys
import web, re
from DianPingTuan.items import PetServicesItem
from scrapy_redis.spiders import RedisSpider
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
dt = time.strftime('%Y-%m-%d', time.localtime())

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}

# redis_ = redis.Redis(host='127.0.0.1', port=6679)
redis_ = redis.Redis(host='10.15.1.11', port=6379)


class DianpingtuanSpider(scrapy.Spider):
    name = "meishi_job"
    allowed_domains = ["dianping.com"]

    # start_urls = ['http://t.dianping.com/citylist']


    def start_requests(self):
        data = db.query(
            "select distinct city_id,city_name,district_id,district_name from t_hh_dianping_business_area where city_name in ('武汉','长沙','南昌','成都','北京','广州','上海','深圳','苏州','重庆','合肥','兰州','吉林','贵阳','郑州','襄阳','常德','九江','开封','乐山');")
        for d in data:
            city_id = d.city_id
            city_name = d.city_name
            district_id = d.district_id
            district_name = d.district_name
            # print city_id, city_name, district_id, district_name
            url = 'https://www.dianping.com/search/category/%s/10/g223r%s' % (city_id,district_id)
            # print url
            yield Request(url, callback=self.parse,
                          meta={'city_id': city_id, 'city_name': city_name, 'district_id': district_id,
                                'district_name': district_name, 'page': 1, 'failure_time': 0,'category':'snack'},
                          dont_filter=True, headers=header, errback=self.parse_failure)
            url = 'https://www.dianping.com/search/category/%s/20/g33759r%s' % (city_id, district_id)
            yield Request(url, callback=self.parse,
                          meta={'city_id': city_id, 'city_name': city_name, 'district_id': district_id,
                                'district_name': district_name, 'page': 1, 'failure_time': 0, 'category': 'health'},
                          dont_filter=True, headers=header, errback=self.parse_failure)
        # yield Request('https://www.dianping.com/search/category/2/10/g223',callback=self.parse,errback=self.parse_failure,meta={'city_id': '2', 'city_name': '北京', 'district_id': '14',
        #                         'district_name': '朝阳','page':1, 'failure_time': 0,})

    def parse(self, response):
        page = response.meta['page']
        sel = Selector(response)
        deal_links = sel.xpath('//div[@class="txt"]/div[@class="tit"]/a/@href')
        meta = response.meta
        meta['retry_times'] = 0
        if deal_links:
            for deal_link in deal_links:
                detail_url = urljoin(response.url, ''.join(deal_link.extract()))
                meta['detail_url'] = detail_url
                url_meta = json.dumps(meta)
                if meta['category']=='snack':
                    redis_.lpush('dianping:meishi_snack', url_meta)
                elif meta['category'] == 'health':
                    redis_.lpush('dianping:meishi_health', url_meta)
                # __redis.lpush(detail_url)
                # yield Request(detail_url, callback=self.parse_detail, meta=meta, dont_filter=True,
                #               headers=header, errback=self.parse_failure)
        if page == 1:
            # 找到最有一页的页码，比对是否为当前页
            next_page = ''.join(sel.xpath('//a[@class="PageLink"][last()]/@title').extract())
            if next_page:
                # print next_page
                if int(next_page) == page:
                    pass
                else:
                    for i in xrange(2, int(next_page) + 1):
                        meta['page'] = i
                        next_page_link = response.url + 'p%s' % i
                        yield Request(next_page_link, callback=self.parse, meta=meta, dont_filter=True, headers=header,
                                      errback=self.parse_failure)

    def parse_failure1(self, failure):
        meta = failure.request.meta
        meta['retry_times'] = 0
        failure_time = meta['failure_time']
        if failure_time < 5:
            meta['failure_time'] += 1
            error_resion = failure.value
            redis_.hset('dianping:error_resion', str(error_resion)[:38], '1')
            if 'Connection refused' in str(error_resion) or 'timeout' in str(
                    error_resion) or 'Could not open CONNECT tunnel with proxy' in str(
                error_resion) or 'TCP connection timed out' in str(error_resion) or 'twisted' in str(error_resion):
                # print type(error_resion)
                url = failure.request.url
                if 'search' in url:
                    yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True, meta=meta,
                                  headers=header)
            else:
                try:
                    error_resion = failure.value.response._body
                    if 'aboutBox errorMessage' in error_resion or '没有找到相应的商户' in error_resion:
                        print error_resion
                        print error_resion
                        print error_resion
                        print error_resion
                    else:
                        url = failure.request.url
                        if 'search' in url:
                            yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True,
                                          meta=meta,
                                          headers=header)
                except Exception, e:
                    print e

    def parse_failure(self, failure):
        meta = failure.request.meta
        meta['retry_times'] = 0
        failure_time = meta['failure_time']
        if failure_time < 50:
            meta['failure_time'] += 1
            try:
                error_resion = failure.value
                redis_.hset('dianping:error_resion', str(error_resion)[:38], '1')
                error_resion = failure.value.response._body
                # if 'aboutBox errorMessage' in error_resion or '您要查看的内容不存在' in error_resion:
                if '您要查看的内容不存在' in error_resion:
                    # print error_resion
                    print '========================='
                    print failure.value.response.url
                    redis_.hset('dianping:bucunzai', failure.value.response.url, '1')
                    print '========================='
                    # print error_resion
                    # print error_resion
                    # print error_resion
                else:
                    url = failure.request.url
                    if 'search' in url:
                        yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True,
                                      meta=meta,
                                      headers=header)
            except Exception, e:
                url = failure.request.url
                if 'search' in url:
                    yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True,
                                  meta=meta,
                                  headers=header)
