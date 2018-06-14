# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\my_program\python_study')
import scrapy
import pymysql
import json
import Geohash as geohash
import time
from waimai.items import WaimaieleShoplistItem

GRAB_TYPE_CATEGORY = 1
GRAB_TYPE_SHOPLIST = 2

class ElewaimaishoplistSpider(scrapy.Spider):
    name = "elewaimaishoplist"
    allowed_domains = ["www.ele.me"]

    def start_requests(self):
        conn = pymysql.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        sql='select count(*) from `o2o`.`t_hh_gaode_hotspots`;'
        cur.execute(sql)
        count=cur.fetchall()
        count=int(count[0]['count(*)'])
        for i in range(0,count,10000):
            sql = 'select city, lng, lat, spot_name, spot_id from t_hh_gaode_hotspots limit %s,10000;' %i
            cur.execute(sql)
            temps=cur.fetchall()
            for i,r in enumerate(temps):
                if r['lng']<r['lat']:
                    a=r['lng']
                    r['lng']=r['lat']
                    r['lat']=a
                r['lat'] = round(r['lat'], 5)
                r['lng'] = round(r['lng'], 5)
                url = "https://mainsite-restapi.ele.me/shopping/v2/restaurant/category?"
                url += "latitude=%s&longitude=%s" % (r['lat'], r['lng'])
                yield  scrapy.Request(url,dont_filter=True,callback=self.parse_category,meta={'item':{
                    'lat':r['lat'],'lng':r['lng'],'city':r['city'],'spot_id':r['spot_id'],'spot_name':r['spot_name'],
                }})
                time.sleep(1)

    def __parse_category(self, json_data):
        cates = []
        for item in json_data:
            if 'sub_categories' not in item:
                continue
            cate1_name = item['name']
            cate1_id = item['id']
            cates.append({
                'cate1_id': cate1_id,
                'cate1_name': cate1_name
            })
            for item2 in item['sub_categories']:
                cate2_id = item2['id']
                cate2_name = item2['name']
                cates.append({
                    'cate1_id': cate1_id,
                    'cate1_name': cate1_name,
                    'cate2_id': cate2_id,
                    'cate2_name': cate2_name
                })
        return cates

    def parse_category(self, response):
        json_data = json.loads(response.body)
        cates = self.__parse_category(json_data)
        geo_hash_val = geohash.encode(response.meta['item']['lat'], response.meta['item']['lng'], precision=11)
        for cate in cates:
            cate_id = cate['cate1_id']
            if 'cate2_id' in cate:
                cate_id = cate['cate2_id']
            url = "https://mainsite-restapi.ele.me/shopping/restaurants?extras%5B%5D=activities"
            url += "&geohash=%s&latitude=%s&limit=24&longitude=%s" % (
            geo_hash_val, response.meta['item']['lat'], response.meta['item']['lng'])
            url += "&restaurant_category_ids%%5B%%5D=%s&sign=%s&offset=0" % (cate_id, int(time.time() * 1000))
            request_context = {
                'url': url,
                'grab_type': GRAB_TYPE_SHOPLIST,
                'cate1': cate['cate1_name'],
                'city': response.meta['item']['city'],
                'spot_id': response.meta['item']['spot_id'],
                'spot_name': response.meta['item']['spot_name'],
                'lng': response.meta['item']['lng'],
                'lat': response.meta['item']['lat'],
                'offset': 0
            }
            if 'cate2_id' in cate:
                request_context['cate2'] = cate['cate2_name']
            yield scrapy.Request(url,dont_filter=True,callback=self.parse_shop,meta={'item':request_context})


    def parse_shop(self,response):  #解析商店列表并且生成下一个链接。如果返回的内容为空说明已经到左后一页。不返回了。
        json_data=json.loads(response.body)
        results = self.__parse_shop_list(json_data,response.meta['item'])
        if results:
            request_context = response.meta['item']
            request_context['offset'] += 24
            url = "%s&offset=%s" % (request_context['url'].split('&offset=')[0], request_context['offset'])
            request_context['url'] = url
        for temp in results:
            item = WaimaieleShoplistItem()
            item['category2']=''
            item.update(temp)
            item['dt']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            yield item

    def __parse_shop_list(self, json_data,temp):
        results = []
        if not json_data:
            return results
        for si in json_data:
            item = {
                'frm': '饿了么',
                'shop_id': si['id'],
                'shop_name': si['name'],
                'city': temp['city'],
                'category1': temp['cate1'],
                'address': si['address'],
                'phone': '' if 'phone' not in si else si['phone'],
                'score': si['rating'],
                'lng': si['longitude'],
                'lat': si['latitude'],
                'month_sale_num': si['recent_order_num'],
                'context': json.dumps(si)
            }
            if 'cate2' in temp:
                item['category2'] = temp['cate2']
            results.append(item)
        return results
