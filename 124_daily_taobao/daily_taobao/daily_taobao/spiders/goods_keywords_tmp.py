# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pyhs2
import time
from daily_taobao.items import GoodsKeywordsItem
import datetime
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}



class Goods_Keywords_Tmp_Spider(scrapy.Spider):

    name = 'goods_keywords_tmp_spider'

    def start_requests(self):
        with pyhs2.connect(host='10.15.1.16', port=10000, authMechanism="PLAIN", user='zyliu', password='zyliu',
                           database='ods') as conn:
            with conn.cursor() as cur:
                the_day = time.strftime('%Y-%m-%d', time.localtime())
                # the_day = '2018-01-04'
                cur.execute(
                    "select goods_id from ods.daily_goodsList where (dt='2017-11-08' or dt='2017-11-07' or "
                    "dt='2017-12-03' or dt='2018-01-04' or dt='{}') and user_id in (446338500,890482188,"
                    "133227658,1993730769,772352677,167873659, 98563612, 353042333, 1731961317, 353042353, 829273025, "
                    "2940972233, 2940677727, 435878238, 281917995, 737997431, 458599810, 1739810699, 1574853209, "
                    "1893742894, 1122478447, 373327370, 2647118809, 2786693231, 2434852658, 3000560259, 1916102784, "
                    "656650799, 2074964291, 708668355, 720472756, 356579667, 1731961317,98563612,1689954831,387266832"
                    ",2073309259,325718097,1891339807,834807033,1974964452,372602234,167486422,356374102,"
                    "320083279,411832242,1602582004,2428721558,1574853209,2986712394,2183615086,2424477833,1754310760,1754310760,1122478447,3000560259,2652614726,533230328,2935707588,2945786195,2074690906,3458347554,3383168585,2366121327,3099864367,106852162,152579056,1754310760,783329018,1600687454,205919815,113484749,94092459,6655,2978259752) group by goods_id".format(the_day))
                # print '************'
                for i in cur.fetch():
                    nid = i[0]
                    url = 'https://rate.tmall.com/listTagClouds.htm?itemId={}&isAll=true&isInner=true&t=1510632615425' \
                          '&_ksTS=1510632615425_2407&callback=jsonp2408'.format(nid)
                    yield scrapy.Request(url, headers=header, callback=self.parse_keyword, meta={'nid': nid
                                                                                                 }, dont_filter=True)

    def parse_keyword(self, response):
        content = str(response.body).decode('gb18030', 'ignore').encode('utf-8')
        nid = response.meta['nid']
        pattern = re.search('jsonp.*?\(([\s\S]*?}})', content)
        print pattern.group(1)
        json_con = json.loads(pattern.group(1))
        tag_list = json_con.get('tags').get('tagClouds')
        for tag_con in tag_list:
            keyword = tag_con['tag']
            count_num = tag_con['count']
            sentiment = str(tag_con['posi'])
            url = 'https://detail.m.tmall.com/item.htm?id={}'.format(nid)
            yield scrapy.Request(url, headers=header, callback=self.parse_shop, meta=
            {'nid': nid, 'keyword': keyword, 'count_num': count_num, 'sentiment': sentiment}, dont_filter=True)

    def parse_shop(self, response):
        items = GoodsKeywordsItem()
        nid = response.meta['nid']
        keyword = response.meta['keyword']
        count_num = response.meta['count_num']
        sentiment = response.meta['sentiment']
        if sentiment == 'True':
            sentiment = '1'
        elif sentiment == 'False':
            sentiment = '-1'
        content = str(response.body).decode('gb18030', 'ignore').encode('utf-8')
        pattern1 = re.search('"shopName":"(.*?)"', content)
        shop_name = pattern1.group(1)
        pattern2 = re.search('"品牌":"([\s\S]*?)"', content)
        brand = pattern2.group(1)
        dt = time.strftime('%Y-%m-%d', time.localtime())
        # dt = '2018-01-10'
        items['nid'] = nid
        items['shop_name'] = shop_name
        items['brand'] = brand
        items['keyword'] = keyword
        items['count_num'] = count_num
        items['sentiment'] = sentiment
        items['dt'] = dt
        yield items
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    