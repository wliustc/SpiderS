# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import SecondTableItem
import datetime
import time
import json
import web
# http://compass.vis.vip.com/homepage/flow/overview?callback=jQuery3210356254914678965_1515066009315&brandStoreName=%E4%BB%96%E5%A5%B9TATA&dateType=D&detailType=D&beginDate=2017-12-05&endDate=2018-01-03&_=1515066009329

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
# before = '2017-01-01'


class Second_Table_Sports_Spider(scrapy.Spider):

    name = 'second_table_sports_spider'
    sum_uv = 0
    brand_num = 0
    total_item = []

    def start_requests(self):
        crawl_day = datetime.datetime.now().strftime('%Y-%m-%d')
        #crawl_day = '2018-03-01'
        the_signal = ''
        data = db.query("select sign from t_spider_vip_sign where dt='{}' and spider_name='{}'".format(crawl_day,
                                                                                                       'second_table_sports_spider'))
        for t in data:
            the_signal = t.sign
        if the_signal == '1':
            pass
        else:
            for brand in brand_list:
                url = 'http://compass.vis.vip.com/homepage/flow/overview?callback=jQuery3210356254914678965_{}&brandStor' \
                      'eName={}&dateType=D&detailType=D&beginDate={}&endDate={}&_={}'.format\
                    (int(time.time()*1000), brand, before, today, int(time.time()*1000))
                yield scrapy.Request(url, cookies=cookie, callback=self.second_parse, dont_filter=True, meta={'brand': brand})

    def second_parse(self, response):
        brand = response.meta['brand']
        content = response.body
        Second_Table_Sports_Spider.brand_num += 1
        if '"code":"0"' not in content:
            content = re.findall('jQuery3210356254914678965_\d+\(([\s\S]*?)\);', content)[0]
            con_json = json.loads(content)
            groups_list = con_json['singleResult']['chart']['groups']
            flow_list = con_json['singleResult']['chart']['data']['flowEntrance']
            for i in range(len(groups_list)):
                flow = flow_list[i]
                group = groups_list[i]
                Second_Table_Sports_Spider.sum_uv = Second_Table_Sports_Spider.sum_uv + float(flow[-1]['uv'])
                for item in flow:
                    items = SecondTableItem()
                    items['the_date'] = item['x']
                    items['uv'] = item['uv']
                    items['proportion'] = item['y']
                    items['group_'] = group
                    items['brand'] = brand
                    Second_Table_Sports_Spider.total_item.append(items)
        if Second_Table_Sports_Spider.brand_num == 10 and Second_Table_Sports_Spider.sum_uv != 0:
            for item in Second_Table_Sports_Spider.total_item:
                yield item
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    