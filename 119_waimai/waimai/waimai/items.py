# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WaimaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WaimaibaiduItem(scrapy.Item):
    frm=scrapy.Field()
    goods_id=scrapy.Field()
    goods_name=scrapy.Field()
    price=scrapy.Field()
    category=scrapy.Field()
    shop_id=scrapy.Field()
    month_sales=scrapy.Field()
    dt=scrapy.Field()

class WaimaibaiduShoplistItem(scrapy.Item):
    frm = scrapy.Field()
    city = scrapy.Field()
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    category1 = scrapy.Field()
    brand_name = scrapy.Field()
    min_send_price = scrapy.Field()
    avg_delivery_time = scrapy.Field()
    score = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    sale_num = scrapy.Field()
    month_sale_num = scrapy.Field()
    dt=scrapy.Field()

class WaimaieleShoplistItem(scrapy.Item):
    frm = scrapy.Field()
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    city = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    score = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    month_sale_num = scrapy.Field()
    context = scrapy.Field()
    dt= scrapy.Field()

class WaimaieleItem(scrapy.Item):
    frm = scrapy.Field()
    goods_id = scrapy.Field()
    goods_name = scrapy.Field()
    category = scrapy.Field()
    shop_id = scrapy.Field()
    orig_price = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    month_sales = scrapy.Field()
    dt = scrapy.Field()


class WaimaimeituanShoplistItem(scrapy.Item):
    shop_name=scrapy.Field()
    frm=scrapy.Field()
    city=scrapy.Field()
    address=scrapy.Field()
    phone=scrapy.Field()
    shop_id=scrapy.Field()
    score=scrapy.Field()
    in_time_delivery_percent=scrapy.Field()
    in_time_delivery_percent_ranking=scrapy.Field()
    avg_delivery_time=scrapy.Field()
    avg_delivery_time_ranking=scrapy.Field()
    lng=scrapy.Field()
    lat=scrapy.Field()
    category1=scrapy.Field()
    min_send_price=scrapy.Field()
    month_sale_num=scrapy.Field()
    dt=scrapy.Field()
    uni_hash_code = scrapy.Field()

class WaimaimeituanItem(scrapy.Item):
    dt = scrapy.Field()
    frm = scrapy.Field()
    goods_id = scrapy.Field()
    goods_name = scrapy.Field()
    category = scrapy.Field()
    shop_id = scrapy.Field()
    orig_price = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    month_sales = scrapy.Field()
    uni_hash_code=scrapy.Field()
