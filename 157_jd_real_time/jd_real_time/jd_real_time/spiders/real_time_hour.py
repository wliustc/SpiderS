# -*- coding: utf-8 -*-
import scrapy
import web
import json
import time
import datetime
from jd_real_time.items import JdRealTimeHourItem

replenish_history=0
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}

class RealTimeHourSpider(scrapy.Spider):
    name = "real_time_hour"
    allowed_domains = ["sz.jd.com"]
    start_urls = ['http://sz.jd.com/']
    def time_parse(self, t):
        t = int(t)
        today = datetime.date.today()
        oneday = datetime.timedelta(days=t)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def time_month(self, dt):
        return (
            datetime.datetime.strptime(dt, "%Y-%m-%d") - relativedelta(months=1) + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d")

    def time_range(self, start_time, end_time):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        while start_time <= end_time:
            yield start_time.strftime("%Y-%m-%d")
            start_time = start_time + datetime.timedelta(days=1)

    def start_requests(self):
        self.brand_list = []
        if replenish_history==1:
            sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
            (shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
            group by shop_name;'''
            for i in db.query(sql):
                cookies = str(i.get('cookies'))
                name = i.get('shop_name')
                cookies_tuple = name, cookies
                self.brand_list.append(cookies_tuple)
        else:
            
            sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
        			(shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
        			and `shop_name` not in(select `shop_name` from t_spider_jd_real_time_trend where `date`='%s' and hour='%s')
        			group by shop_name;''' %( time.strftime('%Y-%m-%d', time.localtime(time.time())),int(datetime.datetime.now().hour)-1)
            for i in db.query(sql):
                cookies = str(i.get('cookies'))
                name = i.get('shop_name')
                cookies_tuple = name, cookies
                self.brand_list.append(cookies_tuple)   
        start_date = self.time_parse(1)
        yester_day = self.time_parse(1)
        if  datetime.datetime.now().hour==0 and replenish_history==0:
            start_date = self.time_parse(2)
        for i in self.brand_list:
            cookies = json.loads(i[1])
            shop_name = i[0]
            for dt in self.time_range(start_date, yester_day):
                After_sale_url = 'https://sz.jd.com/realTime/getRealTimeSeries.ajax?date=%s' \
                                 '&indChannel=99'   %dt
                yield scrapy.Request(After_sale_url, headers=headers, cookies=cookies,
                                 meta={'date': dt,'Account': shop_name},
                                 dont_filter=True)

    def parse(self, response):
        temp=json.loads(response.body)
        if replenish_history==0:
            item=JdRealTimeHourItem()
            datas=temp['content']['sourceTrend']
            if len(datas['OrdProNum']) == 0:
                return
            hours=len(datas['OrdProNum'])-1
            for i in range(0,hours):
                item['shop_name'] = response.meta['Account']
                item['OrdProNum'] = datas['OrdProNum'][i][0]
                item['PV'] = datas['PV'][i][0]
                item['OrdAmt'] = datas['OrdAmt'][i][0]
                item['OrdCustNum'] = datas['OrdCustNum'][i][0]
                item['OrdNum'] = datas['OrdNum'][i][0]
                item['UV'] = datas['UV'][i][0]
                item['date'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item['hour'] = i
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
        else:
            datas=temp['content']['sourceTrend']
            for i in range(0,24):
                item = JdRealTimeHourItem()
                item['shop_name'] = response.meta['Account']
                item['OrdProNum'] = datas['OrdProNumInd'][i][0]
                item['PV'] = datas['PVInd'][i][0]
                item['OrdAmt'] = datas['OrdAmtInd'][i][0]
                item['OrdCustNum'] = datas['OrdCustNumInd'][i][0]
                item['OrdNum'] = datas['OrdNumInd'][i][0]
                item['UV'] = datas['UVInd'][i][0]
                item['date'] = response.meta['date']
                item['hour'] = i
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item

    
    
    
    
    
    
    
    
    
    
    
    
    
    