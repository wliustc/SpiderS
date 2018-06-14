# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MeituanPetAppyankeItem(scrapy.Item):
    dpsi_id=scrapy.Field()
    shop_id=scrapy.Field()
    shop_name=scrapy.Field()
    category1_id=scrapy.Field()
    category2_id=scrapy.Field()
    last_update_dt=scrapy.Field()
    city_id=scrapy.Field()
    city_name=scrapy.Field()
    address=scrapy.Field()
    lng=scrapy.Field()
    lat=scrapy.Field()
    avg_price=scrapy.Field()
    shop_power=scrapy.Field()
    phone_no=scrapy.Field()
    dt=scrapy.Field()
    avgscore=scrapy.Field()
    comments_num=scrapy.Field()
    historyCouponCount=scrapy.Field()
    brand=scrapy.Field()
    backCateName=scrapy.Field()

class MeituanPetHospitalshopItem(scrapy.Item):
    # define the fields for your item here like:
    mtshop_name = scrapy.Field()
    shop_url = scrapy.Field()
    mtshop_id = scrapy.Field()
    score = scrapy.Field()
    pinglun_num = scrapy.Field()
    shop_sale_num = scrapy.Field()
    dist = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    city_name = scrapy.Field()
    type = scrapy.Field()
    distract = scrapy.Field()
    dt = scrapy.Field()
    host = scrapy.Field()
    pass

class MeituanPetHospitalItem(scrapy.Item):
    # define the fields for your item here like:
    mtshop_id = scrapy.Field()
    mtdeal_id = scrapy.Field()
    deal_detail = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    sold = scrapy.Field()
    score=scrapy.Field()
    pingjia_num=scrapy.Field()
    start_time=scrapy.Field()
    end_time=scrapy.Field()
    dt = scrapy.Field()
    title = scrapy.Field()
    describe = scrapy.Field()


class Meituan_to_Dp_Item(scrapy.Item):
    mtdealid = scrapy.Field()
    brandName = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    originalPrice = scrapy.Field()
    title = scrapy.Field()
    coupontitle = scrapy.Field()
    price = scrapy.Field()
    orderTitle = scrapy.Field()
    dpDealGroupId = scrapy.Field()
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    phone =scrapy.Field()
    addr = scrapy.Field()
    avgscore = scrapy.Field()
    dpShopId = scrapy.Field()
    dt = scrapy.Field()
    solds = scrapy.Field()
    
class MeituanPetAppdealIdItem(scrapy.Item):
    # define the fields for your item here like:
    deal_id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    text = scrapy.Field()
    sale = scrapy.Field()
    dt=scrapy.Field()
    shop_id=scrapy.Field()

class MeituanPetAppYankecommentItem(scrapy.Item):
    backCateName = scrapy.Field()
    dsc_id = scrapy.Field()
    shop_id = scrapy.Field()
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    total_score = scrapy.Field()
    comment_text = scrapy.Field()
    comment_dt = scrapy.Field()
    dt = scrapy.Field()
    hash = scrapy.Field()

class MeituanPetAppcommentItem(scrapy.Item):
    backCateName = scrapy.Field()
    dsc_id = scrapy.Field()
    shop_id = scrapy.Field()
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    total_score = scrapy.Field()
    comment_text = scrapy.Field()
    comment_dt = scrapy.Field()
    dt = scrapy.Field()
    hash = scrapy.Field()
    
class MeituanPetAppweizhiItem(scrapy.Item):
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    dt = scrapy.Field()
    
    
    
    