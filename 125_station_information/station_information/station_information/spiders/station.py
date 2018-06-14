# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
from scrapy import Request
from scrapy.selector import Selector
import re
from station_information.items import StationInformationItem


class StationSpider(scrapy.Spider):
    name = "station"
    allowed_domains = ["12306.cn"]
    start_urls = ['http://www.12306.cn/mormhweb/kyyyz/']

    # def start_requests(self):
    #     url = 'http://www.12306.cn/mormhweb/kyyyz/'
    #     yield Request(url)

    def parse(self, response):
        # sel = Selector(response)
        content = response.body
        station_name_list = re.findall('<td class="sec\d+".*?onClick=".*?">(.*?)</td>', content)
        station_info_link_list = re.findall('href="(.*?)" target="frameCon" title="客运站数据\(车站\)"', content)
        for index, station_info_link in enumerate(station_info_link_list):
            print station_info_link
            url = urljoin(response.url, station_info_link)
            print url
            yield Request(url, callback=self.parse_detail, meta={'station_name': station_name_list[index]})

    def parse_detail(self, response):
        item = StationInformationItem()
        content = response.body
        meta = response.meta
        item['content'] = content
        item['meta'] = meta
        yield item
