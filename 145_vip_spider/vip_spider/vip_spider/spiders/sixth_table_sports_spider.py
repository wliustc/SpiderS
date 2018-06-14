# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import SixthTableItem
import datetime
import time
import json
import web

#cookie = {'mars_cid': '1528853260938_b58bbf894de05e2b2ea6abb6fef40b7f', 'user_type': '1', 'shop_id': '18894', 'codes': '605599', 'user_id': '68384', 'compassV': '2.4', 'guideV': '2.3', 'mars_pid': '0', 'vc_token': 'eyJ0b2tlbiI6ImM2OTg5YzAwY2Q3NjUxMzRiYWFkN2Q0YTcxYWI5YTdjIiwidG9rZW4xIjoiNGZlZGY2MzQ5ZDcyNjIxMGI0YjJjNGZiOTM1ZWFlMDEiLCJ2ZW5kb3JJZCI6IjE4ODk0IiwidXNlck5hbWUiOiJ5bGluQGhpbGxpbnNpZ2h0LmNvbSIsInZlbmRvckNvZGUiOiI2MDU1OTkiLCJ1c2VySWQiOiI2ODM4NCIsInZpc1Nlc3Npb25JZCI6Im1nM2htN2c0cTJ0Z2k3YnRkZW9iNGo4YzQwIiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D', 'permission': '_95_96_105_106_107_112_114_116_117_119_121_123_129_130_137_140_149_150_152_196_197_200_201_203_206_207_208_209_210_211_212_213_214_229_242_243_244_245_259_260_261_279_288_289_290_293_304_315_316_317_338_340_342_360_389_394_408_414_415_427_428_429_435_442_528_530_572_834_', 'vendor_id': '605599', '_ga': 'GA1.2.1394506578.1528853244', 'vendor_code': '605599', 'axdata': 'ZWYwZjQ5ZGU2ZGMyMzlkYzY1YTM1OTM5YmZkOWYyNjQ3MGIyY2YzZjJlODY3ZWZhOGJjMDkxMjI2OThmZDU3ZQ%3D%3D', 'visadminvipvipcom': 'mg3hm7g4q2tgi7btdeob4j8c40', 'expire': '1528885658', 'user': 'ylin%40hillinsight.com', 'nickname': '%E6%9E%97%E9%98%B3', 'visit_id': 'CDF3A631EC9BA22627D9EFDE1DE41ABA', 'mars_sid': 'e61094f5f1daa4d50291e697d97c33a8', 'tipInfoV': '2.3', '_gid': 'GA1.2.1625875626.1528853244', 'shops': '18894', 'jobnumber': '20180105'}
import ast
db2 = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                  host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

data = db2.query('select cookie from t_spider_vip_sign_cookie_sport;')
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
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
now = datetime.datetime.now()
today = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
before = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
#before = '2017-10-01'


class Sixth_Table_Spider(scrapy.Spider):

    name = 'sixth_table_sports_spider'

    def start_requests(self):
        crawl_day = datetime.datetime.now().strftime('%Y-%m-%d')
        the_signal = ''
        data = db.query("select sign from t_spider_vip_sign where dt='{}' and spider_name='{}'".format(crawl_day,
                                                                                                       'sixth_table_sports_spider'))
        for t in data:
            the_signal = t.sign
        if the_signal == '1':
            pass
        else:
            for brand in brand_list:
                url = 'http://compass.vis.vip.com/dangqi/reject/getRejectOverview?callback=jQuery32108590923814259758_{}' \
                      '&brandStoreName={}&dateType=D&detailType=D&beginDate={}&endDate={}&_={}'.format\
                    (int(time.time()*1000), brand, before, today, int(time.time()*1000))
                yield scrapy.Request(url, callback=self.json_parse, cookies=cookie, dont_filter=True, meta={'brand': brand})

    def json_parse(self, response):
        content = response.body
        brand = response.meta['brand']
        items = SixthTableItem()
        content = re.findall('jQuery32108590923814259758_\d+\((.*?)\);', content)[0]
        if '"code":"1"' in content:
            json_con = json.loads(content)
            gmv_list = json_con['singleResult']['chart']['data']['sales'][0]
            sales_list = json_con['singleResult']['chart']['data']['salesCnt'][0]
            return_list = json_con['singleResult']['chart']['data']['salesReturnCnt'][0]
            return_gmv_list = json_con['singleResult']['chart']['data']['salesReturnAmt'][0]
            ReturnPercent_list = json_con['singleResult']['chart']['data']['salesReturnPercent'][0]
            reject_list = json_con['singleResult']['chart']['data']['rejectCnt'][0]
            reject_gmv_list = json_con['singleResult']['chart']['data']['rejectAmt'][0]
            rejectPercent_list = json_con['singleResult']['chart']['data']['rejectPercent'][0]
            returnPercent_list2 = json_con['singleResult']['chart']['data']['returnPercent'][0]
            date_list = json_con['singleResult']['chart']['scale']
            for i in range(len(date_list)):
                items['the_date'] = date_list[i]
                items['brand'] = brand
                items['sales'] = gmv_list[i]['y']
                items['salesCnt'] = sales_list[i]['y']
                items['salesReturnCnt'] = return_list[i]['y']
                items['salesReturnAmt'] = return_gmv_list[i]['y']
                items['salesReturnPercent'] = ReturnPercent_list[i]['y']
                items['rejectCnt'] = reject_list[i]['y']
                items['rejectAmt'] = reject_gmv_list[i]['y']
                items['rejectPercent'] = rejectPercent_list[i]['y']
                items['returnPercent'] = returnPercent_list2[i]['y']

                yield items

    
    
    
    
    
    
    
    
    
    
    
    
    
    