# -*- coding: utf-8 -*-
import scrapy
import json
from daily_taobao.items import GoodsTmpItem
import pyhs2
import re
import time


def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj


def get_json_brand(_json_obj):
    for i in _json_obj:
        if u'品牌' in i:
            return i[u'品牌']
        else:
            for item in i:
                if u'品牌' in item:
                    return i[item]
    return ""


def parse_apiStack(_json):
    result = {}
    if _json and len(_json) == 1:
        for item in _json:
            tmp_json = json.loads(item['value'])
            tmp = get_json_hierarchy(tmp_json, ['item', 'sellCount'])
            if tmp or tmp == 0:
                result['sellCount'] = tmp
            tmp = get_json_hierarchy(tmp_json, ['delivery', 'from'])
            if tmp:
                result['item_loc'] = tmp
            tmp = get_json_hierarchy(tmp_json, ['delivery', 'postage'])
            if tmp:
                result['view_fee'] = tmp.replace(u'快递: ', r'')
            tmp = get_json_hierarchy(tmp_json, ['skuCore', 'sku2info', '0', 'quantity'])
            if tmp:
                result['quantity'] = tmp
            tmp = get_json_hierarchy(tmp_json, ['price', 'price', 'priceText'])
            if tmp:
                if '-' in tmp:
                    result['price_range'] = tmp
                    tmp = tmp.split('-')[0]
                result['view_price'] = tmp
            tmp = get_json_hierarchy(tmp_json, ['price', 'extraPrices'])
            if tmp:
                for it in tmp:
                    price = it['priceText']
                    if '-' in price:
                        price = price.split('-')[0]
                    result['reserve_price'] = price
                    break
            tmp = get_json_hierarchy(tmp_json, ['buyer', 'tmallMemberLevel'])
            if tmp or tmp == 0:
                result['isTmall'] = True
            else:
                result['isTmall'] = False
    return result


header = {
    'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Letv X500 Build/DBXCNOP5902605181S)'
}


