# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import web
import time
from jd_shangzhi.items import JdShangzhiliuliangItem
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

replenish_history = 0
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}


class ShangzhiLiuliangSpider(scrapy.Spider):
    name = "shangzhi_liuliang"
    allowed_domains = ["sz.jd.com"]

    def time_parse(self, t):
        t = int(t)
        today = datetime.date.today()
        oneday = datetime.timedelta(days=t)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def scan_need_request(self):
        if replenish_history == 1:
            return True
        else:
            sql_spider_front = "select * from hillinsight.t_spider_jdweizhi_spider where `dt`='%s' and `spider_name`='%s'" % (
                self.time_parse(1), 't_spider_jdweizhi_flow_source')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_flow_source'))
                return True

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
        # self.time_parse(1)
        for j, i in enumerate(self.brand_list):
            cookies = json.loads(i[1])
            shom_name = i[0]
            for dt in self.time_range(start_date, yester_day):
                parameter = {'PC': 20, 'APP': 2, '微信': 3, '手Q': 4, 'M端': 1}
                for i in parameter:
                    url = 'https://sz.jd.com/viewflow/getSourceChannelData.ajax?date={date}&endDate={date}&indChannel={tt}&startDate={date}'
                    s = parameter.get(i)
                    url = url.format(tt=s, date=dt)
                    yield scrapy.Request(url, headers=headers, cookies=cookies,
                                         meta={'cookiejar': j, 'date': dt, 'Account': shom_name, 'source': i, 'tt': s},
                                         dont_filter=True)

    def parse(self, response):
        datas = json.loads(response.body.decode())
        datas = datas['content']['data']
        for data in datas:
            item = JdShangzhiliuliangItem()
            item['category1'] = data[0]
            if item['category1'] == '京东付费':
                item['fufei'] = '收费'
            else:
                item['fufei'] = '免费'
            id1 = data[1]
            #如果不加python3会报错
            item['fathername']='null'
            item['category2'] = 'null'
            item['category3'] = 'null'
            item['sourceid']=data[1]
            item['fathersourceid']='null'
            item['peer_UV'] = data[2]
            item['shop_UV'] = data[3]
            item['shop_UV_rate'] = data[4]
            item['uv_zhanbi'] = data[6]
            item['uv_zhanbi_rate'] = data[7]
            item['shop_CustRate'] = data[30]
            item['shop_CustRate_rate'] = data[31]
            item['scan'] = data[15]
            item['scan_rate'] = data[16]
            shom_name = response.meta['Account']
            item['shop_name'] = shom_name
            date = response.meta['date']
            item['date'] = date
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['source'] = response.meta['source']
            yield item
            tt = response.meta['tt']
            url = 'https://sz.jd.com/viewflow/getSourceChildrenData.ajax?date={date}&endDate={date}&id1={id1}&indChannel={tt}&startDate={date}'
            url = url.format(tt=tt, date=date, id1=id1)
            yield scrapy.Request(url, headers=headers,
                                 meta={'cookiejar': response.meta['cookiejar'], 'date': date, 'Account': shom_name,
                                       'category1': data[0], 'id1': id1, 'fathername':data[0],'tt': tt, 'source': response.meta['source'],
                                       'fufei': item['fufei']},
                                 dont_filter=True, callback=self.get_item_category2)

    def get_item_category2(self, response):
        datas = json.loads(response.body.decode())
        datas = datas['content']['data']
        for data in datas:
            item = JdShangzhiliuliangItem()
            item['category1'] = response.meta['category1']
            item['category2'] = data[0]
            item['category3'] = 'null'
            item['sourceid']=data[1]
            item['fathersourceid']=response.meta['id1']
            item['fathername']=response.meta['fathername']
            id1 = response.meta['id1']
            id2 = data[1]
            item['peer_UV'] = data[2]
            item['shop_UV'] = data[3]
            item['shop_UV_rate'] = data[4]
            item['uv_zhanbi'] = data[6]
            item['uv_zhanbi_rate'] = data[7]
            item['shop_CustRate'] = data[30]
            item['shop_CustRate_rate'] = data[31]
            item['scan'] = data[15]
            item['scan_rate'] = data[16]
            shom_name = response.meta['Account']
            item['shop_name'] = shom_name
            date = response.meta['date']
            item['date'] = date
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['source'] = response.meta['source']
            item['fufei'] = response.meta['fufei']
            yield item
            tt = response.meta['tt']
            if data[-3]:
                url = 'https://sz.jd.com/viewflow/getSourceChildrenData.ajax?date={date}&endDate={date}&id1={id1}&id2={id2}&indChannel={tt}&startDate={date}'
                url = url.format(tt=tt, date=date, id2=id2, id1=id1)
                yield scrapy.Request(url, headers=headers,
                                     meta={'cookiejar': response.meta['cookiejar'],
                                           'date': date, 'Account': shom_name,
                                           'category1': response.meta['category1'], 'category2': data[0],
                                           'id1': id1, 'id2': id2,'fathername':data[0], 'source': response.meta['source'],
                                           'fufei': item['fufei']},
                                     dont_filter=True, callback=self.get_item_category3)

    def get_item_category3(self, response):
        datas = json.loads(response.body.decode())
        datas = datas['content']['data']
        for data in datas:
            item = JdShangzhiliuliangItem()
            item['category1'] = response.meta['category1']
            item['category2'] = response.meta['category2']
            item['category3'] = data[0]
            item['sourceid']=data[1]
            item['fathersourceid']=response.meta['id2']
            item['fathername']=response.meta['fathername']
            item['peer_UV'] = data[2]
            item['shop_UV'] = data[3]
            item['shop_UV_rate'] = data[4]
            item['uv_zhanbi'] = data[6]
            item['uv_zhanbi_rate'] = data[7]
            item['shop_CustRate'] = data[30]
            item['shop_CustRate_rate'] = data[31]
            item['scan'] = data[15]
            item['scan_rate'] = data[16]
            shom_name = response.meta['Account']
            item['shop_name'] = shom_name
            date = response.meta['date']
            item['date'] = date
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['source'] = response.meta['source']
            item['fufei'] = response.meta['fufei']
            yield item


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    