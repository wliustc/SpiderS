# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GdCwssItem(scrapy.Item):
    uid = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    telephone = scrapy.Field()
    distance = scrapy.Field()
    detail_url = scrapy.Field()
    #service_rating = scrapy.Field()
    environment_rating = scrapy.Field()
    clinic_name = scrapy.Field()
    chong_uid = scrapy.Field()
    write_time = scrapy.Field()
    city_id = scrapy.Field()


    