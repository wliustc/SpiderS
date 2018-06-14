# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherReportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WeatherReportNmcCityItem(scrapy.Item):
    city_code = scrapy.Field()
    city_name = scrapy.Field()
    city_url = scrapy.Field()
    province_code = scrapy.Field()
    province_name = scrapy.Field()
    province_url = scrapy.Field()
    sign = scrapy.Field()

class WeatherReportNmcDetailItem(scrapy.Item):
    content = scrapy.Field()
    meta = scrapy.Field()
    
    