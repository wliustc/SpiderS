# -*- coding: utf-8 -*-
import scrapy
import json
from weather_report.items import WeatherReportNmcCityItem

class NmcSpider(scrapy.Spider):
    name = "nmc_city"
    allowed_domains = ["nmc.cn"]
    start_urls = ['http://www.nmc.cn/f/rest/province']

    def parse(self, response):
        data_json = json.loads(response.body)
        if data_json:
            for data in data_json:
                province_code = data.get('code')
                province_name = data.get('name')
                province_url = data.get('url')
                url = 'http://www.nmc.cn/f/rest/province/'+province_code
                yield scrapy.Request(url,callback=self.parse_city,
                                     meta={'province_code':province_code,
                                           'province_name':province_name,
                                           'province_url':province_url})

    def parse_city(self, response):
        data_json = json.loads(response.body)
        meta = response.meta
        if data_json:
            for data in data_json:
                item = WeatherReportNmcCityItem()
                item['city_code'] = data.get('code')
                item['city_name'] = data.get('city')
                item['city_url'] = data.get('url')
                item['province_code'] = meta.get('province_code')
                item['province_name'] = meta.get('province_name')
                item['province_url'] = meta.get('province_url')
                item['sign'] = 1
                yield item


    
    