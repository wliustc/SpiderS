# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DailyTaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()
    shop_url = scrapy.Field()
    fg_category_id = scrapy.Field()
    category_id = scrapy.Field()
    user_id = scrapy.Field()
    shop_name = scrapy.Field()
    dt = scrapy.Field()


class ShopGoodsItem(scrapy.Item):
    data = scrapy.Field()
    dt = scrapy.Field()


class GoodsKeywordsItem(scrapy.Item):
    shop_name = scrapy.Field()
    brand = scrapy.Field()
    nid = scrapy.Field()
    dt = scrapy.Field()
    keyword = scrapy.Field()
    count_num = scrapy.Field()
    sentiment = scrapy.Field()


class GoodsTmpItem(scrapy.Item):
    nid = scrapy.Field()
    shop_name = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    sellcount = scrapy.Field()
    price = scrapy.Field()
    commentcount = scrapy.Field()
    categoryId = scrapy.Field()
    rootCategoryId = scrapy.Field()
    quantity = scrapy.Field()
    model_num = scrapy.Field()
    sexual = scrapy.Field()
    tag_price = scrapy.Field()
    time_to_market = scrapy.Field()
    price_range = scrapy.Field()
    sku_count = scrapy.Field()
    reserve_price = scrapy.Field()
    favcount = scrapy.Field()
    image_str = scrapy.Field()
    dt = scrapy.Field()
    
    
    
    