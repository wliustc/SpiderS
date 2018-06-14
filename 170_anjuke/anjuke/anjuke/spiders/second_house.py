# -*- coding: utf-8 -*-
import scrapy
# import random
import sys
# import re
import web
from anjuke.items import AnjukeItem
from scrapy.http.request import Request
import time

reload(sys)
sys.setdefaultencoding('utf-8')

# db = web.database(dbn='mysql', db='anjuke', user='root', pw='110707', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))


class SecondHouseSpider(scrapy.Spider):
    name = 'second_house'
    # start_urls = ['https://cangzhou.anjuke.com/sale/xinhuaa/p30/#filtersort']
    # handle_httpstatus_list = [301, 302]
    # def start_requests(self):
        # url = 'https://cangzhou.anjuke.com/sale/botouab/p33/#filtersort'
        # yield Request(url, meta={'url': url}, callback=self.parse, dont_filter=True)
    
    def start_requests(self):
        sql = '''select city_name, base_url from t_spider_anjuke_city;'''
        for i in db.query(sql):
            url = i.get('base_url')
            city_name = i.get('city_name')
            url = url + '/'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }

            yield Request(url, meta={'url': url, 'city_name': city_name}, headers=headers, callback=self.parse,
                          dont_filter=True)

    def parse(self, response):
        meta = response.meta
        if 'callback' not in response.url and response.status == 200:
            url_list = response.xpath('//div[@class="items"][1]/span[@class="elems-l"]/a')
            if url_list:
                for li in url_list:
                    city_name = meta.get('city_name')
                    url = li.xpath('./@href').extract()
                    url = ''.join(url)
                    area = li.xpath('./text()').extract()
                    area = ''.join(area)
                    yield scrapy.Request(url, meta={'city_name': city_name, 'url': url, 'area': area},
                                         callback=self.parse_data, dont_filter=True)

        else:
            url = meta.get('url')
            city_name = meta.get('city_name')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name}, callback=self.parse,
                                     dont_filter=True)

    def parse_data(self, response):
        meta = response.meta
        if 'callback' not in response.url and response.status == 200:
            url_list = response.xpath('//div[@class="sub-items"]/a')
            if url_list:
                for li in url_list:
                    city_name = meta.get('city_name')
                    area = meta.get('area')
                    url = li.xpath('./@href').extract()
                    url = ''.join(url)
                    location = li.xpath('./text()').extract()
                    location = ''.join(location)
                    yield scrapy.Request(url,
                                         meta={'city_name': city_name, 'url': url, 'area': area, 'location': location},
                                         callback=self.parse_item, dont_filter=True)
        else:
            url = meta.get('url')
            city_name = meta.get('city_name')
            area = meta.get('area')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area},
                                     callback=self.parse_data,
                                     dont_filter=True)

    def parse_item(self, response):
        meta = response.meta
        if 'callback' not in response.url and response.status == 200:
            li = response.xpath('//ul[@id="houselist-mod-new"]/li')
            if li:
                for i in li:
                    city_name = meta.get('city_name')

                    area = meta.get('area')
                    location = meta.get('location')
                    item = AnjukeItem()
                    item['area'] = area
                    item['location'] = location
                    item['city_name'] = city_name
                
                    title = i.xpath('./div[@class="house-details"]/div/a/@title').extract()
                    base_url = i.xpath('./div[@class="house-details"]/div/a/@href').extract()
                    if base_url:
                        item['base_url'] = ''.join(base_url)
                    else:
                        item['base_url'] = ''
                    if title:
                        item['title'] = ''.join(title)
                    else:
                        item['title'] = ''
                    addr = i.xpath(
                        './div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"]/@title').extract()
                    if addr:
                        item['addr'] = ''.join(addr)
                    else:
                        item['addr'] = ''
                    sum_price = i.xpath('./div[@class="pro-price"]/span[@class="price-det"]/strong/text()').extract()
                    if sum_price:
                        item['sum_price'] = ''.join(sum_price)
                    else:
                        item['sum_price'] = ''
                    unit_price = i.xpath('./div[@class="pro-price"]/span[@class="unit-price"]/text()').extract()
                    if unit_price:
                        item['unit_price'] = ''.join(unit_price)
                    else:
                        item['unit_price'] = ''
                    item['url'] = response.url
                    item['dt'] = dt
                    yield item

            next_url = response.xpath('//div[@class="multi-page"]/a[@class="aNxt"]/@href').extract()
            if next_url:
                city_name = meta.get('city_name')
                area = meta.get('area')
                location = meta.get('location')
                url = ''.join(next_url)
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area, 'location': location},
                                     callback=self.parse_item, dont_filter=True)
        else:
            url = meta.get('url')
            city_name = meta.get('city_name')
            area = meta.get('area')
            location = meta.get('location')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area, 'location': location},
                                     callback=self.parse_item,
                                     dont_filter=True)



