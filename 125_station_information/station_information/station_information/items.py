# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StationInformationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    meta = scrapy.Field()

class TrainInfomationItem(scrapy.Item):
    arrive_time = scrapy.Field()
    end_station_name = scrapy.Field()
    isEnabled = scrapy.Field()
    service_type = scrapy.Field()
    start_station_name = scrapy.Field()
    start_time = scrapy.Field()
    station_name = scrapy.Field()
    station_no = scrapy.Field()
    station_train_code = scrapy.Field()
    stopover_time = scrapy.Field()
    train_class_name = scrapy.Field()
    search_start = scrapy.Field()
    search_end = scrapy.Field()
    train_number = scrapy.Field()
    train_start = scrapy.Field()
    train_end = scrapy.Field()
