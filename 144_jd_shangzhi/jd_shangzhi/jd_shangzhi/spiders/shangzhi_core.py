# -*- coding: utf-8 -*-
import scrapy
# from login import login_test
import datetime
import json
from dateutil.relativedelta import relativedelta
import web
import time
from jd_shangzhi.items import JdShangCoreItem
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
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


class ShangzhiCoreSpider(scrapy.Spider):
    name = "shangzhi_core"
    allowed_domains = ["sz.jd.com"]

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

    def scan_need_request(self):
        if replenish_history == 1:
            return True
        else:
            sql_spider_front = "select * from hillinsight.t_spider_jdweizhi_spider where `dt`='%s' and `spider_name`='%s'" % (
            self.time_parse(1), 't_spider_jdweizhi_ci')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_ci'))
                return True

    def start_requests(self):
        if not self.scan_need_request():
            return
        self.brand_list = []
        sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
        (shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
        group by shop_name;'''
        for i in db.query(sql):
            cookies = str(i.get('cookies'))
            name = i.get('shop_name')
            cookies_tuple = name, cookies
            self.brand_list.append(cookies_tuple)
        start_date = self.time_parse(1)
        yester_day = self.time_parse(1)
        for i in self.brand_list:
            cookies = json.loads(i[1])
            shom_name = i[0]
            for dt in self.time_range(start_date, yester_day):
                # 核心指标
                Core_KPI_url = '''https://sz.jd.com/index/getIndexData.ajax?date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=self.time_month(dt))
                yield scrapy.Request(Core_KPI_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'核心指标', 'Account': shom_name}, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body.decode())
        shop_name = response.meta['Account']
        item = JdShangCoreItem()
        data = data['content']['summary']
        # print data
        # 下单金额
        item['Orders_sum'] = data['OrdAmt']['value']
        # 下单金额无线占比
        
        temp=data['OrdAmt']['MobileRate']
        if not temp:
            temp=0
        item['Orders_rate'] = '%.2f%%' % ( temp * 100)
        # 较前一天
        
        temp=data['OrdAmt']['ComYesterdayRate']
        if not temp:
            temp=0
        item['OrdersRate'] = '%.2f%%' % (temp * 100)
        # 浏览量
        item['PV'] = data['PV']['value']
        # 浏览量无线占比
        
        temp=data['PV']['MobileRate']
        if not temp:
            temp=0
        item['PV_rate'] = '%.2f%%' % (temp * 100)
        # 较前一天
        temp=data['PV']['ComYesterdayRate']
        if not temp:
            temp=0
        item['PVRate'] = '%.2f%%' % (temp * 100)
        # 访客数
        item['UV'] = data['UV']['value']
        # 访客数无线占比
        temp=data['UV']['MobileRate']
        if not temp:
            temp=0
        item['UV_rate'] = '%.2f%%' % (temp * 100)
        # 较前一天
        temp=data['UV']['ComYesterdayRate']
        if not temp:
            temp=0
        item['UVRate'] = '%.2f%%' % (temp * 100)
        # 客单价
        item['CustPriceAvg'] = data['CustPriceAvg']['value']
        # 客单价无线客单
        item['CustPriceAvg_Price'] = data['CustPriceAvg']['MobileCustPrice']
        # 较前一天
        temp=data['CustPriceAvg']['ComYesterdayRate']
        if not temp:
            temp=0
        item['CustPriceAvg_rate'] = '%.2f%%' % (temp * 100)
        # 下单转化率
        temp=data['CustRate']['value']
        if not temp:
            temp=0
        item['CustRate'] = '%.2f%%' % (temp * 100)
        # 下单转化无线转化
        temp=data['CustRate']['MobileCustRate']
        if not temp:
            temp=0
        item['Cust_wireless_rate'] = '%.2f%%' % (temp * 100)
        # 较前一天
        temp=data['CustRate']['ComYesterdayRate']
        if not temp:
            temp=0
        item['Cust_rate'] = '%.2f%%' % (temp * 100)
        # 90天重复购买率
        temp=data['The90RepeatPurchaseRate']['value']
        if not temp:
            temp=0
        item['The90'] = '%.2f%%' % (temp * 100)
        # 90天重复购买率APP渠道占比
        temp=data['The90RepeatPurchaseRate']['AppCustRate']
        if not temp:
            temp=0
        item['The90Rate'] = '%.2f%%' % (temp * 100)
        # 较前一天
        temp=data['The90RepeatPurchaseRate']['ComYesterdayRate']
        if not temp:
            temp=0
        item['The90_rate'] = '%.2f%%' % (temp * 100)
        # 30天重复购买率
        temp=data['The30RepeatPurchaseRate']['value']
        if not temp:
            temp=0
        item['The30'] = '%.2f%%' % (temp * 100)
        # 30天重复购买率APP渠道占比
        temp=data['The30RepeatPurchaseRate']['AppCustRate']
        if not temp:
            temp=0
        item['The30Rate'] = '%.2f%%' % (temp * 100)
        # 较前一天
        temp=data['The30RepeatPurchaseRate']['ComYesterdayRate']
        if not temp:
            temp=0
        item['The30_rate'] = '%.2f%%' % (temp * 100)
        # 店铺关注人数
        item['ShopCollectNum'] = data['ShopCollectNum']['value']
        # 店铺关注人数APP渠道
        item['App_population'] = data['ShopCollectNum']['AppCustNum']
        # 较前一天
        temp=data['ShopCollectNum']['ComYesterdayRate']
        if not temp:
            temp=0
        item['ShopCollectNum_rate'] = '%.2f%%' % (temp * 100)
        item['shop_name'] = shop_name
        item['date'] = response.meta['date']
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item

    
    
    
    
    
    