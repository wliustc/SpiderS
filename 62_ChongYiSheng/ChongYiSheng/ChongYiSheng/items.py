# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChongyishengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    package_name = scrapy.Field()
    package_num = scrapy.Field()
    package_id = scrapy.Field()
    clinic_name = scrapy.Field()
    id = scrapy.Field()
    dianping_id = scrapy.Field()
    system_id = scrapy.Field()
    hospital = scrapy.Field()
    dealDetail = scrapy.Field()
    write_time = scrapy.Field()

class DianPingTuanDetailItem(scrapy.Item):
    Serial = scrapy.Field()
    phone = scrapy.Field()
    consume_time = scrapy.Field()
    package_name = scrapy.Field()
    price = scrapy.Field()
    business_privilege = scrapy.Field()
    settlement_price = scrapy.Field()
    shopname = scrapy.Field()
    checkout_account = scrapy.Field()
    shopId = scrapy.Field()
    write_time = scrapy.Field()
    account = scrapy.Field()
    deal_id = scrapy.Field()

class TuanGouQuanItem(scrapy.Item):
    dpSailedTipMsg = scrapy.Field()
    processId = scrapy.Field()
    endDate = scrapy.Field()
    mtDealGroupId = scrapy.Field()
    ownerName = scrapy.Field()
    mtSailedNum = scrapy.Field()
    ownerTel = scrapy.Field()
    channelStatus = scrapy.Field()
    title = scrapy.Field()
    mtUrl = scrapy.Field()
    brief = scrapy.Field()
    buttons = scrapy.Field()
    dpSailedTip = scrapy.Field()
    status = scrapy.Field()
    outBizId = scrapy.Field()
    mtSailedTip = scrapy.Field()
    price = scrapy.Field()
    dpSailedNum = scrapy.Field()
    merchantType = scrapy.Field()
    dpDealGroupId = scrapy.Field()
    mtSailedTipMsg = scrapy.Field()
    endTip = scrapy.Field()
    ownerId = scrapy.Field()
    dpUrl = scrapy.Field()
    customerId = scrapy.Field()
    dphospital_name = scrapy.Field()
    dphospital_id = scrapy.Field()
    mthospital_name = scrapy.Field()
    mthospital_id = scrapy.Field()
    write_time = scrapy.Field()
    dphospital_list = scrapy.Field()
    mthospital_list = scrapy.Field()
    account = scrapy.Field()
    
class BaiDuMapDetailItem(scrapy.Item):
    # task_time = scrapy.Field()
    hospital_name = scrapy.Field()
    hospital_id = scrapy.Field()
    hospital_system_id = scrapy.Field()
    hospital_baidu_id = scrapy.Field()
    comment_avg_score = scrapy.Field()
    comment_num = scrapy.Field()
    service_rating = scrapy.Field()
    video_url = scrapy.Field()
    quality_score = scrapy.Field()
    cn_name = scrapy.Field()
    taste_rating = scrapy.Field()
    integral_award = scrapy.Field()
    user_id = scrapy.Field()
    sentiment = scrapy.Field()
    favorNum = scrapy.Field()
    content = scrapy.Field()
    facility_rating = scrapy.Field()
    video_pic = scrapy.Field()
    isAgree = scrapy.Field()
    time_stamp = scrapy.Field()
    effect_rating = scrapy.Field()
    one_url_mobile = scrapy.Field()
    overall_rating = scrapy.Field()
    user_logo = scrapy.Field()
    cmt_id = scrapy.Field()
    user_url = scrapy.Field()
    price = scrapy.Field()
    agreeUserLogoUrl = scrapy.Field()
    one_url = scrapy.Field()
    nick_user_recommend = scrapy.Field()
    date = scrapy.Field()
    product_rating = scrapy.Field()
    class_one = scrapy.Field()
    src = scrapy.Field()
    poi_id = scrapy.Field()
    user_url_mobile = scrapy.Field()
    comment_url_mobile = scrapy.Field()
    pics = scrapy.Field()
    environment_rating = scrapy.Field()
    user_name = scrapy.Field()
    video_time = scrapy.Field()
    comment_url = scrapy.Field()
    write_time = scrapy.Field()

    
    
class BaiDuMapRadiusItem(scrapy.Item):
    uid = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    telephone = scrapy.Field()
    detail_info = scrapy.Field()
    distance = scrapy.Field()
    detail_url = scrapy.Field()
   # price = scrapy.Field()
    service_rating = scrapy.Field()
    environment_rating = scrapy.Field()
    clinic_name = scrapy.Field()
    chong_uid = scrapy.Field()
    city_id = scrapy.Field()
    write_time = scrapy.Field()
    
    
    
    
    
class CalDateCountItem(scrapy.Item):
    calDate = scrapy.Field()
    calCount = scrapy.Field()
    tasktime = scrapy.Field()
    deal_id = scrapy.Field()
    
    
    