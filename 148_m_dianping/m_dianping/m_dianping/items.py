# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DianpingShopItem(scrapy.Item):
    id=scrapy.Field()
    searchword=scrapy.Field()
    city_name=scrapy.Field()
    city_id=scrapy.Field()
    branchName=scrapy.Field()
    categoryId=scrapy.Field()
    categoryName=scrapy.Field()
    cityId=scrapy.Field()
    shop_id=scrapy.Field()
    matchText=scrapy.Field()
    name=scrapy.Field()
    priceText=scrapy.Field()
    regionName=scrapy.Field()
    reviewCount=scrapy.Field()
    scoreText=scrapy.Field()
    shopPower=scrapy.Field()
    shopType=scrapy.Field()
    shop_address=scrapy.Field()
    phone=scrapy.Field()
    dt=scrapy.Field()

class DianpingDealItem(scrapy.Item):
    id = scrapy.Field()
    title=scrapy.Field()
    shop_id=scrapy.Field()
    price=scrapy.Field()
    oldprice=scrapy.Field()
    soldNum=scrapy.Field()
    deal_id=scrapy.Field()
    desc=scrapy.Field()
    type=scrapy.Field()
    detail=scrapy.Field()
    buy_know=scrapy.Field()
    start_time=scrapy.Field()
    end_time=scrapy.Field()
    dt = scrapy.Field()
    