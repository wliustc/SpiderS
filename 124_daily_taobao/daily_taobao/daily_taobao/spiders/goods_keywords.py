# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pyhs2
import time
from daily_taobao.items import GoodsKeywordsItem
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


class Goods_Keywords_Spider(scrapy.Spider):

    name = 'goods_keywords_spider'

    def start_requests(self):
        with pyhs2.connect(host='10.15.1.16', port=10000, authMechanism="PLAIN", user='zyliu', password='zyliu',
                           database='ods') as conn:
            with conn.cursor() as cur:
                the_day = time.strftime('%Y-%m-%d', time.localtime())
                cur.execute(
                    "select goods_id from ods.daily_goodsList where dt='{}' and user_id in (446338500,890482188,"
                    "133227658,1993730769,772352677,167873659, 98563612, 353042333, 1731961317, 353042353, 829273025, "
                    "2940972233, 2940677727, 435878238, 281917995, 737997431, 458599810, 1739810699, 1574853209, "
                    "1893742894, 1122478447, 373327370, 2647118809, 2786693231, 2434852658, 3000560259, 1916102784, "
                    "656650799, 2074964291, 708668355, 720472756, 356579667) group by goods_id".format(
                        the_day))
                for i in cur.fetch():
                    nid = i[0]
                    url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=14606167' \
                          '25586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=' \
                          '2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%2' \
                          '2{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C' \
                          '%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(nid)
                    print url
                    yield scrapy.Request(url, headers=header, callback=self.parse_detail, meta={'nid': nid, 'retry': 0},
                                         dont_filter=True)

    def parse_detail(self, response):
        items = GoodsKeywordsItem()
        content_json = json.loads(response.body)
        content_text = response.body
        nid = response.meta['nid']
        data = content_json['data']
        brand = ''
        pattern1 = re.search('"品牌":"(.*?)"', content_text)
        if pattern1:
            brand = pattern1.group(1)
        shop_name = ''
        pattern2 = re.search('"shopName":"(.*?)"', content_text)
        if pattern2:
            shop_name = pattern2.group(1)
        if data.get('rate'):
            rate_con = data['rate']
            if rate_con.has_key('keywords'):
                key_list = rate_con['keywords']
                for k in key_list:
                    keyword = k['word']
                    count_num = k['count']
                    sentiment = k['type']
                    dt = time.strftime('%Y-%m-%d', time.localtime())
                    items['brand'] = brand
                    items['shop_name'] = shop_name
                    items['nid'] = nid
                    items['keyword'] = keyword
                    items['count_num'] = count_num
                    items['sentiment'] = sentiment
                    items['dt'] = dt

                    yield items