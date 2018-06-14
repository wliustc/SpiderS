# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from dateutil.relativedelta import relativedelta
import web
import xlrd
import pandas
import time
import sys
from jd_shangzhi.items import JdShangzhiliuliangdownItem

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

class ShangzhiFlowSourceDownSpider(scrapy.Spider):
    name = "shangzhi_flow_source_down"
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
            self.time_parse(1), 't_spider_jdweizhi_flow_source_down')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_flow_source_down'))
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
                url = 'https://sz.jd.com/viewflow/exportFlowData.ajax'
                yield scrapy.FormRequest(url, headers=headers, cookies=cookies,
                                    formdata={
                                    'date':dt,
                                    'endDate':dt,
                                    'startDate':dt,
                                    'type':'day',
                                    },
                                     meta={'shop_name':shom_name,'date': dt, 'cate': u'核心指标', 'Account': shom_name},
                                     dont_filter=True)

    def parse(self, response):
        workbook=xlrd.open_workbook(file_contents=response.body)
        data=pandas.read_excel(io=workbook,sheet_name='sheet1',header=[0,1], engine='xlrd')
        data_m=pandas.DataFrame()
        for da in data.columns.levels[0]:
            temp=data[da].copy()
            temp['数据类型']=da
            data_m=data_m.append(temp)

        for row in data_m.iterrows():
            date=response.meta['date'].split('-')
            del date[0]
            date='-'.join(date)
            if row[0]==date:
                item=JdShangzhiliuliangdownItem()
                item['shop_name'] =response.meta[u'shop_name']
                item['source'] =   row[1][u'数据类型']
                item['shop_UV'] = row[1][u'访客数']
                item['peer_UV'] =  row[1][u'访客数_同行同级']
                item['PV'] =  row[1][u'浏览量']
                item['peer_PV'] =   row[1][u'浏览量_同行同级']
                item['jumplose'] =  row[1][u'跳失率']
                item['peer_jumplose'] =   row[1][u'跳失率_同行同级']
                item['per_PV'] =  row[1][u'人均浏览量']
                item['peer_per_PV'] = row[1][u'人均浏览量_同行同级']
                item['avg_time'] =  row[1][u'平均停留时长']
                item['peer_avg_time'] =  row[1][u'平均停留时长_同行同级']
                item['new_UV'] = row[1][u'新访客数']
                item['peer_new_UV'] = row[1][u'新访客数_同行同级']
                item['old_UV'] =  row[1][u'老访客数']
                item['peer_old_UV'] =  row[1][u'老访客数_同行同级']
                item['date'] =response.meta['date']
                item['dt'] =time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
    
    
    