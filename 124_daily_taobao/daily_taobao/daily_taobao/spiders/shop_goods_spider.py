# -*- coding: utf-8 -*-
import scrapy
import json
from daily_taobao.items import ShopGoodsItem
import pyhs2
import re
import time

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}



def get_regex_group1(_str, default=None):
    p = re.compile(r'^((?!https://sec.taobao.com/).)*$')
    m = p.search(_str)
    if m:
        return m.group(1)
    return default


def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj




class Shop_Goods_Spider(scrapy.Spider):

    name = 'shop_goods_spider'

    @staticmethod
    def _is_access_controlled(html):
        return get_regex_group1(html, None) is None

    @staticmethod
    def _is_access_controlled_url(url):
        if "alisec.taobao.com" in url:
            return True
        return False

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
                    "656650799, 2074964291, 708668355, 720472756, 356579667, 1731961317,98563612,1689954831,387266832"
                    ",2073309259,325718097,1891339807,834807033,1974964452,372602234,167486422,356374102,"
                    "320083279) group by goods_id".format(
                        the_day))
                for i in cur.fetch():
                    nid = i[0]
                    url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=14606167' \
                          '25586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=' \
                          '2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%2' \
                          '2{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C' \
                          '%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(nid)
                    #print url
                    yield scrapy.Request(url, headers=header, callback=self.parse_detail, meta={'nid': nid, 'retry': 0},
                                   dont_filter=True)

    def parse_detail(self, response):
        items = ShopGoodsItem()
        if Shop_Goods_Spider._is_access_controlled(response.body) and Shop_Goods_Spider._is_access_controlled_url(
                response.url):
            self.logger.warning(response.body)
            retry = response.meta['retry']
            retry += 1
            self.logger.warning("I'm fucking controlled! " + response.url)
            if retry > 3:
                yield {}
            else:
                nid = response.meta['nid']
                yield scrapy.Request(response.url, meta={'nid': nid, 'retry': retry}, callback=self.parse_detail,
                                     dont_filter=True)
        else:
            nid = response.meta['nid']
            content = {}
            content['nid'] = nid
            try:
                content['goods'] = json.loads(re.sub('\t', '', response.body))
                if get_json_hierarchy(content['goods'], ['data', 'item', 'itemId']):
                    pass
                else:
                    content = {}
            except:
                retry = response.meta['retry']
                retry += 1
                if retry > 3:
                    content = {}
                else:
                    yield scrapy.Request(response.url, meta={'nid': nid, 'retry': retry}, callback=self.parse_detail,
                                         dont_filter=True)
                self.logger.error('fuck for [{}]'.format(response.url))
            if content:
                items['data'] = {'content': content}
                items['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                #items['dt'] = '2017-11-02'
                yield items
                # yield {'content': content}
            # else:
            #     yield {}
    
    
    
    
    
    
    