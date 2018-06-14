# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    the_star = scrapy.Field()
    reviewCount = scrapy.Field()
    consumption = scrapy.Field()
    product = scrapy.Field()
    environment = scrapy.Field()
    service = scrapy.Field()
    addr = scrapy.Field()
    tel = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
    district = scrapy.Field()
    business = scrapy.Field()
    url = scrapy.Field()
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    city_name = scrapy.Field()
    real_province = scrapy.Field()
    category1_id = scrapy.Field()
    category2_id = scrapy.Field()
    category3_id = scrapy.Field()
    district_id = scrapy.Field()
    biz_id = scrapy.Field()
    city_id = scrapy.Field()
    display_score1_name = scrapy.Field()
    display_score1 = scrapy.Field()
    display_score2_name = scrapy.Field()
    display_score2 = scrapy.Field()
    display_score3_name = scrapy.Field()
    display_score3 = scrapy.Field()

class CommentItem(scrapy.Item):
    comment_text = scrapy.Field()
    user_name = scrapy.Field()
    score1_name = scrapy.Field()
    score1 = scrapy.Field()
    score2_name = scrapy.Field()
    score2 = scrapy.Field()
    score3_name = scrapy.Field()
    score3 = scrapy.Field()
    user_contrib_val = scrapy.Field()
    total_score = scrapy.Field()
    shop_id = scrapy.Field()
    comment_dt = scrapy.Field()
    user_id = scrapy.Field()
    comment_id = scrapy.Field()
    dt = scrapy.Field()
    brand = scrapy.Field()
    
    
class DianpingShopItem(scrapy.Item):
    id=scrapy.Field()
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
    shop_lat = scrapy.Field()
    shop_lng = scrapy.Field()
    dt=scrapy.Field()

class DianpingDealItem(scrapy.Item):
    dt = scrapy.Field()
    shop_id = scrapy.Field()
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
    tag = scrapy.Field()


    
    
    
    
    
    