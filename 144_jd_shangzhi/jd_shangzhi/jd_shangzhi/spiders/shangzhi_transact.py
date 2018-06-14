# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from dateutil.relativedelta import relativedelta
import web
import time
from jd_shangzhi.items import JdShangTransctItem
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
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


class ShangzhiTransactSpider(scrapy.Spider):
    name = "shangzhi_transact"
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
            self.time_parse(1), 't_spider_jdweizhi_transact')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_transact'))
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
            # 交易概况  可以
            for dt in self.time_range(start_date, yester_day):
                situation_url = '''https://sz.jd.com/trade/getSummaryData.ajax?channel=99&date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(situation_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'url': situation_url, 'Account': shom_name},
                                     dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body.decode())
        if 'length' not in data.keys():
            return
        item = JdShangTransctItem()
        shop_name = response.meta['Account']
        # 下单商品件数
        item['OrdProNum'] = data['content']['OrdProNum']['value']
        # 下单百分比
        rates = data['content']['OrdProNum']['rate']
        if not rates:
            rates=0
        item['OrdProNum_rate'] = "%.2f%%" % (rates * 100)
        # 客单价
        item['CustPriceAvg'] = data['content']['CustPriceAvg']['value']
        # 百分比
        CustPriceAvg_rates = data['content']['CustPriceAvg']['rate']
        if not CustPriceAvg_rates:
            CustPriceAvg_rates=0
        item['CustPriceAvg_rate'] = "%.2f%%" % (CustPriceAvg_rates * 100)
        # 人均浏览量
        item['AvgDepth'] = data['content']['AvgDepth']['value']
        # 百分比
        AvgDepth_rates = data['content']['AvgDepth']['rate']
        if not AvgDepth_rates:
            AvgDepth_rates=0
        item['AvgDepth_rate'] = "%.2f%%" % (AvgDepth_rates * 100)
        # 平均停留时长
        item['AvgStayTime'] = data['content']['AvgStayTime']['value']
        # 百分比
        AvgStayTime_rates = data['content']['AvgStayTime']['rate']
        if not AvgStayTime_rates:
            AvgStayTime_rates=0
        item['AvgStayTime_rate'] = "%.2f%%" % (AvgStayTime_rates * 100)
        # 下单转化率
        item['ToOrdRate'] = data['content']['ToOrdRate']['value']
        # 百分比
        ToOrdRate_rates = data['content']['ToOrdRate']['rate']
        if not ToOrdRate_rates:
            ToOrdRate_rates=0
        item['ToOrdRate_rate'] = "%.2f%%" % (ToOrdRate_rates * 100)
        # 下单金额
        item['OrdAmt'] = data['content']['OrdAmt']['value']
        # 百分比
        OrdAmt_rates = data['content']['OrdAmt']['rate']
        if not OrdAmt_rates:
            OrdAmt_rates=0
        item['OrdAmt_rate'] = "%.2f%%" % (OrdAmt_rates * 100)
        # 跳失率
        item['SkipOut'] = data['content']['SkipOut']['value']
        # 百分比
        SkipOut_rates = data['content']['SkipOut']['rate']
        if not SkipOut_rates:
            SkipOut_rates=0
        item['SkipOut_rate'] = "%.2f%%" % (SkipOut_rates * 100)
        # 浏览量
        item['PV'] = data['content']['PV']['value']
        # 百分比
        PV_rates = data['content']['PV']['rate']
        if not PV_rates:
            PV_rates=0
        item['PV_rate'] = "%.2f%%" % (PV_rates * 100)
        # 下单客户数
        item['OrdCustNum'] = data['content']['OrdCustNum']['value']
        # 百分比
        OrdCustNum_rates = data['content']['OrdCustNum']['rate']
        if not OrdCustNum_rates:
            OrdCustNum_rates=0
        item['OrdCustNum_rate'] = "%.2f%%" % (OrdCustNum_rates * 100)
        # 下单单量
        item['OrdNum'] = data['content']['OrdNum']['value']
        # 百分比
        OrdNum_rates = data['content']['OrdNum']['rate']
        if not OrdNum_rates:
            OrdNum_rates=0
        item['OrdNum_rate'] = "%.2f%%" % (OrdNum_rates * 100)
        # 访客数
        item['UV'] = data['content']['UV']['value']
        # 百分比
        UV_rates = data['content']['UV']['rate']
        if not UV_rates:
            UV_rates=0
        item['UV_rate'] = "%.2f%%" % (UV_rates * 100)
        item['shop_name'] = shop_name
        item['date'] = response.meta['date']
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item





    
    
    
    
    
    
    
    
    
    
    
    
    