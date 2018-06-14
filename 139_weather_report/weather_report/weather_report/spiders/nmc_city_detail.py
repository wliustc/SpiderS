# -*- coding: utf-8 -*-

import scrapy
import web
from scrapy import Selector
import re
from weather_report.items import WeatherReportNmcDetailItem
import datetime

header = {
    'Host': 'www.nmc.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class NmcSpider(scrapy.Spider):
    name = "nmc_detail"
    allowed_domains = ["nmc.cn"]
    start_urls = ['http://www.nmc.cn/f/rest/province']

    def start_requests(self):
        data = db.query(
            'select distinct city_url from t_spider_weather_report_nmc_city where sign=1 and city_code="54511";')
        if data:
            d_city_url = data[0].get('city_url')
            detail_url = 'http://www.nmc.cn' + d_city_url
            yield scrapy.Request(detail_url, callback=self.parse_check, headers=header,dont_filter=True)

    def parse_check(self, response):
        sel = Selector(response)
        data = sel.xpath('//div[@class="btitle"]/span/text()').extract()
        data = ''.join(data)
        data = ''.join(re.findall('\d+-\d+-\d+', data))
        if str(data) == str(self.getYesterday()):
            data = db.query(
                'select distinct city_url,city_code from t_spider_weather_report_nmc_city where sign=1;')
            if data:
                for d in data:
                    city_code = d.get('city_code')
                    city_url = d.get('city_url')
                    detail_url = 'http://www.nmc.cn' + city_url
                    print detail_url
                    yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'city_code': city_code, },
                                         headers=header,dont_filter=True)

    def parse_detail(self, response):
        item = WeatherReportNmcDetailItem()
        city_code = response.meta['city_code']
        detail_content = response.body
        meta = {'city_code': city_code, 'detail_content': detail_content}
        item['meta'] = meta
        yield item

    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        # print type(str(yesterday))
        return yesterday
