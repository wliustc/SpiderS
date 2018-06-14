# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TrafficDataItem(scrapy.Item):
    # define the fields for your item here like:
    hospital_name = scrapy.Field()
    shop_id = scrapy.Field()
    plat = scrapy.Field()
    dt = scrapy.Field()
    uv = scrapy.Field()
    pv = scrapy.Field()
    loss_rate = scrapy.Field()
    loss_num = scrapy.Field()
    avg_view_time = scrapy.Field()
    total_view_time = scrapy.Field()
    created_time = scrapy.Field()
    _target_table = scrapy.Field()


class TrafficSourceItem(scrapy.Item):
    hospital_name = scrapy.Field()
    shop_id = scrapy.Field()
    plat = scrapy.Field()
    dt = scrapy.Field()
    source_name = scrapy.Field()
    search_count = scrapy.Field()
    source_ratio = scrapy.Field()
    industry_avg_ratio = scrapy.Field()
    circle_ratio = scrapy.Field()
    created_time = scrapy.Field()
    _target_table = scrapy.Field()

class MerchantPageClickItem(scrapy.Item):
    hospital_name = scrapy.Field()
    shop_id = scrapy.Field()
    plat = scrapy.Field()
    dt = scrapy.Field()
    click_module = scrapy.Field()
    click_count = scrapy.Field()
    click_ratio = scrapy.Field()
    industry_avg_ratio = scrapy.Field()
    circle_ratio = scrapy.Field()
    created_time = scrapy.Field()
    _target_table = scrapy.Field()


    
    
    