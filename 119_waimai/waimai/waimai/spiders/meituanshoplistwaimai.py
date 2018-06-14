# -*- coding: utf-8 -*-
import scrapy
import pymysql
import re
import json
import time
import Geohash
import hashlib

GRAB_TYPE_CATEGORY = 1
GRAB_TYPE_SHOPLIST = 2
from urllib.parse import quote
from waimai.items import WaimaimeituanShoplistItem
from waimai.items import WaimaimeituanItem
import execjs
#会记录IP和浏览器版本访问信息,如果防爬需要换个浏览器,经过更换浏览器头,发现是cookie算错的问题,但是没有纠正，
#换了不需要传cookies的浏览器,准备攻破他的防线,但是chrome的header被封。
class MeituanshoplistwaimaiSpider(scrapy.Spider):
    name = "meituanshoplistwaimai"


    def start_requests(self):
        conn = pymysql.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        sql = '''
                select city, spot_name, spot_id, lng, lat
                from t_hh_gaode_hotspots limit 10;
              '''
        cur.execute(sql)
        temps = cur.fetchall()
        for i,r in enumerate(temps):
            if r['lng']<r['lat']:
                a=r['lng']
                r['lng']=r['lat']
                r['lat']=a
            a=Geohash.encode(r['lat'], r['lng'], 12)
            url='http://waimai.meituan.com/home/' +a


            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'waimai.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                "User-Agent": "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            }
            yield scrapy.Request(url,headers=headers,meta={'item':{'lat':r['lat'],'lng':r['lng'],
                                                            'spot_name':r['spot_name'],'base_url':url},
                                                           },dont_filter=True)


    def parse(self, response):
        uuid=''
        offset=0
        if response.url.split('/')[3]=='home':
            cook_data=response.headers.getlist('Set-Cookie')
            for tmp in cook_data:
                if tmp.decode().split('=')[0]=='w_uuid':
                    uuid=tmp.decode().split('=')[1]
            offset=1
        elif response.url.split('/')[3]=='ajax':
            uuid=response.meta['item']['uuid']
            offset=response.meta['item']['offset']
        if offset:
            temp = 'http://waimai.meituan.com/ajax/poilist?'+'classify_type=cate_all&sort_type=0&price_type=0&support_online_pay=0&support_invoice=0&' \
                   'support_logistic=0&page_offset=%s&page_size=20&%s&' \
                   'originUrl=http%%253A%%252F%%252Fwaimai.meituan.com%%252Fhome%%252Fwx4g8c8q847n' % (offset, uuid)
        with open(r'D:\my_program\python_study\scrapy_test\waimai\waimai\meituan_shopjs.js','r') as f:
            shop_list_js=f.read()
            phantom = execjs.get('PhantomJS')
            getpass = phantom.compile(shop_list_js)
            toke = getpass.call('a',temp)

        url='http://waimai.meituan.com/ajax/poilist?_token='+toke
        header={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'waimai.meituan.com',
            'Origin':'http://waimai.meituan.com',
            'Proxy-Connection':'keep-alive',
            'Referer':response.meta['item']['base_url'],
            "User-Agent": "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        }
        if response.url.split('/')[3]=='ajax':
            data=json.loads(response.body)
            for item in self.get_page_data(data):
                yield item
            if len(data['data']['poiList'])<20:
                return
        yield scrapy.FormRequest(url,method='POST',headers=header,
                                 formdata={
                                     'classify_type': 'cate_all',
                                     'sort_type':'0',
                                     'price_type': '0',
                                     'support_online_pay': '0',
                                     'support_invoice': '0',
                                     'support_logistic': '0',
                                     'page_offset':str(offset),
                                     'page_size': '20',
                                     'uuid': uuid,
                                     'platform': '1',
                                     'partner': '4',
                                     'originUrl':response.meta['item']['base_url'],
                                 },
                                meta={'item':{'base_url':response.meta['item']['base_url'],'uuid':uuid,
                                            'offset':offset+20}})

    def get_page_data(self,data):
        datas=data['data']['poiList']
        for data in datas:
            item=WaimaimeituanShoplistItem()
            item['shop_name'] = data['wmPoi4Web']['name']
            item['frm'] = '美团'
            item['city'] = '上海'
            item['address']= data['wmPoi4Web']['address']
            item['phone']=data['wmPoi4Web']['call_center']
            item['shop_id'] = data['wmPoi4Web']['wm_poi_id']
            item['score'] = data['wmPoi4Web']['wm_poi_score']
            item['in_time_delivery_percent']=data['wmPoi4Web']['in_time_delivery_percent']
            item['in_time_delivery_percent_ranking']=data['wmPoi4Web']['in_time_delivery_percent_ranking']
            item['avg_delivery_time']=data['wmPoi4Web']['avg_delivery_time']
            item['avg_delivery_time_ranking']=data['wmPoi4Web']['avg_delivery_time_ranking']
            item['lng'] = data['wmPoi4Web']['longitude']
            item['lat'] = data['wmPoi4Web']['latitude']
            item['category1']=data['wmPoiTagDicList'][0]['name']
            item['min_send_price'] = data['wmPoi4Web']['wmCPoiLbs']['min_price']
            item['month_sale_num'] = data['wmPoi4Web']['month_sale_num']
            item['dt']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['uni_hash_code']=hashlib.md5((item['shop_name']+item['address']).encode()).hexdigest()
            yield item
            url = 'http://waimai.meituan.com/restaurant/'+str(data['wmPoi4Web']['wm_poi_id'])
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'waimai.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)",
            }
            yield scrapy.Request(url, headers=headers,
                                 meta={'item': {'shop_id':data['wmPoi4Web']['wm_poi_id'],'uni_hash_code':item['uni_hash_code']}},
                                 dont_filter=True,callback=self.get_goods_data)

    def get_goods_data(self,response):
        categorys = response.css('.category')
        for category in categorys:
            cate = category.css('h3::attr("title")').extract()[0]
            goods = category.css('div[id]')
            for good in goods:
                item = WaimaimeituanItem()
                id = good.css('::attr("id")').extract()[0]
                data = (good.css('[id="foodcontext-' + id + '"]::text').extract()[0])
                data = json.loads(data)
                item['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                item['frm'] = '美团'
                item['goods_id'] = data['id']
                item['goods_name'] = data['name']
                item['category'] = cate
                item['shop_id'] = response.meta['item']['shop_id']
                item['orig_price'] = data['sku'][0]['origin_price']
                item['price'] = data['sku'][0]['price']
                item['uni_hash_code']=response.meta['item']['uni_hash_code']
                item['skus'] = str(data['sku'])
                month_sales = re.sub('[^0-9]', '', ''.join(good.css('.sold-count ::text').extract()).strip())
                if not month_sales:
                    month_sales = 0
                month_sales = int(month_sales)
                item['month_sales'] = month_sales
                yield item