class Daily_Goods_Danger(scrapy.Spider):

    name = 'daily_goods_danger'
    handle_httpstatus_list = [420, 419]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'daily_taobao.middlewares_mine.ProxyMiddleware': 100,
                                   'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110}
    }

    def start_requests(self):
        with pyhs2.connect(host='10.15.1.16', port=10000, authMechanism="PLAIN", user='zyliu', password='zyliu',
                           database='ods') as conn:
            with conn.cursor() as cur:
                # the_day = time.strftime('%Y-%m-%d', time.localtime())
                the_day = '2018-06-12'
                cur.execute("select nid_a FROM (SELECT a.nid_a, b.nid_b FROM (SELECT nid AS nid_a FROM ods.daily_taobao_item_info WHERE dt='2018-06-11') a LEFT JOIN (SELECT nid AS nid_b FROM ods.daily_taobao_item_info WHERE dt='{}') b ON a.nid_a=b.nid_b) c WHERE nid_b is null".format(the_day))
                for i in cur.fetch():
                    nid = i[0]
                    retry = 0
                    url = 'https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{}%22%2C%22detail_v%22%3A%223.1.0%22%7D&ttid=142857@taobao_iphone_7.10.3'.format(
                       nid)
                    #url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1460616725586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%22{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(
                     #   nid)
                    yield scrapy.Request(url, callback=self.parse_sell, meta={'nid': nid, 'retry': retry},
                                         headers=header, dont_filter=True)

    def parse_sell(self, response):
        items = GoodsTmpItem()
        nid = response.meta['nid']
        retry = response.meta['retry']
        content = response.body
        pattern = re.search('"sellCount\\\\":\\\\"(.*?)\\\\"', content)
        # pattern = re.search(u'月销(.*?)笔', content)
        if pattern and retry < 150:
            sellcount = pattern.group(1)
            json_con = json.loads(content)
            pattern1 = re.search('"itemId":.*?,"title":"(.*?)"', content)
            title = pattern1.group(1)
            pattern2 = re.search('"shopName":"(.*?)"', content)
            shop_name = pattern2.group(1)
            extra_info = ''
            props_json = get_json_hierarchy(json_con, ['data', 'props', 'groupProps'])
            if props_json:
                for i in props_json:
                    if u'基本信息' in i:
                        extra_info = i[u'基本信息']
                        break
            brand = ''
            for i in extra_info:
                if i.get(u'品牌'):
                    brand = i.get(u'品牌')
                    break
            # 上市时间
            time_to_market = ''
            for i in extra_info:
                if i.get(u'上市时间'):
                    time_to_market = i.get(u'上市时间')
                    break
                elif i.get(u'上市年份季节'):
                    time_to_market = i.get(u'上市年份季节')
                    break
                else:
                    continue
            # 款号
            model_num = ''
            for i in extra_info:
                if i.get(u'款号'):
                    model_num = i.get(u'款号')
                    break
            apiStack = parse_apiStack(get_json_hierarchy(json_con, ['data', 'apiStack']))
            price = get_json_hierarchy(apiStack, ['view_price'])
            commentcount = json_con['data']['item'].get('commentCount')
            favcount = json_con['data']['item'].get('favcount')
            pattern7 = re.search('"categoryId":"(.*?)"', content)
            categoryId = pattern7.group(1)
            pattern8 = re.search('"rootCategoryId":"(.*?)"', content)
            rootCategoryId = pattern8.group(1)
            quantity = get_json_hierarchy(apiStack, ['quantity'])
            # 图片链接
            image_list = json_con['data']['item'].get('images')
            image_str = ''
            if image_list:
                for image in image_list:
                    image_str = image_str + image + '|'
            # 适用对象
            sexual = ''
            for i in extra_info:
                if i.get(u'性别'):
                    sexual = i.get(u'性别')
                    break
                else:
                    sexual_list = ['男婴童', '男大童', '男小童', '女婴童', '女大童', '女小童', '幼童', '大童', '婴童', '小童']
                    for sexual2 in sexual_list:
                        if sexual2 in title:
                            sexual = sexual2
                            break
            # 吊牌价
            tag_price = ''
            for i in extra_info:
                if i.get(u'吊牌价'):
                    tag_price = i.get(u'吊牌价')
                    break
            # sku数量
            sku_count = '0'
            sku_list = json_con['data']['skuBase'].get('skus')
            if sku_list:
                sku_count = len(sku_list)
            price_range = get_json_hierarchy(apiStack, ['price_range'])
            reserve_price = get_json_hierarchy(apiStack, ['reserve_price'])
            items['nid'] = nid
            items['shop_name'] = shop_name
            items['title'] = title
            items['brand'] = brand
            items['sellcount'] = sellcount
            items['price'] = price
            items['price_range'] = price_range
            items['commentcount'] = commentcount
            items['categoryId'] = categoryId
            items['rootCategoryId'] = rootCategoryId
            items['quantity'] = quantity
            items['model_num'] = model_num
            items['sexual'] = sexual
            items['tag_price'] = tag_price
            items['time_to_market'] = time_to_market
            items['sku_count'] = sku_count
            items['reserve_price'] = reserve_price
            items['favcount'] = favcount
            items['image_str'] = image_str
            items['dt'] = '2018-06-12'
            yield items
        elif 'SUCCESS' in content and not pattern:
            pass
        elif retry > 100:
            pass
        else:
            url = 'https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{}%22%2C%22detail_v%22%3A%223.1.0%22%7D&ttid=142857@taobao_iphone_7.10.3'.format(
                nid)
            #url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1460616725586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%22{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(
             #           nid)
            retry += 1
            yield scrapy.Request(url, callback=self.parse_sell, meta={'nid': nid, 'retry': retry}, headers=header,
                                 dont_filter=True)

    
    
    
    
    
    
    
    
    