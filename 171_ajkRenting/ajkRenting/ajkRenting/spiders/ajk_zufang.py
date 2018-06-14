# -*- coding: utf-8 -*-
import scrapy
import sys
import web
from ajkRenting.items import AjkrentingItem
from scrapy.http.request import Request
import time
reload(sys)
sys.setdefaultencoding('utf-8')
import re

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = time.strftime('%Y-%m-%d',time.localtime(time.time()))

class SecondHouseSpider(scrapy.Spider):
    name = 'ajk_zufang'

    def start_requests(self):
        sql = '''select city_name, base_url from t_spider_anjuke_city;'''
        for i in db.query(sql):
            url = i.get('base_url')
            city_name = i.get('city_name')
            a = re.search(r'//(.*?)\.', url)
            if a:
                a = a.group(1)
                #base_url = 'https://' + a + '.zu.anjuke.com/fangyuan/p1/'
                base_url = 'https://' + a + '.zu.anjuke.com/' + '?from=navigation'
                # headers = {
                #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                #     'Accept-Encoding': 'gzip, deflate, br',
                #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                # }
                yield Request(base_url, meta={'base_url': base_url, 'city_name': city_name},
                              #headers=headers,
                              callback=self.parse,
                              dont_filter=True)

    def parse(self, response):
        meta = response.meta
        if 'callback' not in response.url:
            url_list = response.xpath("//div[@class='items'][1]/span[@class='elems-l']/div[@class='sub-items sub-level1']/a")
            if url_list:
                for li in url_list[1:]:
                    city_name = meta.get('city_name')
                    url = li.xpath('./@href').extract()
                    url = ''.join(url)
                    area = li.xpath('./text()').extract()
                    area = ''.join(area)
                    yield scrapy.Request(url, meta={'city_name':city_name, 'url':url,'area':area}, callback=self.parse_data, dont_filter=True)
            else:
                url_list = response.xpath("//div[@class='items'][1]/span[@class='elems-l']/a")
                if url_list:
                    for li in url_list[1:]:
                        city_name = meta.get('city_name')
                        url = li.xpath('./@href').extract()
                        url = ''.join(url)
                        area = li.xpath('./text()').extract()
                        area = ''.join(area)
                        yield scrapy.Request(url, meta={'city_name': city_name, 'url': url, 'area': area},
                                             callback=self.parse_data, dont_filter=True)

        else:
            url = meta.get('base_url')
            city_name = meta.get('city_name')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name}, callback=self.parse, dont_filter=True)

    def parse_data(self, response):
        meta = response.meta
        if 'callback' not in response.url:
            url_list = response.xpath("//div[@class='sub-items sub-level1']/div[@class='sub-items sub-level2']/a")
            if url_list:
                for li in url_list:
                    city_name = meta.get('city_name')
                    area = meta.get('area')
                    url = li.xpath('./@href').extract()
                    url = ''.join(url)
                    location = li.xpath('./text()').extract()
                    location = ''.join(location)
                    yield scrapy.Request(url, meta={'city_name':city_name, 'url':url,'area':area, 'location':location}, callback=self.parse_item, dont_filter=True)

            else:
                url_list = response.xpath("//div[@class='sub-items sub-level1']/a")
                if url_list:
                    for li in url_list:
                        city_name = meta.get('city_name')
                        area = meta.get('area')
                        url = li.xpath('./@href').extract()
                        url = ''.join(url)
                        location = li.xpath('./text()').extract()
                        location = ''.join(location)
                        yield scrapy.Request(url, meta={'city_name': city_name, 'url': url, 'area': area,
                                                        'location': location}, callback=self.parse_item,
                                             dont_filter=True)

        else:
            url = meta.get('url')
            city_name = meta.get('city_name')
            area = meta.get('area')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area}, callback=self.parse_data,
                                     dont_filter=True)
    def parse_item(self, response):
        meta = response.meta
        if 'callback' not in response.url:
            li = response.xpath('//div/div[@class="zu-info"]')
            if li:
                for i in li:
                    city_name = meta.get('city_name')
                    area = meta.get('area')
                    location = meta.get('location')
                    item = AjkrentingItem()
                    item['area'] = area
                    item['location'] = location
                    item['city_name'] = city_name
                    title = i.xpath('./h3/a/text()').extract()
                    if title:
                        title = ''.join(title)
                        item['title'] = title.strip()
                    item['url'] = i.xpath("./h3/a/@href").extract_first()
                    item['dt'] = dt
                    yield item

            next_url = response.xpath('//div[@class="page-content"]/div/a[@class="aNxt"]/@href').extract_first()
            if next_url:
                city_name = meta.get('city_name')
                area = meta.get('area')
                location = meta.get('location')
                url = next_url
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area, 'location': location}, callback=self.parse_item, dont_filter=True)
        else:
            url = meta.get('url')
            city_name = meta.get('city_name')
            area = meta.get('area')
            location = meta.get('location')
            if url:
                yield scrapy.Request(url, meta={'url': url, 'city_name': city_name, 'area': area, 'location': location}, callback=self.parse_item,
                                     dont_filter=True)

    