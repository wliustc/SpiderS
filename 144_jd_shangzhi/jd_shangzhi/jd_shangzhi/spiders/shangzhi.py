# -*- coding: utf-8 -*-
import scrapy
# from login import login_test
import datetime
import json
from dateutil.relativedelta import relativedelta
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}


# Account  店铺名称
# cookies = {u'ceshi3.com': u'000', u'_jrdb': u'1514430172439', u'__jdc': u'251704139', u'pin': u'CAT-%E5%95%86%E6%99%BA', u'_jrda': u'1', u'_tp': u'nPNfhG0upNy%2FBEMaE6KEHgTH84qRu%2FgWt2nrkX6ncs4%3D', u'TrackID': u'1bsxRtUskUn98DgHfmDXfweEM6erwT0d5I70BCUOCWTg8R-38jE-g5dCG1OzH-K5Dy7kAJz-mkbJs84kBXE4DCK__H8rZOxEC5I1aBOQBbZo', u'__jdb': u'251704139.4.15144301630881660201413|1.1514430163', u'_pst': u'CAT-%E5%95%86%E6%99%BA', u'JSESSIONID': u'64504FB581E4EB29F741B4CDBECE8218.s1', u'__jdu': u'15144301630881660201413', u'thor': u'BA5051C5705DB5F7CF31766FE70A9F5AFD92D4E27BF14BDAA594E897C60220DC1891FEDF436C4853854BEA9A1A158ECCBCFA80D0E0BF04773D391780EF218D0D000DE59A29707821C8B759575C268AC5386F1D4F04BA29BC7276C6B96DFA3032E4B288E0FAF9A41FAA0A4AA2538D472B248765169CF552A860DDF45EFB34AFE0', u'pinId': u'aiFQXum9imwuMLcvCZiWGA', u'__jdv': u'122270672|direct|-|none|-|1514430163092', u'unick': u'CAT-%E5%95%86%E6%99%BA', u'__jda': u'251704139.15144301630881660201413.1514430163.1514430163.1514430163.1', u'3AB9D23F7A4B3C9B': u'Y2OIIDSR666O7W2FXUPJSRH7AQYH2CUO46QR2BCWHIMRD4WAVMQNJOHJZ4V3LU5SYNP76YSDDHIRRFMT2GGMWSRJF4', u'wlfstk_smdl': u'jp5sx7f5ko5e387l8c6bsdkhr4luu8fd'}
class JdShangzhiSpider(scrapy.Spider):
    name = 'shangzhi'
    allowed_domains = []
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(JdShangzhiSpider, self).__init__(*args, **kwargs)
        self.brand_list = []
        sql = '''select * from t_spiedr_JD_cookies'''
        for i in db.query(sql):
            cookies = str(i.get('cookies'))
            name = i.get('shop_name')
            cookies_tuple = name, cookies
            self.brand_list.append(cookies_tuple)

    def parse(self, response):
        item = {}
        if b'浏览器版本过低' in response.body:
            response.request.headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            yield response.requset
            return
        item['data'] = response.body
        item['cate'] = response.meta['cate']
        item['shop_name'] = response.meta['Account']
        item['date'] = response.meta['date']
        if item['cate'] == u'流量来源':
            item['source'] = response.meta['source']
        yield item

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
        start_date = '2018-01-09' 
        #self.time_parse(1)
        yester_day = '2018-01-10'
        #self.time_parse(1)
        for i in self.brand_list:
            cookies = json.loads(i[1])
            shom_name = i[0]
            # 交易概况  可以
            for dt in self.time_range(start_date, yester_day):
                situation_url = '''https://sz.jd.com/trade/getSummaryData.ajax?channel=99&date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(situation_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'交易概况', 'url': situation_url, 'Account': shom_name},
                                     dont_filter=True)
                # 流量概括

                Flow_rate_url = 'https://sz.jd.com/viewflow/getCoreIndexData.ajax?date={date}&endDate={endDate}&startDate={startDate}'.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(Flow_rate_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'流量概括', 'Account': shom_name}, dont_filter=True)
                # 商品概览
                merchandise_url = '''https://sz.jd.com/productDetail/getProductSummary.ajax?channel=99&date={date}&endDate={endDate}&startDate={startDate}&type=0'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(merchandise_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'商品概览', 'Account': shom_name}, dont_filter=True)
                # 商品明细 spu
                Goods_detail_url_spu = '''https://sz.jd.com/productDetail/getProductList.ajax?categoryType=0&channel=99&date={date}&endDate={endDate}&goodsId=&second=999999&skuId=&startDate={startDate}&third=&type=0'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(Goods_detail_url_spu, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'商品明细spu', 'Account': shom_name}, dont_filter=True)
                # 商品明细 sku
                Goods_detail_url_sku = '''https://sz.jd.com/productDetail/getProductList.ajax?categoryType=0&channel=99&date={date}&endDate={endDate}&goodsId=&second=999999&spuId=&startDate={startDate}&third=&type=1'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(Goods_detail_url_sku, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'商品明细sku', 'Account': shom_name}, dont_filter=True)
                # 交易特征
                feature_url = '''https://sz.jd.com/trade/getChannelFeatureData.ajax?channel=99&date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(feature_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'交易特征', 'Account': shom_name}, dont_filter=True)
                # 售后分析
                After_sale_url = '''https://sz.jd.com/afterSale/dataSummary.ajax?date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(After_sale_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'售后分析', 'Account': shom_name}, dont_filter=True)
                # 下单客户分析
                Place_order_url = '''https://sz.jd.com/cust/order/detail.ajax?date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(Place_order_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'下单客户分析', 'Account': shom_name}, dont_filter=True)
                # 核心指标
                Core_KPI_url = '''https://sz.jd.com/index/getIndexData.ajax?date={date}&endDate={endDate}&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=self.time_month(dt))
                yield scrapy.Request(Core_KPI_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'核心指标', 'Account': shom_name}, dont_filter=True)
                # 流量来源
                parameter = {'PC': 20, 'APP': 2, '微信': 3, '手Q': 4, 'M端': 1}
                for i in parameter:
                    url = '''https://sz.jd.com/index/flowAnalysis/sourceTop.ajax?channel={tt}&date={date}'''
                    s = parameter.get(i)
                    url = url.format(tt=s, date=dt)
                    yield scrapy.Request(url, headers=headers, cookies=cookies,
                                         meta={'date': dt, 'cate': u'流量来源', 'Account': shom_name, 'source': i},
                                         dont_filter=True)
                # 订单明细 （最多返回日期订单的最近1000条订单信息）
                order_details_url = '''https://sz.jd.com/trade/getOrderDetailList.ajax?channel=99&date={date}&endDate={endDate}&orderId=&startDate={startDate}'''.format(
                    date=dt, endDate=dt, startDate=dt)
                yield scrapy.Request(order_details_url, headers=headers, cookies=cookies,
                                     meta={'date': dt, 'cate': u'订单明细', 'Account': shom_name}, dont_filter=True)


    
    
    