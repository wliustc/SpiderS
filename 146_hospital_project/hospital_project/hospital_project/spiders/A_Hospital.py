# -*- coding: utf-8 -*-
import scrapy
from hospital_project.items import HospitalProjectItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AHospitalSpider(scrapy.Spider):
    name = 'A-Hospital'
    allowed_domains = ['www.a-hospital.com']
    start_urls = ['http://www.a-hospital.com/w/全国医院列表']

    def parse(self, response):
        '''
            1.获取所有省份以及省份的url地址
        '''
        # 获取到所有的省份
        hospital_province_list = response.xpath('//div[@id="bodyContent"]/h3/span/text()').extract()
        hospital_link_list = response.xpath('//div[@id="bodyContent"]/p/b/a/@href').extract()
        for hospital_province, hospital_link in zip(hospital_province_list, hospital_link_list):
            base_url = 'http://www.a-hospital.com' + hospital_link
            yield scrapy.Request(base_url, meta={'hospital_province': hospital_province}, callback=self.parse_url)

    def parse_url(self, response):
        '''
             获取到市或者直辖市下面的区域
        '''

        hospital_city_link_list = response.xpath('//div[@id="bodyContent"]/p[3]/a/@href').extract()
        hospital_list = response.xpath('//div[@id="bodyContent"]/p[3]/a/text()').extract()
        pos = response.xpath('//div[@id="content"]/h1/text()').extract_first()
        if '市' in pos:
            for link, hospital_county in zip(hospital_city_link_list, hospital_list):
                base_url = 'http://www.a-hospital.com' + link
                response.meta['hospital_city'] = response.meta['hospital_province']
                #  所在辖区
                response.meta['hospital_county'] = hospital_county
                yield scrapy.Request(base_url, meta=response.meta, callback=self.parse_data)
        elif '省' in pos:
            for link, hospital_city in zip(hospital_city_link_list, hospital_list):
                base_url = 'http://www.a-hospital.com' + link
                # 所在市
                response.meta['hospital_city'] = hospital_city
                yield scrapy.Request(base_url, meta=response.meta, callback=self.parse_item)

    def parse_item(self, response):
        '''
            获取省市下面所在辖区
        '''
        hospital_county_list = response.xpath('//div[@id="bodyContent"]/ul[1]/li/a/text()').extract()
        hospital_county_link_list = response.xpath('//div[@id="bodyContent"]/ul[1]/li/a/@href').extract()
        for hospital_county, link in zip(hospital_county_list, hospital_county_link_list):
            response.meta['hospital_county'] = hospital_county
            base_url = 'http://www.a-hospital.com' + link
            yield scrapy.Request(base_url, meta=response.meta, callback=self.parse_data)

    def parse_data(self, response):
        '''
            获取医院名称以及详情页的链接
        '''
        link_list = response.xpath('//div[@id="bodyContent"]/ul/li/b/a/@href').extract()
        # 医院名称
        hospital_name_list = response.xpath('//div[@id="bodyContent"]/ul/li/b/a/text()').extract()
        for link, hospital_name in zip(link_list, hospital_name_list):
            base_url = 'http://www.a-hospital.com' + link
            response.meta['hospital_name'] = hospital_name
            yield scrapy.Request(base_url, meta=response.meta, callback=self.parse_hospital)

    def parse_hospital(self, response):
        '''
            获取所有的数据
        '''
        item = HospitalProjectItem()

        hospital_addrs = response.xpath('//*[@id="bodyContent"]/ul[1]/li[1]/text()').extract()
        if hospital_addrs != None:
            item['hospital_addrs'] = hospital_addrs[0][1:]
        # 医院名称
        item['hospital_name'] = response.meta['hospital_name']
        # 医院别名
        alias = response.xpath('//*[@id="bodyContent"]/p/b/text()').extract_first()
        if '（' in alias:
            alias = alias.split('（')[1]
            item['hospital_alias'] = alias[0:-1]
        else:
            item['hospital_alias'] = None
        # item['hospital_alias'] = response.meta['hospital_alias']
        # 所在省份
        item['hospital_province'] = response.meta['hospital_province']
        # 所在城市
        item['hospital_city'] = response.meta['hospital_city']
        # 所在辖区
        item['hospital_county'] = response.meta['hospital_county']
        # 医院等级
        item['hospital_grade'] = response.xpath('//*[@id="bodyContent"]/ul[1]/li[3]/a/text()').extract_first()
        # 电话
        hospital_phone = response.xpath('//*[@id="bodyContent"]/ul[1]/li[2]/text()').extract()
        if hospital_phone != None:
            item['hospital_phone'] = hospital_phone[0][1:]
        # 经营方式
        item['business_practice'] = response.xpath('//*[@id="bodyContent"]/ul[1]/li[6]/a/text()').extract_first()
        # 数据来源
        item['data_source'] = 'A-Hospital'
        print item
        yield item

    
    
    
    
    
    