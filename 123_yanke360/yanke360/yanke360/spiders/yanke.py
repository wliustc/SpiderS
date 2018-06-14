# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
from scrapy.selector import Selector
from yanke360.items import Yanke360Item


class YankeSpider(scrapy.Spider):
    name = "yanke"
    allowed_domains = ["yanke360.com"]
    start_urls = ['http://www.yanke360.com/hospital/']

    def parse(self, response):
        sel = Selector(response)
        eye_list = sel.xpath('//ul[@class="eye_list"]')
        province_list = eye_list.xpath('./li/span/a/text()').extract()
        city_list = eye_list.xpath('./div')
        for index, province in enumerate(province_list):
            # print province
            c_list = city_list[index].xpath('./p/a')
            for c in c_list:
                c_id = c.xpath('./@id').extract_first()
                c_href = c.xpath('./@href').extract_first()
                title = c.xpath('./@title').extract_first()
                # print c_id
                # print c_href
                # print title
                yield scrapy.Request(url=urljoin(response.url, c_href), callback=self.parse_hospital_list,
                                     meta={'province': province, 'c_id': c_id, 'c_href': c_href, 'title': title})
        # yield scrapy.Request(url='http://www.yanke360.com/7975326d-743f-992b-3089-de0110024f19/', callback=self.parse_hospital_list,
        #                      meta={'province': '', 'c_id': '', 'c_href': '', 'title': ''})


    def parse_hospital_list(self, response):
        sel = Selector(response)
        meta = response.meta
        hospital_list = sel.xpath('//div[@class="hospital"]/ul/li/a')
        if hospital_list:
            for hospital in hospital_list:
                hospital_detail_url = hospital.xpath('./@href').extract_first()
                hospital_name = hospital.xpath('./text()').extract_first()
                # print hospital_detail_url
                # print hospital_name
                
                meta['hospital_name'] = hospital_name
                meta['hospital_detail_url'] = hospital_detail_url
                yield scrapy.Request(url=urljoin(response.url,hospital_detail_url), callback=self.parse_detail, meta=meta)
            next_page = sel.xpath('//div[@class="page"]/a[1]/text()').extract_first()
            print next_page
            if next_page:
                if next_page==u'下一页 ':
                    c_href = sel.xpath('//div[@class="page"]/a[1]/@href').extract_first()
                    yield scrapy.Request(url=urljoin(response.url, c_href),
                                         callback=self.parse_hospital_list,
                                         meta=meta)

    def parse_detail(self, response):
        meta = response.meta
        content = response.body
        item = Yanke360Item()
        item['meta'] = meta
        item['content'] = content
        yield item
