# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JdRealTimeFlowSource(scrapy.Item):
    source=scrapy.Field()
    indChannel=scrapy.Field()
    visit_num=scrapy.Field()
    visit_rate=scrapy.Field()
    source_id=scrapy.Field()
    has_sub=scrapy.Field()
    fathersourceid=scrapy.Field()
    fathersourcename =scrapy.Field()
    dt=scrapy.Field()
    shop_name=scrapy.Field()
    date=scrapy.Field()
    
class JdRealTimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_name=scrapy.Field()
    CustPriceAvg = scrapy.Field()
    CustPriceAvg_ytd = scrapy.Field()
    CustPriceAvg_ytdRate = scrapy.Field()
    OrdProNum =scrapy.Field()
    OrdProNum_channelPercent = scrapy.Field()
    OrdProNum_ytdTime = scrapy.Field()
    OrdProNum_ytdTimeRate = scrapy.Field()
    OrdProNum_ytdPercent = scrapy.Field()
    OrdAmt = scrapy.Field()
    OrdAmt_channelPercent = scrapy.Field()
    OrdAmt_ytdTimeRate = scrapy.Field()
    OrdAmt_ytdTime = scrapy.Field()
    OrdAmt_ytdPercent = scrapy.Field()
    OrdCustNum = scrapy.Field()
    OrdCustNum_channelPercent = scrapy.Field()
    OrdCustNum_ytdTimeRate = scrapy.Field()
    OrdCustNum_ytdTime = scrapy.Field()
    OrdCustNum_ytdPercent = scrapy.Field()
    OrdNum = scrapy.Field()
    OrdNum_channelPercent = scrapy.Field()
    OrdNum_ytdTimeRate = scrapy.Field()
    OrdNum_ytdTime = scrapy.Field()
    OrdNum_ytdPercent = scrapy.Field()
    ToOrdRate = scrapy.Field()
    ToOrdRate_ytd = scrapy.Field()
    ToOrdRate_ytdRate = scrapy.Field()
    PV = scrapy.Field()
    PV_channelPercent = scrapy.Field()
    PV_ytdTimeRate = scrapy.Field()
    PV_ytdTime = scrapy.Field()
    PV_ytdPercent = scrapy.Field()
    ShopCollectNum = scrapy.Field()
    CartUserNum = scrapy.Field()
    UV = scrapy.Field()
    UV_channelPercent = scrapy.Field()
    UV_ytdTimeRate = scrapy.Field()
    UV_ytdTime = scrapy.Field()
    UV_ytdPercent = scrapy.Field()
    realTime = scrapy.Field()
    compareTime = scrapy.Field()
    dt = scrapy.Field()
    
class JdRealTimeTopItem(scrapy.Item):
    shop_name=scrapy.Field()
    date=scrapy.Field()
    title=scrapy.Field()
    xiadan_jine=scrapy.Field()
    xiadan_danliang=scrapy.Field()
    xiandan_kehu=scrapy.Field()
    xiadan_count=scrapy.Field()
    pv=scrapy.Field()
    uv=scrapy.Field()
    change=scrapy.Field()
    top=scrapy.Field()
    spuid=scrapy.Field()
    dt=scrapy.Field()
    imgurl=scrapy.Field()
    
class JdRealTimeHourItem(scrapy.Item):
    shop_name=scrapy.Field()
    OrdProNum=scrapy.Field()
    PV=scrapy.Field()
    OrdAmt=scrapy.Field()
    OrdCustNum=scrapy.Field()
    OrdNum=scrapy.Field()
    UV=scrapy.Field()
    date=scrapy.Field()
    hour=scrapy.Field()
    dt=scrapy.Field()

    
    
    
    
    