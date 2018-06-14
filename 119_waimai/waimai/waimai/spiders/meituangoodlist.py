# -*- coding: utf-8 -*-
import scrapy
import pymysql
import execjs
import json
import time
import re
from waimai.items import WaimaimeituanItem
class MeituangoodlistSpider(scrapy.Spider):
    name = "meituangoodlist"
    # allowed_domains = ["waimai.meituan.com"]

    def start_requests(self):
        # conn = pymysql.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
        #                        connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
        conn = pymysql.connect(host='localhost', user='root', passwd='111111', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        sql = '''
                select shop_id, concat('http://waimai.meituan.com/restaurant/', shop_id) url
                from t_hh_waimai_shop_info 
                where frm='美团外卖'
               '''
        cur.execute(sql)
        temps = cur.fetchall()
        for r in temps:
            url = r['url']
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'waimai.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)",
            }

            yield scrapy.Request(url, headers=headers,
                                 meta={'item': {'shop_id':r['shop_id']}},
                                 dont_filter=True)


    def parse(self, response):
        categorys=response.css('.category')
        for category in categorys:
            cate=category.css('h3::attr("title")').extract()[0]
            goods=category.css('div[id]')
            for good in goods:
                item=WaimaimeituanItem()
                id=good.css('::attr("id")').extract()[0]
                data=(good.css('[id="foodcontext-'+id+'"]::text').extract()[0])
                data=json.loads(data)
                item['dt']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                item['frm']='美团外卖'
                item['goods_id'] = data['id']
                item['goods_name'] = data['name']
                item['category'] = cate
                item['shop_id'] = response.meta['item']['shop_id']
                item['orig_price'] = data['sku'][0]['origin_price']
                item['price'] = data['sku'][0]['price']
                item['skus'] = str(data['sku'])
                month_sales=re.sub('[^0-9]','',''.join(good.css('.sold-count ::text').extract()).strip())
                if not month_sales:
                    month_sales=0
                month_sales=int(month_sales)
                item['month_sales']=month_sales
                yield item