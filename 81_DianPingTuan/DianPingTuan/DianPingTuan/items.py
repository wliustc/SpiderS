# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DianPIngAllStoreJson(scrapy.Item):
    response_content = scrapy.Field()
    meta = scrapy.Field()
    
class DianpingtuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PetServicesItem(scrapy.Item):
    dt = scrapy.Field()
    deal_id = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    sales = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    description = scrapy.Field()
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    shop_id = scrapy.Field()
    
class PetCommentsItem(scrapy.Item):
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    total_score = scrapy.Field()
    score1_name = scrapy.Field()
    score1 = scrapy.Field()
    score2_name = scrapy.Field()
    score2 = scrapy.Field()
    score3_name = scrapy.Field()
    score3 = scrapy.Field()
    comment_text = scrapy.Field()
    comment_dt = scrapy.Field()
    user_contrib_val = scrapy.Field()
    shop_id = scrapy.Field()
    comment_type = scrapy.Field()
    comment_id = scrapy.Field()
    

class MeiShiItem(scrapy.Item):
    shop_name = scrapy.Field()
    shop_num = scrapy.Field()
    average_spend = scrapy.Field()
    recommendation = scrapy.Field()
    comment_item = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    shopId = scrapy.Field()
    branch = scrapy.Field()
    comment_score =scrapy.Field()
    city_name = scrapy.Field()
    category = scrapy.Field()
    
    
    