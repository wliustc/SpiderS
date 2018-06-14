# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.selector import Selector
from scrapy import Request
from urlparse import urljoin
import sys
import web, re
from DianPingTuan.items import PetServicesItem

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
dt = time.strftime('%Y-%m-%d', time.localtime())

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}


class DianpingtuanSpider(scrapy.Spider):
    name = "pet_services"
    allowed_domains = ["dianping.com"]

    # start_urls = ['http://t.dianping.com/citylist']


    def start_requests(self):
        data = db.query('select distinct city_id,city_name from t_hh_dianping_business_area;')
        for d in data:
            city_id = d.city_id
            city_name = d.city_name
            print city_id, city_name
            url = 'https://www.dianping.com/search/category/%s/95/m3' % city_id
            yield Request(url, callback=self.parse, meta={'city_id': city_id, 'city_name': city_name, 'page': 1},
                          dont_filter=True, headers=header, errback=self.parse_failure)
            # yield Request('https://www.dianping.com/search/category/1/95/m3', callback=self.parse,
            #               meta={'city_id': 1, 'city_name': '上海','retry_times':0})
            # yield Request('http://t.dianping.com/deal/19767107', callback=self.parse_detail,
            #               meta={'city_id': 7, 'city_name': '深圳'})
            # yield Request('https://www.dianping.com/search/category/2/95/m3',meta={'city_id': 7, 'city_name': '深圳','page':1},errback=self.parse_failure,callback=self.parse)

    def parse(self, response):
        page = response.meta['page']

        sel = Selector(response)
        deal_links = sel.xpath('//div[@class="svr-info"]/div/a[@target]/@href')
        meta = response.meta
        meta['retry_times'] = 0
        if deal_links:
            for deal_link in deal_links:
                detail_url = urljoin(response.url, ''.join(deal_link.extract()))
                yield Request(detail_url, callback=self.parse_detail, meta=meta, dont_filter=True,
                              headers=header, errback=self.parse_failure)
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

    def parse_detail(self, response):
        item = PetServicesItem()
        # sel = Selector(response)
        content = response.body
        deal_id = ''.join(re.findall('dealGroupId:(\d+),', content))
        # category = ''.join(re.findall("category:'(.*?)'", content))
        title = ''.join(re.findall("shortTitle:'(.*?)'", content))
        new_price = re.findall('"price":(\d+),', content)
        if new_price:
            new_price = new_price[0]
        old_price = re.findall('"marketPrice":(\d+),', content)
        if old_price:
            old_price = old_price[0]
        sales = re.findall('J_current_join">(\d+)<', content)
        if sales:
            sales = sales[0]
        start_time = ''.join(re.findall("beginDate:'(.*?)'", content))
        end_time = ''.join(re.findall("endDate:'(.*?)'", content))
        description = ''.join(
            re.findall('summary summary-comments-big J_summary Fix[\s\S]*?<div class="bd">([\s\S]*?)</h2>', content))
        description = re.sub('<.*?>', '', description)
        description = description.replace('\n', '').replace('\r', '').replace(' ', '')
        city_id = response.meta['city_id']
        city_name = response.meta['city_name']
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
        item['city_name'] = city_name

        yield item

    def parse_failure(self, failure):
        meta = failure.request.meta
        meta['retry_times'] = 0
        error_resion = failure.value
        if 'Connection refused' in str(error_resion) or 'timeout' in str(
                error_resion) or 'Could not open CONNECT tunnel with proxy' in str(error_resion):
            # print type(error_resion)
            url = failure.request.url
            if 'search' in url:
                yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True, meta=meta,
                              headers=header)
            elif 'deal' in url:
                yield Request(url, callback=self.parse_detail, errback=self.parse_failure, dont_filter=True, meta=meta,
                              headers=header)
        else:

            try:
                error_resion = failure.value.response._body
                if 'aboutBox errorMessage' in error_resion:
                    pass
                else:
                    url = failure.request.url
                    if 'search' in url:
                        yield Request(url, callback=self.parse, errback=self.parse_failure, dont_filter=True, meta=meta,
                                      headers=header)
                    elif 'deal' in url:
                        yield Request(url, callback=self.parse_detail, errback=self.parse_failure, dont_filter=True,
                                      meta=meta, headers=header)

            except Exception, e:
                print e
