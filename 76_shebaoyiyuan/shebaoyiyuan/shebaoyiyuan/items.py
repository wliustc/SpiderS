# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShebaoyuyuanItem(scrapy.Item):
    code = scrapy.Field()
    hospital = scrapy.Field()
    county = scrapy.Field()
    kind = scrapy.Field()
    sort = scrapy.Field()
    type = scrapy.Field()
    address = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()

class HeathFoodbjItem(scrapy.Item):
    licensekey = scrapy.Field()
    company = scrapy.Field()
    date_issue = scrapy.Field()
    term = scrapy.Field()
