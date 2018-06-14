# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class F58AdvertItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    logr = scrapy.Field()
    sortid = scrapy.Field()
    infoid = scrapy.Field()
    uid = scrapy.Field()
    company_id = scrapy.Field()
    item_title = scrapy.Field()
    job_link = scrapy.Field()
    urlparams = scrapy.Field()
    company = scrapy.Field()
    company_link = scrapy.Field()
    location = scrapy.Field()
    up_time = scrapy.Field()
    wlt = scrapy.Field()
    city_name = scrapy.Field()
    district = scrapy.Field()
    shangquan = scrapy.Field()
    sub1_name = scrapy.Field()
    sub2_name = scrapy.Field()
    current_link = scrapy.Field()
    total_count = scrapy.Field()
    real_up_date = scrapy.Field()
    getdate = scrapy.Field()

    