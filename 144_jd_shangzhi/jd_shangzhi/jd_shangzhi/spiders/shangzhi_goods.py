# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from dateutil.relativedelta import relativedelta
import web
import time
from jd_shangzhi.items import JdShangGoodsItem
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

replenish_history=0
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           # 'Connection': 'keep-alive',
           'Connection': 'close',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}


class ShangzhiGoodsSpider(scrapy.Spider):
    name = "shangzhi_goods"
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

    def scan_need_request(self):
        if replenish_history == 1:
            return True
        else:
            sql_spider_front = "select * from hillinsight.t_spider_jdweizhi_spider where `dt`='%s' and `spider_name`='%s'" % (
            self.time_parse(1), 't_spider_jdweizhi_goods')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_goods'))
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
        start_date =self.time_parse(1)
        yester_day =self.time_parse(1)
        for i in self.brand_list:
            cookies = json.loads(i[1])
            shom_name = i[0]
            # 交易概况  可以
            for dt in self.time_range(start_date, yester_day):
                # 商品概览
                merchandise_url = '''https://sz.jd.com/productDetail/getProductSummary.ajax?channel=99&cmpType=0&date={date}&endDate={endDate}&startDate={startDate}&type=0'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(merchandise_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'商品概览', 'Account': shom_name}, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body.decode())
        item = JdShangGoodsItem()
        shop_name = response.meta['Account']
        try:
            for i in data['content']:
                item[i + '_value'] = data['content'].get(i).get('value')
                if data['content'].get(i).get('rate')==None:
                    item[i + '_rate']='-'
                else:
                    item[i + '_rate'] = "%.2f%%" % (data['content'].get(i).get('rate') * 100)
            for i in item:
                if i in ['goodsAddBuyRate_value', 'goodsConverRate_value', 'goodsSaleRate_value',
                     'goodsExposureRate_value']:
                    item[i] = "%.2f%%" % (item[i] * 100)
            item['shop_name'] = shop_name
            item['date'] = response.meta['date']
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield item
        except Exception as e:
            self.logger.error("error in %s,%s" %(shop_name,e))




    
    
    
    
    
    
    
    
    