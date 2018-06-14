# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    frm = scrapy.Field()
    title = scrapy.Field()
    src_uid = scrapy.Field()
    link = scrapy.Field()
    avg_price = scrapy.Field()
    sale_houses = scrapy.Field()
    rental_houses = scrapy.Field()


class FangDetailItem(scrapy.Item):
    csi_id = scrapy.Field()
    district = scrapy.Field()
    position = scrapy.Field()
    address = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    built_dt = scrapy.Field()
    developer = scrapy.Field()
    property_company = scrapy.Field()
    property_type = scrapy.Field()
    property_fee = scrapy.Field()
    covered_area = scrapy.Field()
    households = scrapy.Field()
    cur_households = scrapy.Field()
    plot_ratio = scrapy.Field()
    greening_rate = scrapy.Field()


class FangPriceItem(scrapy.Item):
    csi_id = scrapy.Field()
    avg_price = scrapy.Field()