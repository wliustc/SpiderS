# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdShangzhiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JdShangzhiliuliangItem(scrapy.Item):
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    category3 = scrapy.Field()
    peer_UV = scrapy.Field()
    shop_UV = scrapy.Field()
    shop_UV_rate = scrapy.Field()
    uv_zhanbi = scrapy.Field()
    uv_zhanbi_rate = scrapy.Field()
    shop_CustRate = scrapy.Field()
    shop_CustRate_rate = scrapy.Field()
    scan = scrapy.Field()
    scan_rate = scrapy.Field()
    shom_name = scrapy.Field()
    shop_name = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()
    id = scrapy.Field()
    source = scrapy.Field()
    fufei = scrapy.Field()
    sourceid = scrapy.Field()
    fathersourceid = scrapy.Field()
    fathername = scrapy.Field()


class JdShangTransctItem(scrapy.Item):
    OrdProNum = scrapy.Field()
    # 下单百分比
    rates = scrapy.Field()
    OrdProNum_rate = scrapy.Field()
    CustPriceAvg = scrapy.Field()
    # 百分比
    CustPriceAvg_rates = scrapy.Field()
    CustPriceAvg_rate = scrapy.Field()
    # 人均浏览量
    AvgDepth = scrapy.Field()
    # 百分比
    AvgDepth_rates = scrapy.Field()
    AvgDepth_rate = scrapy.Field()
    # 平均停留时长
    AvgStayTime = scrapy.Field()
    # 百分比
    AvgStayTime_rates = scrapy.Field()
    AvgStayTime_rate = scrapy.Field()
    # 下单转化率
    ToOrdRate = scrapy.Field()
    # 百分比
    ToOrdRate_rates = scrapy.Field()
    ToOrdRate_rate = scrapy.Field()
    # 下单金额
    OrdAmt = scrapy.Field()
    # 百分比
    OrdAmt_rates = scrapy.Field()
    OrdAmt_rate = scrapy.Field()
    # 跳失率
    SkipOut = scrapy.Field()
    # 百分比
    SkipOut_rates = scrapy.Field()
    SkipOut_rate = scrapy.Field()
    # 浏览量
    PV = scrapy.Field()
    # 百分比
    PV_rates = scrapy.Field()
    PV_rate = scrapy.Field()
    # 下单客户数
    OrdCustNum = scrapy.Field()
    # 百分比
    OrdCustNum_rates = scrapy.Field()
    OrdCustNum_rate = scrapy.Field()
    # 下单单量
    OrdNum = scrapy.Field()
    # 百分比
    OrdNum_rates = scrapy.Field()
    OrdNum_rate = scrapy.Field()
    # 访客数
    UV = scrapy.Field()
    # 百分比
    UV_rates = scrapy.Field()
    UV_rate = scrapy.Field()
    shop_name = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()
    id = scrapy.Field()


