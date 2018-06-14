# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import FangPriceItem
import json
import web
import MySQLdb

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0;+http://www.baidu.com/search/spider.html)",
    "referer": 'https://www.baidu.com'
}
header1 = {
    # 'access-control-allow-headers': 'X-Requested-With',
    # 'upgrade-insecure-requests': '1',
    #'cookie': 'global_cookie=ktvc403xb78rwxt5309oikjwk1lj46xlksj; new_search_uid=2a61efd1f0ed4c32a75d13bda1e40a31; searchLabelN=3_1498556289_7318%5B%3A%7C%40%7C%3A%5D5d824b8d1609fd5782b5cf460c5ab1df; searchConN=3_1498556289_7608%5B%3A%7C%40%7C%3A%5Dd71276b021ed33231ded7efdf2b25513; sf_source=; s=; newhouse_chat_guid=19E2A109-FCFE-AD01-F49A-9DC5F53599B2; __jsluid=9dd4b3582d182a14ccaffbd2b24520fe; Captcha=69334F6770767355716244524179332F7075584C72614A717751776D416F50785065554B42566633645877334D655A77586A724A5845772F574446724A346363304B58535235634D7279513D; newhouse_user_guid=9C61F966-6ED1-13C8-5E01-8F05C4719FF6; city=www; unique_cookie=U_ktvc403xb78rwxt5309oikjwk1lj46xlksj*193; __utma=147393320.1923800830.1498045478.1499679176.1499740245.21; __utmb=147393320.3.10.1499740245; __utmc=147393320; __utmz=147393320.1499740245.21.7.utmcsr=fangjia.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/pghouse-c0bj/a01-h315-i32-j3100/; mencity=yt',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
cookies = {
    'global_cookie': 'ktvc403xb78rwxt5309oikjwk1lj46xlksj',
    'new_search_uid': '2a61efd1f0ed4c32a75d13bda1e40a31',
    'searchLabelN': '3_1498556289_7318%5B%3A%7C%40%7C%3A%5D5d824b8d1609fd5782b5cf460c5ab1df',
    'searchConN': '3_1498556289_7608%5B%3A%7C%40%7C%3A%5Dd71276b021ed33231ded7efdf2b25513',
    'sf_source': '',
    's': '',
    'newhouse_chat_guid': '19E2A109-FCFE-AD01-F49A-9DC5F53599B2',
    '__jsluid': '9dd4b3582d182a14ccaffbd2b24520fe',
    'Captcha': '69334F6770767355716244524179332F7075584C72614A717751776D416F50785065554B42566633645877334D655A77586A724A5845772F574446724A346363304B58535235634D7279513D',
    'newhouse_user_guid': '9C61F966-6ED1-13C8-5E01-8F05C4719FF6',
    'city': 'www',
    'unique_cookie': 'U_ktvc403xb78rwxt5309oikjwk1lj46xlksj*193',
    '__utma': '147393320.1923800830.1498045478.1499679176.1499740245.21',
    '__utmb': '147393320.3.10.1499740245',
    '__utmc': '147393320',
    '__utmz': '147393320.1499740245.21.7.utmcsr=fangjia.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/pghouse-c0bj/a01-h315-i32-j3100/',
    'mencity': 'yt',
}
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
db2 = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



class Fang_Price_Spider(scrapy.Spider):

    name = 'fang_price_spider'

    def start_requests(self):
        sql = '''
               select csi_id, src_uid
               from t_hh_community_source_info
               where frm='搜房'
              '''
        results = db.query(sql)
        for data in results:
            csi_id = data['csi_id']
            src_uid = data['src_uid']
            url = 'https://m.fang.com/fangjia/?c=pinggu&a=ajaxGetDetailDraw&topnum=12&newcode=%s' % (src_uid)

            yield scrapy.Request(url, headers=header1, cookies=cookies, callback=self.jsonparse, meta={'csi_id': csi_id},
                                 dont_filter=True)

    def jsonparse(self, response):
        json_data = json.loads(response.body)
        csi_id = response.meta['csi_id']
        price_data = json_data['xqcode']
        items = FangPriceItem()
        if price_data and 'price' in price_data:
            price = price_data['price'][-1]
            if price > 0:
                items['csi_id'] = csi_id
                items['avg_price'] = price
                # key_str = ','.join('`%s`' % k for k in items.keys())
                # value_str = ','.join(
                #     'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v) for v in
                #     items.values())
                # kv_str = ','.join(
                #     "`%s`=%s" % (k, 'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v))
                #     for (k, v)
                #     in items.items())
                # sql = "INSERT INTO t_hh_community_source_info(%s) VALUES(%s)" % (key_str, value_str)
                # sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
                # db.query(sql)

                yield items
    
    
    