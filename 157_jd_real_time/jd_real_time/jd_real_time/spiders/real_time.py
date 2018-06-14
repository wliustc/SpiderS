# -*- coding: utf-8 -*-
import scrapy
import web
import json
import time
from jd_real_time.items import JdRealTimeItem
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}

class RealTimeSpider(scrapy.Spider):
    name = "real_time"
    allowed_domains = ["sz.jd.com"]
    start_urls = ['http://sz.jd.com/']


    def start_requests(self):
        self.brand_list = []
        sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
        (shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
        group by shop_name;'''
        for i in db.query(sql):
            cookies = str(i.get('cookies'))
            name = i.get('shop_name')
            cookies_tuple = name, cookies
            self.brand_list.append(cookies_tuple)

        for i in self.brand_list:
            cookies = json.loads(i[1])
            shop_name = i[0]
            dt=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            After_sale_url='https://sz.jd.com/realTime/getRealTimeSummary.ajax?indChannel=99'
            yield scrapy.Request(After_sale_url, headers=headers, cookies=cookies,
                                 meta={'date': dt, 'cate': u'售后分析', 'Account': shop_name}, dont_filter=True)

    def parse(self, response):
        try:
            data=json.loads(response.body.decode())
        except Exception as e:
            self.logger.error(response.body.decode())
        item=JdRealTimeItem()
        item['shop_name']= response.meta['Account']
        item['CustPriceAvg']=data['content']['summary']['Order']['CustPriceAvg']['value'] #客单件
        item['CustPriceAvg_ytd'] = data['content']['summary']['Order']['CustPriceAvg']['ytd']  # 昨日同时客单件
        item['CustPriceAvg_ytdRate'] = data['content']['summary']['Order']['CustPriceAvg']['ytdRate']  # 昨日同时客单件环比
        item['OrdProNum'] = data['content']['summary']['Order']['OrdProNum']['value']  # 工单商品件数
        item['OrdProNum_channelPercent'] = data['content']['summary']['Order']['OrdProNum']['channelPercent']  # 工单商品件数占全部渠道
        item['OrdProNum_ytdTime'] = data['content']['summary']['Order']['OrdProNum']['ytdTime']  # 昨日同时工单商品件数
        item['OrdProNum_ytdTimeRate'] = data['content']['summary']['Order']['OrdProNum']['ytdTimeRate']  # 工单商品件数环比
        item['OrdProNum_ytdPercent'] = data['content']['summary']['Order']['OrdProNum']['ytdPercent']  # 工单商品件数占昨天全天
        item['OrdAmt'] = data['content']['summary']['Order']['OrdAmt']['value']  # 下单金额
        item['OrdAmt_channelPercent'] = data['content']['summary']['Order']['OrdAmt']['channelPercent']  # 下单金额占全部渠道
        item['OrdAmt_ytdTimeRate'] = data['content']['summary']['Order']['OrdAmt']['ytdTimeRate']  # 下单金额环比
        item['OrdAmt_ytdTime'] = data['content']['summary']['Order']['OrdAmt']['ytdTime']  # 昨日同时的下单金额
        item['OrdAmt_ytdPercent'] = data['content']['summary']['Order']['OrdAmt']['ytdPercent']  # 下单金额占昨天全天
        item['OrdCustNum'] = data['content']['summary']['Order']['OrdCustNum']['value']  # 客单量
        item['OrdCustNum_channelPercent'] = data['content']['summary']['Order']['OrdCustNum']['channelPercent']  # 客单量占全部渠道
        item['OrdCustNum_ytdTimeRate'] = data['content']['summary']['Order']['OrdCustNum']['ytdTimeRate']  # 客单量环比
        item['OrdCustNum_ytdTime'] = data['content']['summary']['Order']['OrdCustNum']['ytdTime']  # 昨日同时的客单量
        item['OrdCustNum_ytdPercent'] = data['content']['summary']['Order']['OrdCustNum']['ytdPercent']  # 客单量占昨天全天
        item['OrdNum'] = data['content']['summary']['Order']['OrdNum']['value']  # 下单客户数
        item['OrdNum_channelPercent'] = data['content']['summary']['Order']['OrdNum']['channelPercent']  # 下单客户数占全部渠道
        item['OrdNum_ytdTimeRate'] = data['content']['summary']['Order']['OrdNum']['ytdTimeRate']  # 下单客户数环比
        item['OrdNum_ytdTime'] = data['content']['summary']['Order']['OrdNum']['ytdTime']  # 昨日同时的下单客户数
        item['OrdNum_ytdPercent'] = data['content']['summary']['Order']['OrdNum']['ytdPercent']  # 下单客户数占昨天全天
        item['ToOrdRate'] = data['content']['summary']['Visited']['ToOrdRate']['value']  # 转换率
        item['ToOrdRate_ytd'] = data['content']['summary']['Visited']['ToOrdRate']['ytd']  # 昨天同时的转换率
        item['ToOrdRate_ytdRate'] = data['content']['summary']['Visited']['ToOrdRate']['ytdRate']  # 转换率环比
        item['PV'] = data['content']['summary']['Visited']['PV']['value']  # 浏览量
        item['PV_channelPercent'] = data['content']['summary']['Visited']['PV']['channelPercent']  # 浏览量占全部渠道
        item['PV_ytdTimeRate'] = data['content']['summary']['Visited']['PV']['ytdTimeRate']  # 浏览量环比
        item['PV_ytdTime'] = data['content']['summary']['Visited']['PV']['ytdTime']  # 昨天同时的浏览量
        item['PV_ytdPercent'] = data['content']['summary']['Visited']['PV']['ytdPercent']  # 浏览量占昨天的浏览量
        item['ShopCollectNum'] = data['content']['summary']['Visited']['ShopCollectNum']['value']  # 店铺收藏数
        item['CartUserNum'] = data['content']['summary']['Visited']['CartUserNum']['value']  # 加购人数
        item['UV'] = data['content']['summary']['Visited']['UV']['value']  # 访客数
        item['UV_channelPercent'] = data['content']['summary']['Visited']['UV']['channelPercent']  # 访客数占全部渠道
        item['UV_ytdTimeRate'] = data['content']['summary']['Visited']['UV']['ytdTimeRate']  # 访客数环比
        item['UV_ytdTime'] = data['content']['summary']['Visited']['UV']['ytdTime']  # 昨天同时的访客数
        item['UV_ytdPercent'] = data['content']['summary']['Visited']['UV']['ytdPercent']  # 访客数占昨天的访客数
        item['realTime']=data['content']['realTime']
        item['compareTime'] = data['content']['compareTime']
        item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item
    
    
    