class JdShangTrafficItem(scrapy.Item):
    id = scrapy.Field()
    shop_name = scrapy.Field()
    jump_rate = scrapy.Field()
    visitors = scrapy.Field()
    stay = scrapy.Field()
    source = scrapy.Field()
    jump_rate_contrast = scrapy.Field()
    visitors_abnormal = scrapy.Field()
    views = scrapy.Field()
    Per_capita_views_abnormal = scrapy.Field()
    views_rate = scrapy.Field()
    views_abnormal = scrapy.Field()
    stay_abnormal = scrapy.Field()
    visitors_rate = scrapy.Field()
    stay_rate = scrapy.Field()
    jump_rate_abnormal = scrapy.Field()
    Per_capita_views_rate = scrapy.Field()
    Per_capita_views = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangGoodsItem(scrapy.Item):
    id = scrapy.Field()
    shop_name = scrapy.Field()
    goodsAddBuyRate_value = scrapy.Field()
    addBuyCustNum_value = scrapy.Field()
    addBuyGoodsPieceNum_rate = scrapy.Field()
    ordGoodsPieceNum_value = scrapy.Field()
    goodsConverRate_value = scrapy.Field()
    addBuyGoodsPieceNum_value = scrapy.Field()
    goodsConcernNum_rate = scrapy.Field()
    addBuyCustNum_rate = scrapy.Field()
    saleGoodsNum_value = scrapy.Field()
    ordAmt_value = scrapy.Field()
    visitedGoodsNum_rate = scrapy.Field()
    goodsBrowseNum_value = scrapy.Field()
    visitedGoodsNum_value = scrapy.Field()
    goodsBrowseNum_rate = scrapy.Field()
    goodsConcernNum_value = scrapy.Field()
    addBuyGoodsNum_value = scrapy.Field()
    addBuyGoodsNum_rate = scrapy.Field()
    goodsSaleRate_rate = scrapy.Field()
    goodsVisitorNum_value = scrapy.Field()
    goodsVisitorNum_rate = scrapy.Field()
    goodsAddBuyRate_rate = scrapy.Field()
    ordAmt_rate = scrapy.Field()
    goodsSaleRate_value = scrapy.Field()
    goodsConverRate_rate = scrapy.Field()
    saleGoodsNum_rate = scrapy.Field()
    ordGoodsPieceNum_rate = scrapy.Field()
    goodsExposureRate_value = scrapy.Field()
    goodsExposureRate_rate = scrapy.Field()
    ProSkipOut_value= scrapy.Field()
    ProSkipOut_rate= scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangDealtraitItem(scrapy.Item):
    id = scrapy.Field()
    shop_name = scrapy.Field()
    peer_occupies = scrapy.Field()
    Orders_amount = scrapy.Field()
    channel = scrapy.Field()
    Orders_occupies = scrapy.Field()
    Orders_money = scrapy.Field()
    Orders_client = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangAftersalesItem(scrapy.Item):
    id = scrapy.Field()
    replyRatio_value = scrapy.Field()
    numGs_value = scrapy.Field()
    numFx_rate = scrapy.Field()
    amtFx_value = scrapy.Field()
    numTs_rate = scrapy.Field()
    numTh_value = scrapy.Field()
    amtFx_rate = scrapy.Field()
    shop_name = scrapy.Field()
    ordDisRatio_value = scrapy.Field()
    numGs_rate = scrapy.Field()
    numHh_rate = scrapy.Field()
    amtHh_value = scrapy.Field()
    numGd_rate = scrapy.Field()
    amtHh_rate = scrapy.Field()
    amtTh_rate = scrapy.Field()
    amtTh_value = scrapy.Field()
    numTh_rate = scrapy.Field()
    numHh_value = scrapy.Field()
    ordDisRatioInd_rate = scrapy.Field()
    replyRatio_rate = scrapy.Field()
    ordDisRatioInd_value = scrapy.Field()
    numGd_value = scrapy.Field()
    numTs_value = scrapy.Field()
    ordDisRatio_rate = scrapy.Field()
    numFx_value = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangCoreItem(scrapy.Item):
    id = scrapy.Field()
    Orders_sum = scrapy.Field()
    Orders_rate = scrapy.Field()
    OrdersRate = scrapy.Field()
    PV = scrapy.Field()
    PV_rate = scrapy.Field()
    PVRate = scrapy.Field()
    UV = scrapy.Field()
    UV_rate = scrapy.Field()
    UVRate = scrapy.Field()
    CustPriceAvg = scrapy.Field()
    CustPriceAvg_Price = scrapy.Field()
    CustPriceAvg_rate = scrapy.Field()
    CustRate = scrapy.Field()
    Cust_wireless_rate = scrapy.Field()
    Cust_rate = scrapy.Field()
    The90 = scrapy.Field()
    The90Rate = scrapy.Field()
    The90_rate = scrapy.Field()
    The30 = scrapy.Field()
    The30Rate = scrapy.Field()
    The30_rate = scrapy.Field()
    ShopCollectNum = scrapy.Field()
    App_population = scrapy.Field()
    ShopCollectNum_rate = scrapy.Field()
    shop_name = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangOrderdetailItem(scrapy.Item):
    id = scrapy.Field()
    OrderID = scrapy.Field()
    cover_charge = scrapy.Field()
    Order_time = scrapy.Field()
    title = scrapy.Field()
    coupon = scrapy.Field()
    raw_money = scrapy.Field()
    order_amount = scrapy.Field()
    source = scrapy.Field()
    freight = scrapy.Field()
    commodity_count = scrapy.Field()
    paytime = scrapy.Field()
    shop_name = scrapy.Field()
    Payment = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangOrderclientItem(scrapy.Item):
    id = scrapy.Field()
    Orders_rate = scrapy.Field()
    Guest_piece = scrapy.Field()
    payPct = scrapy.Field()
    Guest_piece_rate = scrapy.Field()
    upt_rate = scrapy.Field()
    shop_name = scrapy.Field()
    Orders_client_rate = scrapy.Field()
    client_type = scrapy.Field()
    Orders_rate_contrast = scrapy.Field()
    payPct_rate = scrapy.Field()
    upt = scrapy.Field()
    Orders_client = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()


class JdShangGoodsdskuItem(scrapy.Item):
    id = scrapy.Field()
    shop_name = scrapy.Field()
    id_ = scrapy.Field()
    orderItemQty = scrapy.Field()
    views = scrapy.Field()
    Focus_on = scrapy.Field()
    addCartItemCnt = scrapy.Field()
    title = scrapy.Field()
    launch_time = scrapy.Field()
    comments = scrapy.Field()
    orderRate = scrapy.Field()
    visitors = scrapy.Field()
    orderAmt = scrapy.Field()
    orderBuyerCnt = scrapy.Field()
    url = scrapy.Field()
    UAworth = scrapy.Field()
    Purchase_one = scrapy.Field()
    Orders_quantity = scrapy.Field()
    date = scrapy.Field()
    dt = scrapy.Field()
    type = scrapy.Field()
    huohao=scrapy.Field()
    
class JdShangzhiliuliangdownItem(scrapy.Item):
    id = scrapy.Field()
    shop_name = scrapy.Field()
    source = scrapy.Field()     #数据类型
    shop_UV = scrapy.Field()    #访客数
    peer_UV = scrapy.Field()    #访客数_同行同级
    PV = scrapy.Field()         #浏览量
    peer_PV = scrapy.Field()    #浏览量_同行同级
    jumplose = scrapy.Field()   #跳失率
    peer_jumplose = scrapy.Field() #跳失率_同行同级
    per_PV = scrapy.Field() #人均浏览量
    peer_per_PV = scrapy.Field()    #人均浏览量_同行同级
    avg_time = scrapy.Field()       #平均停留时长
    peer_avg_time = scrapy.Field()  #平均停留时长_同行同级
    new_UV=scrapy.Field()       #新访客数
    peer_new_UV=scrapy.Field()  #新访客数_同行同级
    old_UV = scrapy.Field()     #老访客数
    peer_old_UV = scrapy.Field()   #老访客数_同行同级
    date=scrapy.Field()
    dt=scrapy.Field()
    
    
    
    
    