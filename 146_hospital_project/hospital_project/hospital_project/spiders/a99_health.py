# -*- coding: utf-8 -*-
import scrapy
from hospital_project.items import HospitalProjectItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class A99HealthSpider(scrapy.Spider):
    name = '99-health'
    allowed_domains = ['yyk.99.com.cn']
    start_urls = ['http://yyk.99.com.cn/']

    def parse(self, response):
        '''
            获取到所有省份的url地址
        '''
        links = response.xpath('//div[@class="lc_right"]/div[@class="lcr_bottom"]/ul/li/a/@href').extract()
        for link in links:
            base_url = 'http://yyk.99.com.cn' + link

            yield scrapy.Request(base_url, callback=self.parse_item)

    def parse_item(self, response):
        '''
            获取省里面的全部医院
        '''
        link_list = response.xpath('//div[@class="tablist"]/ul/li/a/@href').extract()
        # 医院名称
        hospital_name_list = response.xpath('//div[@class="area_list"]/div[@class="tablist"]/ul/li/a/@title').extract()

        # print link_list
        for link, hospital_name in zip(link_list, hospital_name_list):
            hospital_name = hospital_name.strip()
            yield scrapy.Request(link, meta={'hospital_name': hospital_name}, callback=self.parse_content)

    def parse_content(self, response):
        '''
            通过xpath获取数据
        '''
        item = HospitalProjectItem()
        count = response.xpath('//div[@class="w960"]/div/p/a').extract()
        count = len(count)
        if count <= 3:
            # 所在省份
            item['hospital_province'] = response.xpath('//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first()
            # 所在城市
            item['hospital_city'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first().strip()
            # 所在辖区
            item['hospital_county'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[3]/text()').extract_first().strip()
        else:
            item['hospital_province'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first().strip()
            item['hospital_city'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[3]/text()').extract_first().strip()
            item['hospital_county'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[4]/text()').extract_first().strip()
        # 医院名称
        item['hospital_name'] = response.meta['hospital_name']
        # 医院别名
        item['hospital_alias'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[1]/span/text()').extract_first().strip()
        # 医院等级
        item['hospital_grade'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[3]/span/text()').extract_first().strip()
        # 地址
        hospital_addrs = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[5]/span/text()').extract_first()
        if hospital_addrs:
            item['hospital_addrs'] = hospital_addrs
        else:
            item['hospital_addrs'] = None
        # 电话
        item['hospital_phone'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[4]/span/@title').extract_first()
        # 经营方式
        item['business_practice'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[2]/text()').extract_first().strip()
        # 数据来源
        item['data_source'] = '99-健康网'
        yield item
