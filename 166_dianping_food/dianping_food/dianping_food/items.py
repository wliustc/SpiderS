# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingFoodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    categoryName = scrapy.Field()
    dishtags = scrapy.Field()
    shop_name = scrapy.Field()
    branchName = scrapy.Field()
    priceText = scrapy.Field()
    reviewCount = scrapy.Field()
    shopPower = scrapy.Field()
    shop_id = scrapy.Field()
    tagList = scrapy.Field()
    addDate = scrapy.Field()
    address = scrapy.Field()
    origin_data = scrapy.Field()
    point_name1 = scrapy.Field()
    point_name2 = scrapy.Field()
    point_name3 = scrapy.Field()
    point1 = scrapy.Field()
    point2 = scrapy.Field()
    point3 = scrapy.Field()


class DianpingShoptimeItem(scrapy.Item):
    shop_id = scrapy.Field()
    reviewTag = scrapy.Field()
    addDate = scrapy.Field()
    address = scrapy.Field()
    origin_data = scrapy.Field()
    city_level = scrapy.Field()