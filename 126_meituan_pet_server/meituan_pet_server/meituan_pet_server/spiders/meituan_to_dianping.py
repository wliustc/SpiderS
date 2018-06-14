# -*- coding: utf-8 -*-
import scrapy
import sqlalchemy
import json
import time
from meituan_pet_server.items import Meituan_to_Dp_Item
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
class MeituanToDianpingSpider(scrapy.Spider):
    name = "meituan_to_dianping"
    allowed_domains = ["i.meituan.com"]
    handle_httpstatus_list = [500,503]

    def start_requests(self):
        conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                        connect_args={'charset': 'utf8'})
        cur=conn.connect()
        temp=cur.execute('SELECT distinct `deal_id`,`shop_id` FROM hillinsight.tuangou_meituan_deal_id where TO_DAYS( NOW( ) ) - TO_DAYS(`dt`) <= 3;')# where `dt`=DATE(now())
        temp=temp.fetchall()
        for i,tmp in enumerate(temp):
            deal_id=tmp[0]
            shop_id=tmp[1]
            url='https://i.meituan.com/general/platform/mttgdetail/mtdealbasegn.json?dealid=%s&shopid=%s&eventpromochannel=&stid=' %(deal_id,shop_id)
            header = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Host':'i.meituan.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,callback=self.get_item,meta={'cookiejar':i,'timerequest':0},errback=self.error_callback)

    def get_item(self,response):
        if response.status == 500 or response.status == 503:
            return
        item=Meituan_to_Dp_Item()
        temps=json.loads(response.body)
        item['mtdealid']=temps['mtDealGroupId']
        item['brandName'] = temps['brandName']
        item['solds'] = temps['solds']
        item['start_time'] = time.strftime("%Y-%m-%d",time.strptime(temps['start'],"%b %d, %Y %H:%M:%S %p"))
        item['end_time'] = time.strftime("%Y-%m-%d",time.strptime(temps['end'],"%b %d, %Y %H:%M:%S %p"))
        item['originalPrice'] = temps['originalPrice']
        item['title']=temps['title']
        item['coupontitle']=temps['coupontitle']
        item['price'] = temps['price']
        item['orderTitle'] = temps['orderTitle']
        item['dpDealGroupId']=temps['dpDealGroupId']
        item['shop_id']=temps['shop']['poiid']
        item['shop_name'] = temps['shop']['name']
        item['addr'] = temps['shop']['addr']
        item['avgscore'] = temps['shop']['avgscore']
        item['dpShopId'] = temps['shop']['dpShopId']
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
        try:
        	item['phone'] = temps['shop']['phone']
        except Exception as e:
            item['phone'] = None
        yield item
   
    def error_callback(self, failure):
        request = failure.request
        if request.meta['timerequest']>10:
            self.logger.error('qfliu retrytime out %s', request.url)
            return
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s ,%s,cookiejar %s,proxy %s', response.url,response.status,request.meta['cookiejar'],request.meta['proxy'])
            request.meta['timerequest'] += 1
            yield request
        elif failure.check(DNSLookupError):
            self.logger.error('DNSLookupError on %s', request.url)
            request.meta['timerequest'] += 1
            yield request
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error('TimeoutError on %s ,       cookiejar %s,proxy %s', request.url,request.meta['cookiejar'],request.meta['proxy'])
            request.meta['timerequest'] += 1
            yield request
    
    
    