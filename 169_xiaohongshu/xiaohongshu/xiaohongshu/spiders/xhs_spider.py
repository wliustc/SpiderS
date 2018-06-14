# -*- coding: utf-8 -*-
import scrapy
import json
import re
from xiaohongshu.items import XiaohongshuItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Xhs_Spider(scrapy.Spider):

    name = 'xhs_spider'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'xiaohongshu.middlewares_mine.ProxyMiddleware': 110}
    }

    def start_requests(self):
        url = 'https://www.xiaohongshu.com/api/store/v1/classifications'

        yield scrapy.Request(url, dont_filter=True, callback=self.parse_cate)

    def parse_cate(self, response):
        content = response.body
        json_con = json.loads(content)
        cate_list = json_con['data']
        for cate1 in cate_list[1:]:
            cate1_name = cate1['name']
            cate2_list = cate1['entries']
            for cate2 in cate2_list:
                cate2_name = cate2['name']
                cate3_list = cate2.get('entries')
                if cate3_list:
                    for cate3 in cate3_list:
                        cate3_name = cate3['name']
                        for sort in ['sales_qty', 'new_arrival', 'price_asc', 'price_desc']:
                            for num in range(1,11):
                                url = 'https://www.xiaohongshu.com/api/store/ps/products?keyword={}&' \
                                      'filters=%5B%5D&mode=word_search&page={}&size=100&sort={}'.format(cate3_name, num,
                                                                                                        sort)
                                yield scrapy.Request(url, callback=self.parse_list, meta={
                                    'cate1_name': cate1_name, 'cate2_name': cate2_name, 'cate3_name': cate3_name
                                }, dont_filter=True)
                else:
                    cate3_name = ''
                    for sort in ['sales_qty', 'new_arrival', 'price_asc', 'price_desc']:
                        for num in range(1, 11):
                            url = 'https://www.xiaohongshu.com/api/store/ps/products?keyword={}&' \
                                  'filters=%5B%5D&mode=word_search&page={}&size=100&sort={}'.format(cate2_name, num,
                                                                                                    sort)
                            yield scrapy.Request(url, callback=self.parse_list, meta={
                                'cate1_name': cate1_name, 'cate2_name': cate2_name, 'cate3_name': cate3_name
                            }, dont_filter=True)

    def parse_list(self, response):
        content = response.body
        cate1_name = response.meta['cate1_name']
        cate2_name = response.meta['cate2_name']
        cate3_name = response.meta['cate3_name']
        json_con = json.loads(content)
        goods_list = json_con['data']['items']
        for info in goods_list:
            discount_price = info['discount_price']
            goods_id = info['id']
            origin_price = info.get('price')
            if not origin_price:
                origin_price = discount_price
            title = info['title']
            shop_name = info['vendor_name']
            member_price = info.get('member_price')
            url = 'https://pages.xiaohongshu.com/goods/{}'.format(goods_id)
            yield scrapy.Request(url, callback=self.parse_goods, meta={'cate1_name': cate1_name,
            'cate2_name': cate2_name, 'cate3_name': cate3_name, 'discount_price': discount_price, 'goods_id': goods_id,
            'origin_price': origin_price, 'title': title, 'shop_name': shop_name, 'member_price': member_price},
                                 dont_filter=True)

    def parse_goods(self, response):
        content = response.body
        cate1_name = response.meta['cate1_name']
        cate2_name = response.meta['cate2_name']
        cate3_name = response.meta['cate3_name']
        discount_price = response.meta['discount_price']
        goods_id = response.meta['goods_id']
        origin_price = response.meta['origin_price']
        title = response.meta['title']
        shop_name = response.meta['shop_name']
        member_price = response.meta['member_price']
        pattern1 = re.search('href="https://www.xiaohongshu.com/page/brands/(.*?)"', content)
        brand_id = pattern1.group(1)
        pattern2 = re.search('"shortName":"(.*?)"', content)
        shortName = pattern2.group(1)
        pattern3 = re.search('class="goods-name__brand-name"[\s\S]*?>([\s\S]*?)<', content)
        brand = pattern3.group(1).strip()
        url = 'https://www.xiaohongshu.com/items/{}/attributes'.format(goods_id)
        yield scrapy.Request(url, dont_filter=True, meta={'cate1_name': cate1_name,
            'cate2_name': cate2_name, 'cate3_name': cate3_name, 'discount_price': discount_price, 'goods_id': goods_id,
            'origin_price': origin_price, 'title': title, 'shop_name': shop_name, 'member_price': member_price, 'brand_id': brand_id,
            'shortName': shortName, 'brand': brand}, callback=self.parse_attr)

    def parse_attr(self, response):
        content = response.body
        items = XiaohongshuItem()
        cate1_name = response.meta['cate1_name']
        cate2_name = response.meta['cate2_name']
        cate3_name = response.meta['cate3_name']
        discount_price = response.meta['discount_price']
        goods_id = response.meta['goods_id']
        origin_price = response.meta['origin_price']
        title = response.meta['title']
        shop_name = response.meta['shop_name']
        member_price = response.meta['member_price']
        brand_id = response.meta['brand_id']
        shortName = response.meta['shortName']
        brand = response.meta['brand']
        pattern = re.search('({"seller_id"[\s\S]*?)\);<', content)
        json_con = json.loads(pattern.group(1))
        attr_list = json_con['variants']
        items['cate1_name'] = cate1_name
        items['cate2_name'] = cate2_name
        items['cate3_name'] = cate3_name
        items['discount_price'] = discount_price
        items['goods_id'] = goods_id
        items['origin_price'] = origin_price
        items['title'] = title
        items['shop_name'] = shop_name
        items['member_price'] = member_price
        items['brand_id'] = brand_id
        items['shortName'] = shortName
        items['brand'] = brand
        items['attr_list'] = str(attr_list)

        yield items


    