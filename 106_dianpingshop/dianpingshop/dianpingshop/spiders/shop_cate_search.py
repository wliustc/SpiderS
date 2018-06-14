# -*- coding: utf-8 -*-
import json

import scrapy
import time
from scrapy.http import Request
import sys
import web, re
from dianpingshop.items import DianPIngAllStoreJson
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
dt = time.strftime('%Y-%m-%d', time.localtime())

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}


class SearchShopSpider(scrapy.Spider):
    name = "shop_cate_search"
    allowed_domains = ["dianping.com"]

    # start_urls = ['http://t.dianping.com/citylist']
    def __init__(self, search_cate='157', *args, **kwargs):
        super(SearchShopSpider, self).__init__(*args, **kwargs)
        self.search_cate = search_cate

    def start_requests(self):
        data = db.query(
            "select distinct city_id,city_name from "
            "t_hh_dianping_business_area;")

        for d in data:
            city_id = d.city_id
            city_name = d.city_name
            url = 'http://www.dianping.com/search/map/ajax/json?cityId=%s&categoryId=%s' % (city_id, self.search_cate)
            print url
            yield Request(url, callback=self.parse,
                          meta={'city_id': city_id, 'city_name': city_name, 'page': 1},
                          dont_filter=True, headers=header)

    def parse(self, response):
        page = response.meta['page']
        response_json = json.loads(response.body)
        meta = response.meta
        meta['retry_times'] = 0
        if response_json:
            shopRecordBeanList = response_json.get('shopRecordBeanList')
            if shopRecordBeanList:
                # for shopRecordBean1 in shopRecordBeanList:
                item = DianPIngAllStoreJson()
                item['response_content'] = response.body
                meta['search_kw_cate'] = self.search_cate
                item['meta'] = meta
                yield item

        if page == 1:
            # 找到最有一页的页码，比对是否为当前页
            next_page = response_json.get('pageCount')
            if next_page:
                # print next_page
                if int(next_page) == page:
                    pass
                else:
                    for i in xrange(2, int(next_page) + 1):
                        meta['page'] = i
                        next_page_link = response.url + '&page=%s' % i
                        print next_page_link
                        yield Request(next_page_link, callback=self.parse, meta=meta, dont_filter=True, headers=header)

    