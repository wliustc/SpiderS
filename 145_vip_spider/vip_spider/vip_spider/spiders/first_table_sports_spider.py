# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import VipSpiderItem
import datetime
import time
import json
import web
# http://compass.vis.vip.com/homepage/metric/queryAllMetric?callback=jQuery321028968414347674765_1515059790241&brandStoreName=%E4%BB%96%E5%A5%B9TATA&dateType=D&detailType=D&beginDate=2017-12-05&endDate=2018-01-03&contrastBeginDate=2017-11-05&contrastEndDate=2017-12-04&_=1515059790263

#cookie = {'mars_cid': '1528853260938_b58bbf894de05e2b2ea6abb6fef40b7f', 'user_type': '1', 'shop_id': '18894', 'codes': '605599', 'user_id': '68384', 'compassV': '2.4', 'guideV': '2.3', 'mars_pid': '0', 'vc_token': 'eyJ0b2tlbiI6ImM2OTg5YzAwY2Q3NjUxMzRiYWFkN2Q0YTcxYWI5YTdjIiwidG9rZW4xIjoiNGZlZGY2MzQ5ZDcyNjIxMGI0YjJjNGZiOTM1ZWFlMDEiLCJ2ZW5kb3JJZCI6IjE4ODk0IiwidXNlck5hbWUiOiJ5bGluQGhpbGxpbnNpZ2h0LmNvbSIsInZlbmRvckNvZGUiOiI2MDU1OTkiLCJ1c2VySWQiOiI2ODM4NCIsInZpc1Nlc3Npb25JZCI6Im1nM2htN2c0cTJ0Z2k3YnRkZW9iNGo4YzQwIiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D', 'permission': '_95_96_105_106_107_112_114_116_117_119_121_123_129_130_137_140_149_150_152_196_197_200_201_203_206_207_208_209_210_211_212_213_214_229_242_243_244_245_259_260_261_279_288_289_290_293_304_315_316_317_338_340_342_360_389_394_408_414_415_427_428_429_435_442_528_530_572_834_', 'vendor_id': '605599', '_ga': 'GA1.2.1394506578.1528853244', 'vendor_code': '605599', 'axdata': 'ZWYwZjQ5ZGU2ZGMyMzlkYzY1YTM1OTM5YmZkOWYyNjQ3MGIyY2YzZjJlODY3ZWZhOGJjMDkxMjI2OThmZDU3ZQ%3D%3D', 'visadminvipvipcom': 'mg3hm7g4q2tgi7btdeob4j8c40', 'expire': '1528885658', 'user': 'ylin%40hillinsight.com', 'nickname': '%E6%9E%97%E9%98%B3', 'visit_id': 'CDF3A631EC9BA22627D9EFDE1DE41ABA', 'mars_sid': 'e61094f5f1daa4d50291e697d97c33a8', 'tipInfoV': '2.3', '_gid': 'GA1.2.1625875626.1528853244', 'shops': '18894', 'jobnumber': '20180105'}
import ast
db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                  host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

data = db.query('select cookie from t_spider_vip_sign_cookie_sport;')
cookie = data[0].get('cookie')
cookie = ast.literal_eval(cookie)

brand_list = [
                        'New Balance',
                        'ASICS',
                        'ONITSUKA TIGER',
                        'UGG',
                        '匡威converse',
                        '彪马PUMA',
                        '耐克Nike',
                        '范斯vans',
                        '锐步Reebok',
                        '阿迪达斯adidas'
                    ]

now = datetime.datetime.now()
today = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
before = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
con_end = (now - datetime.timedelta(days=31)).strftime('%Y-%m-%d')
con_begin = (now - datetime.timedelta(days=60)).strftime('%Y-%m-%d')


