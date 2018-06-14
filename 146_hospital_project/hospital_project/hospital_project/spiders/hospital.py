# -*- coding: utf-8 -*-
import scrapy
from hospital_project.items import HospitalProjectItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class HospitalSpider(scrapy.Spider):
    name = 'hospital'
    allowed_domains = ['db.yaozh.com']
    p = 1
    url = 'https://db.yaozh.com/hmap?p='
    start_urls = [url + str(p)]

    def parse(self, response):
        # 获取详情页的url地址
        links = response.xpath('//table/tbody/tr/th/a/@href').extract()
        for link in links:
            base_url = 'https://db.yaozh.com' + link
            yield scrapy.Request(base_url, callback=self.parse_item)
        if self.p <= 10:
            self.p += 1
            yield scrapy.Request(self.url + str(self.p), callback=self.parse)

    def parse_item(self, response):
        '''
            获取所需要的数据
        '''
        item = HospitalProjectItem()
        ths = response.xpath('//div[@class="table-wrapper"]/table/tbody/tr/th/text()').extract()
        tds = response.xpath('//div[@class="table-wrapper"]/table/tbody/tr/td/span/text()').extract()
        for th, td in zip(ths, tds):
            if th == '医院名称':
                item['hospital_name'] = td.strip()
            elif th == '医院等级':
                item['hospital_grade'] = td.strip()
            elif th == '医院别名':

                item['hospital_alias'] = td.strip()

            elif th == '省':
                item['hospital_province'] = td.strip()
            elif th == '市':
                item['hospital_city'] = td.strip()
            elif th == '县':
                item['hospital_county'] = td.strip()
            elif th == '医院地址':
                item['hospital_addrs'] = td.strip()
            elif th == '经营方式':
                item['business_practice'] = td.strip()

            elif th == '电话':
                item['hospital_phone'] = td.strip()
            elif 'hospital_alias' not in item:
                item['hospital_alias'] = None
            elif 'hospital_phone' not in item:
                item['hospital_phone'] = None
            elif 'business_practice' not in item:
                item['business_practice'] = None
        item['data_source'] = '药智网'
        yield item

    