# -*- coding: utf-8 -*-
import scrapy
from hospital_project.items import HospitalProjectItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class AHospitalSpider(scrapy.Spider):
    name = 'A-Hospital'
    allowed_domains = ['www.a-hospital.com']
    start_urls = ['http://www.a-hospital.com/w/%E5%BB%BA%E5%AE%81%E5%8E%BF%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E4%B8%89%E5%8F%B0%E5%8E%BF%E5%A6%87%E5%B9%BC%E4%BF%9D%E5%81%A5%E9%99%A2'
                  ,'http://www.a-hospital.com/w/%E4%B8%89%E5%8F%B0%E5%8E%BF%E7%B2%BE%E7%A5%9E%E7%97%85%E9%99%A2',
                  'http://www.a-hospital.com/w/%E4%B8%89%E5%8F%B0%E5%8E%BF%E4%B8%AD%E5%8C%BB%E9%AA%A8%E7%A7%91%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E5%9B%9B%E5%B7%9D%E7%9C%81%E4%B8%89%E5%8F%B0%E5%8E%BF%E4%BA%BA%E6%B0%91%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E4%B8%89%E5%8F%B0%E5%8E%BF%E4%BA%BA%E6%B0%91%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%96%B0%E6%BA%90%E7%85%A4%E7%9F%BF%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E8%92%B2%E6%B1%9F%E5%8E%BF%E5%A6%87%E5%B9%BC%E4%BF%9D%E5%81%A5%E9%99%A2',
                  'http://www.a-hospital.com/w/%E6%96%B0%E6%B4%A5%E5%8E%BF%E4%B8%AD%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E5%A4%A7%E9%82%91%E5%8E%BF%E4%B8%AD%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E5%A4%A7%E9%82%91%E5%8E%BF%E9%AA%A8%E7%A7%91%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E7%9C%89%E5%B1%B1%E5%B8%82%E4%B8%9C%E5%9D%A1%E5%8C%BA%E7%B2%BE%E7%A5%9E%E7%97%85%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%96%B0%E6%BA%90%E7%85%A4%E7%9F%BF%E5%8C%BB%E9%99%A2%E5%A4%A7%E9%82%91%E5%8E%BF%E9%AA%A8%E7%A7%91%E5%8C%BB%E9%99%A2',
                  'http://www.a-hospital.com/w/%E7%9C%89%E5%B1%B1%E5%B8%82%E4%B8%9C%E5%9D%A1%E5%8C%BA%E5%A6%87%E5%B9%BC%E4%BF%9D%E5%81%A5%E9%99%A2'
                  
                  ]

    def parse(self, response):
        '''
            1.获取所有省份以及省份的url地址
        '''
        item = HospitalItem()
        hospital_province = response.xpath('//*[@id="bodyContent"]/table[1]/tbody/tr/td/a[3]/@title').extract()
        if hospital_province:
            item['hospital_province'] = hospital_province[0]
        hospital_addrs = response.xpath('//*[@id="bodyContent"]/ul[1]/li[1]/text()').extract()
        if hospital_addrs != None:
            item['hospital_addrs'] = hospital_addrs[0][1:]
        # 医院名称
        item['hospital_name'] = response.xpath('//*[@id="firstHeading"]/text()').extract_first()
        # 医院别名
        alias = response.xpath('//*[@id="bodyContent"]/p/b/text()').extract_first()
        if '（' in alias:
            alias = alias.split('（')[1]
            item['hospital_alias'] = alias[0:-1]
        else:
            item['hospital_alias'] = None
        # 所在城市
        hospital_city = response.xpath('//*[@id="bodyContent"]/table[1]/tbody/tr/td/a[4]/@title').extract()
        if hospital_city:
            item['hospital_city'] = hospital_city[0]
        # 所在辖区
        hospital_county = response.xpath('//*[@id="bodyContent"]/table[1]/tbody/tr/td/a[5]/@title').extract()
        if hospital_county:
            item['hospital_county'] = hospital_county[0]
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








    
    