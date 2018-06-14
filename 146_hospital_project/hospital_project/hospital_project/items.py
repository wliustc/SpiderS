# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 医院名称
    hospital_name = scrapy.Field()
    # 医院别名
    hospital_alias = scrapy.Field()
    # 所在省份
    hospital_province = scrapy.Field()
    # 所在城市
    hospital_city = scrapy.Field()
    # 所在辖区
    hospital_county = scrapy.Field()
    # 医院等级
    hospital_grade = scrapy.Field()
    # 地址
    hospital_addrs = scrapy.Field()
    # 电话
    hospital_phone = scrapy.Field()
    # 经营方式
    business_practice = scrapy.Field()
    data_source = scrapy.Field()