class First_Table_Sports_Spider(scrapy.Spider):

    name = 'first_table_sports_spider'
    sum_sales = 0
    brand_num = 0
    total_item = []

    def start_requests(self):
        crawl_day = datetime.datetime.now().strftime('%Y-%m-%d')
        #crawl_day = '2018-03-03'
        the_signal = ''
        data = db.query("select sign from t_spider_vip_sign where dt='{}' and spider_name='{}'".format(crawl_day, 'first_table_sports_spider'))
        for t in data:
            the_signal = t.sign
        if the_signal == '1':
            pass
        else:
            for brand in brand_list:
                url = 'http://compass.vis.vip.com/homepage/metric/queryAllMetric?callback=jQuery3210289684143476747' \
                      '65_{}&brandStoreName={}&dateType=D&detailType=D&beginDate={}&endDate={}&contrastBeginDate={}&co' \
                      'ntrastEndDate={}&_={}'.format(int(time.time()*1000), brand, before, today,
                                                     con_begin, con_end, int(time.time()*1000))
                yield scrapy.Request(url, cookies=cookie, callback=self.first_parse, dont_filter=True, meta={'brand': brand})

    def first_parse(self, response):
        content = response.body
        First_Table_Sports_Spider.brand_num += 1
        content = re.findall('jQuery321028968414347674765_\d+\(([\s\S]*?)\);', content)[0]
        if '"code":"0"' not in content:
            con_json = json.loads(content)
            brand = response.meta['brand']
            # print con_json
            # raw_input("enter")
            sales_list = con_json['singleResult']['chart']['data']['sales'][0]
            cutGoodsMoney_list = con_json['singleResult']['chart']['data']['cutGoodsMoney'][0]
            rejectedPct_list = con_json['singleResult']['chart']['data']['rejectedPct'][0]
            flowUv_list = con_json['singleResult']['chart']['data']['flowUv'][0]
            flowConversion_list = con_json['singleResult']['chart']['data']['flowConversion'][0]
            orderCnt_list = con_json['singleResult']['chart']['data']['orderCnt'][0]
            consumerCount_list = con_json['singleResult']['chart']['data']['consumerCount'][0]
            avgUserSalesAmount_list = con_json['singleResult']['chart']['data']['avgUserSalesAmount'][0]
            avgOrderSalesAmount_list = con_json['singleResult']['chart']['data']['avgOrderSalesAmount'][0]
            stockAmtOnline_list = con_json['singleResult']['chart']['data']['stockAmtOnline'][0]
            stockCntOnline_list = con_json['singleResult']['chart']['data']['stockCntOnline'][0]
            saleStockAmt_list = con_json['singleResult']['chart']['data']['saleStockAmt'][0]
            goodsCnt_list = con_json['singleResult']['chart']['data']['goodsCnt'][0]
            couponAmt_list = con_json['singleResult']['chart']['data']['couponAmt'][0]
            for i in range(len(sales_list)):
                items = VipSpiderItem()
                items['the_date'] = sales_list[i]['x']
                items['brand'] = brand
                items['sales'] = sales_list[i]['y']
                First_Table_Sports_Spider.sum_sales = First_Table_Sports_Spider.sum_sales + float(sales_list[-1]['y'])
                items['cutGoodsMoney'] = cutGoodsMoney_list[i]['y']
                items['rejectedPct'] = rejectedPct_list[i]['y']
                items['flowUv'] = flowUv_list[i]['y']
                items['flowConversion'] = flowConversion_list[i]['y']
                items['orderCnt'] = orderCnt_list[i]['y']
                items['consumerCount'] = consumerCount_list[i]['y']
                items['avgUserSalesAmount'] = avgUserSalesAmount_list[i]['y']
                items['avgOrderSalesAmount'] = avgOrderSalesAmount_list[i]['y']
                items['stockAmtOnline'] = stockAmtOnline_list[i]['y']
                items['stockCntOnline'] = stockCntOnline_list[i]['y']
                items['saleStockAmt'] = saleStockAmt_list[i]['y']
                items['goodsCnt'] = goodsCnt_list[i]['y']
                items['couponAmt'] = couponAmt_list[i]['y']
                First_Table_Sports_Spider.total_item.append(items)
        if First_Table_Sports_Spider.brand_num == 10 and First_Table_Sports_Spider.sum_sales != 0:
            for item in First_Table_Sports_Spider.total_item:
                yield item
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    