# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VipSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    the_date = scrapy.Field()
    brand = scrapy.Field()
    sales = scrapy.Field()
    cutGoodsMoney = scrapy.Field()
    rejectedPct = scrapy.Field()
    flowUv = scrapy.Field()
    flowConversion = scrapy.Field()
    orderCnt = scrapy.Field()
    consumerCount = scrapy.Field()
    avgUserSalesAmount = scrapy.Field()
    avgOrderSalesAmount = scrapy.Field()
    stockAmtOnline = scrapy.Field()
    stockCntOnline = scrapy.Field()
    saleStockAmt = scrapy.Field()
    goodsCnt = scrapy.Field()
    couponAmt = scrapy.Field()

class SecondTableItem(scrapy.Item):
    the_date = scrapy.Field()
    uv = scrapy.Field()
    proportion = scrapy.Field()
    group_ = scrapy.Field()
    brand = scrapy.Field()


class ThirdTableItem(scrapy.Item):
    the_date = scrapy.Field()
    brand = scrapy.Field()
    avgOrderSalesAmount = scrapy.Field()
    avgOrderCost = scrapy.Field()
    avgOrdersAmount = scrapy.Field()


class FourthTableItem(scrapy.Item):
    the_date = scrapy.Field()
    brand = scrapy.Field()
    activeTypeName = scrapy.Field()
    goodsCntPct = scrapy.Field()
    avgGoodsSalesAmount = scrapy.Field()
    orderCntPct = scrapy.Field()
    avgOrderGoodsAmount = scrapy.Field()


class FifthTableItem(scrapy.Item):
    brand = scrapy.Field()
    type_name = scrapy.Field()
    crawl_time = scrapy.Field()
    goodsPicUrl = scrapy.Field()
    goodsName = scrapy.Field()
    goodsCode = scrapy.Field()
    vipshopPrice = scrapy.Field()
    goodsStockCnt = scrapy.Field()
    goodsStockAmt = scrapy.Field()
    dayUv = scrapy.Field()
    dayUserCnt = scrapy.Field()
    dayGoodsCnt = scrapy.Field()
    daySalesAmount = scrapy.Field()
    dayAddcartCnt = scrapy.Field()
    conversion = scrapy.Field()
    sellingRatio = scrapy.Field()
    dayUvCtr = scrapy.Field()


class SixthTableItem(scrapy.Item):
    the_date = scrapy.Field()
    brand = scrapy.Field()
    sales = scrapy.Field()
    salesCnt = scrapy.Field()
    salesReturnCnt = scrapy.Field()
    salesReturnAmt = scrapy.Field()
    salesReturnPercent = scrapy.Field()
    rejectCnt = scrapy.Field()
    rejectAmt = scrapy.Field()
    rejectPercent = scrapy.Field()
    returnPercent = scrapy.Field()
    
class RealTimeItem(scrapy.Item):
    brand = scrapy.Field()
    the_time = scrapy.Field()
    sales = scrapy.Field()
    uv = scrapy.Field()
    consumerCount = scrapy.Field()
    conversion = scrapy.Field()
    unitPrice = scrapy.Field()
    salesAmount = scrapy.Field()
    orderCnt = scrapy.Field()

class RealTimeDangqiItem(scrapy.Item):
    brand = scrapy.Field()
    the_type = scrapy.Field()
    the_name = scrapy.Field()
    weight = scrapy.Field()
    dt = scrapy.Field()
    
    