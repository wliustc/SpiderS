# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallShopListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nid = scrapy.Field()
    user_id = scrapy.Field()
    shop_name = scrapy.Field()
    dt = scrapy.Field()


class TmallShopGoodsItem(scrapy.Item):
    url = scrapy.Field()
    dt = scrapy.Field()
    title = scrapy.Field()
    nid = scrapy.Field()
    shop_name = scrapy.Field()
    price = scrapy.Field()
    month_sale = scrapy.Field()
    kuanhao = scrapy.Field()
    huohao = scrapy.Field()
    time_to_market = scrapy.Field()
    tag_price = scrapy.Field()
    