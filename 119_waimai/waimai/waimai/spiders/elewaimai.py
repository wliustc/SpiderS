# -*- coding: utf-8 -*-
import scrapy
import pymysql
import json
import time
from waimai.items import WaimaieleItem

class ElewaimaiSpider(scrapy.Spider):
    name = "elewaimai"
    allowed_domains = ["www.ele.me"]
    def start_requests(self):
        conn = pymysql.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        sql='select count(*) from `o2o`.t_hh_waimai_shop_info where frm="饿了么";'
        cur.execute(sql)
        count=cur.fetchall()
        count=int(count[0]['count(*)'])
        for i in range(0,count,10000):
            sql = '''
                          select shop_id, concat('https://mainsite-restapi.ele.me/shopping/v1/menu?restaurant_id=', shop_id) url
                          from t_hh_waimai_shop_info
                          where frm='饿了么' limit %s,10000;
                        ''' %i
            cur.execute(sql)
            temps=cur.fetchall()
            for temp in temps:
                yield scrapy.Request(temp['url'],dont_filter=True,meta={'item':{'shop_id':temp['shop_id']}})

    def parse(self, response):
        json_data = json.loads(response.body)
        if not json_data:
            return
        for serials in json_data:
            if 'foods' not in serials or not serials['foods']:
                continue
            for food in serials['foods']:
                item=WaimaieleItem()
                orig_price = food['specfoods'][0]['original_price']
                if not orig_price:
                    orig_price = 0.0
                price = food['specfoods'][0]['price']
                item.update( {
                    'frm': '饿了么',
                    'goods_id': food['specfoods'][0]['food_id'],
                    'goods_name': food['name'],
                    'category': serials['name'],
                    'shop_id': response.meta['item']['shop_id'],
                    'orig_price': orig_price,
                    'price': price,
                    'skus': json.dumps(food['specfoods']),
                    'month_sales': food['month_sales'],
                    'dt':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                })
                yield item

