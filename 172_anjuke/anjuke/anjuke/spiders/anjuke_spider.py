# -*- coding: utf-8 -*-
import scrapy
import json
import re
from anjuke.items import AnjukeItem

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


class Anjuke_Spider(scrapy.Spider):

    name = 'anjuke_spider'

    custom_settings = {
      'DOWNLOADER_MIDDLEWARES': {'anjuke.middlewares_mine.ProxyMiddleware': 100,
                                'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110}
    }

    def start_requests(self):
        url = 'https://www.anjuke.com/sy-city.html'

        yield scrapy.Request(url, headers=header, callback=self.city_parse, dont_filter=True)

    def city_parse(self, response):
        if 'antispam' in response.url:
            url = 'https://www.anjuke.com/sy-city.html'
            yield scrapy.Request(url, headers=header, callback=self.city_parse, dont_filter=True)
        else:
            content = response.body
            city_con = re.findall('<p class="title">([\s\S]*?)id="footer"', content)[0]
            city_info = re.findall('<a href="https://(.*?)\.anjuke\.com.*?>(.*?)<', city_con)
            for info in city_info:
                # print info[0], info[1]
                city = info[1]
                city_en = info[0]
                url = 'https://{}.zu.anjuke.com/'.format(city_en)
                yield scrapy.Request(url, headers=header, meta={'city': city, 'city_en': city_en}, dont_filter=True, callback=self.area_parse)

    def area_parse(self, response):
        city_en = response.meta['city_en']
        city = response.meta['city']
        if 'antispam' in response.url:
            url = 'https://{}.zu.anjuke.com/'.format(city_en)
            yield scrapy.Request(url, headers=header, meta={'city': city, 'city_en': city_en}, dont_filter=True,
                                 callback=self.area_parse)
        else:
            content = response.body
            city = response.meta['city']
            area_con = re.findall('title="全部租房"([\s\S]*?)</span>', content)[0]
            area_info = re.findall('<a href="(.*?)"[\s\S]*?>(.*?)<', area_con)
            for info in area_info:
                area = info[1]
                page = 1
                area_url = info[0]
                url = area_url + 'p{}/'.format(page)
                yield scrapy.Request(url, headers=header, callback=self.detail_parse, meta={
                    'city': city, 'area': area, 'page': page, 'area_url': area_url}, dont_filter=True)

    def detail_parse(self, response):
        items = AnjukeItem()
        content = response.body
        area_url = response.meta['area_url']
        page = response.meta['page']
        city = response.meta['city']
        area = response.meta['area']
        if 'antispam' in response.url:
            url = area_url + 'p{}/'.format(page)
            yield scrapy.Request(url, headers=header, callback=self.detail_parse, meta={
                'city': city, 'area': area, 'page': page, 'area_url': area_url}, dont_filter=True)
        else:
            house_info = re.findall('<div class="zu-info">([\s\S]*?)</div>', content)
            for info in house_info[:-1]:
                pattern = re.search('title="([\s\S]*?)"[\s\S]*?href="(.*?)"', info)
                title = pattern.group(1)
                link = pattern.group(2)
                items['city'] = city
                items['area'] = area
                items['title'] = title
                items['link'] = link
                yield items
            if 'aNxt' in content:
                page += 1
                url = area_url + 'p{}/'.format(page)
                yield scrapy.Request(url, headers=header, callback=self.detail_parse, meta={
                    'city': city, 'area': area, 'page': page, 'area_url': area_url}, dont_filter=True)