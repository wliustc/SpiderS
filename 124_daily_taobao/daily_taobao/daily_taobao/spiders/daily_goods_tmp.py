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
cookie = {
    'miid': '1570984631903286176',
    'ctoken': 'dWNk0of7ZzhB1BfVXVvRiceland',
    'thw': 'cn',
    'cookie2': '1ccd63be9facd40ecfea4e09fdd941b8',
    '_cc_': 'UIHiLt3xSw%3D%3D',
    'tg': '0',
    '_tb_token_': 'eeb5abb51e6b0',
    'cna': 'tTCaEWglogQCAd6Ab3yqeklX',
    'x': '98563612',
    'v': '0',
    '_umdata': 'C234BF9D3AFA6FE7FFD3068277C629DA5A243406223B6B0192ECE0E9916B85C728888725A66321FCCD43AD3E795C914C85EEA646E2EEBD4F453702DE0F3FE179',
    'l': 'Ak9PkymhSqgp5xc6UYwBIv4oX-hZdKOW',
    'linezing_session': 'wjsNUKZKZdWmp7DF39AZfzfv_1514962119549bqVT_25',
    'hng': 'CN%7Czh-CN%7CCNY%7C156',
    't': '5a33d90554f958d6150036e16c6844bd',
    'x-nq': 'UNKNOWN',
    '_m_h5_tk': 'ea38b2c5fb82f78c5abb4daf311cff8d_1517847927493',
    '_m_h5_tk_enc': 'c403df3c77a94695c5563d292a305eb1',
    'uc1': 'cookie14',
    'uc3': 'nk2',
    'existShop': 'MTUxNzkwOTI1OA%3D%3D',
    'lgc': '%5Cu6293%5Cu7D27%5Cu65F6%5Cu95F4%5Cu54271992',
    'tracknick': '%5Cu6293%5Cu7D27%5Cu65F6%5Cu95F4%5Cu54271992',
    'dnk': '%E6%8A%93%E7%B4%A7%E6%97%B6%E9%97%B4%E5%90%A71992',
    'sg': '268',
    'csg': 'a135a61e',
    'mt': 'np',
    'cookie1': 'UtJVkanQDJ2OwF7STEAdisKn0GYTfgNTMCnkayxD5kY%3D',
    'unb': '1816169106',
    'skt': 'ed024a718fc3772c',
    '_l_g_': 'Ug%3D%3D',
    '_nk_': '%5Cu6293%5Cu7D27%5Cu65F6%5Cu95F4%5Cu54271992',
    'cookie17': 'UonaU4OypgAakw%3D%3D',
    'isg': 'BAEBfNDaPyl6WVNUKnZR7R_4EEsRPXQsJSDTnmNWy4hnSiAcq34z8IcKKL4Mwg1Y',
    'tk_trace': 'oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1ohKaWxIq7DIAQSQQ7pxp%2BLLbdwAodzuYRr6EnJGk%2BAbPzMMhr1Pd6qDWRICboTDr7OU81yIK21ud7wnqV9%2BCRHe3xnyICv9qgJKrZreiWO5W50xlc%2F5Ocvm93c%2BwfPXNAvZNLD48KVmiFZYK6BsZlBLuxh66psGrAjtx1lLMnHenpmw0G2JOn3nI6ffAaibpvvAOFktLVfJvAVAP7KPjOfRUi',
    'enc': '5AKM9p6cP7isfHGIacN9PiPYC3r3cW1PhLUMqs1TlgncpuexRB4j2Rf7WexIK0D0mMY5RgMfpYLBupiO3YVEYA%3D%3D'
}
the_time = time.strftime('%Y-%m-%d', time.localtime())
#the_time = '2018-05-23'

class Daily_Goods_Tmp_Spider(scrapy.Spider):

    name = 'daily_goods_tmp_spider'
    handle_httpstatus_list = [420,419]
    #custom_settings = {
     #   'DOWNLOADER_MIDDLEWARES': {'daily_taobao.middlewares_mine.ProxyMiddleware': 100,
      #                             'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110}
    #}

    def start_requests(self):
        with pyhs2.connect(host='10.15.1.16', port=10000, authMechanism="PLAIN", user='zyliu', password='zyliu',
                           database='ods') as conn:
            with conn.cursor() as cur:
                the_day = time.strftime('%Y-%m-%d', time.localtime())
                #the_day = '2018-05-23'
                cur.execute(
                    "select goods_id from ods.daily_goodsList where (dt='2017-12-04' or dt='2017-12-03' or "
                    "dt='2017-12-02' or dt='2018-01-04' or dt='2017-11-08' or dt='2018-01-19' or dt='{}') and user_id in (446338500,890482188,"
                    "133227658,1993730769,772352677,167873659, 98563612, 353042333, 1731961317, 353042353, 829273025, "
                    "2940972233, 2940677727, 435878238, 281917995, 737997431, 458599810, 1739810699, 1574853209, "
                    "1893742894, 1122478447, 373327370, 2647118809, 2786693231, 2434852658, 3000560259, 1916102784, "
                    "656650799, 2074964291, 708668355, 720472756, 356579667, 1731961317,98563612,1689954831,387266832"
                    ",2073309259,325718097,1891339807,834807033,1974964452,372602234,167486422,356374102,"
                    "320083279,411832242,1602582004,2428721558,1574853209,2986712394,2183615086,2424477833,"
                    "1754310760,1754310760,1122478447,3000560259,2652614726,533230328,2935707588,2945786195,"
                    "2074690906,3458347554,3383168585,2366121327,3099864367,106852162,152579056,1754310760,783329018,1600687454,205919815,113484749,94092459,6655,2978259752) group by goods_id".format(str(the_day)))
                #cur.execute("select nid_a FROM (SELECT a.nid_a, b.nid_b FROM (SELECT nid AS nid_a FROM ods.daily_taobao_item_info WHERE dt='2018-04-15') a LEFT JOIN (SELECT nid AS nid_b FROM ods.daily_taobao_item_info WHERE dt='2018-04-17') b ON a.nid_a=b.nid_b) c WHERE nid_b is null")
                for i in cur.fetch():
                    nid = i[0]
                    retry = 0
                    # header = {'referer': 'https://detail.tmall.com/item.htm?spm=a230r.1.14.105.60fe4959AXOfeT&id={}&ns=1&abbucket=1'.format(nid)}
                    # url = 'https://mdskip.taobao.com/core/initItemDetail.htm?household=false&offlineShop=false&isRegionLevel=false&sellerPreview=false&showShopProm=false&service3C=false&cachedTimestamp=1517879469587&isPurchaseMallPage=false&queryMemberRight=true&isForbidBuyItem=false&isAreaSell=false&isApparel=true&itemId={}&addressLevel=2&tmallBuySupport=true&cartEnable=true&tryBeforeBuy=false&isUseInventoryCenter=false&isSecKill=false&callback=setMdskip&timestamp={}&isg=null&isg2=Anp6keT59IynnXv69HRyHxXLy6aWOP8Jyi24A4RzkI3vdxqxbLtOFUDHszVQ'.format(nid, str(time.time()*1000))
                    # url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1511754610802&sign=f08f99aef1ded9754c0b2c9ecc56bbe0&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22ft%5C%22%3A%5C%22t%5C%22%2C%5C%22spm%5C%22%3A%5C%22a230r.1.14.5.5b5666b5SBcaMm%5C%22%2C%5C%22id%5C%22%3A%5C%22{}%5C%22%7D%22%2C%22itemNumId%22%3A%22{}%22%7D'.format(nid, nid)
                    # url = 'http://hws.m.taobao.com/cache/wdetail/5.0/?id={}'.format(nid)
                    url = 'https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{}%22%2C%22detail_v%22%3A%223.1.0%22%7D&ttid=142857@taobao_iphone_7.10.3'.format(nid)
                    #url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1460616725586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%22{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(nid)
                    # print url
                    yield scrapy.Request(url, callback=self.parse_sell, meta={'nid': nid, 'retry': retry},headers=header,
                                         dont_filter=True)

    def parse_sell(self, response):
        items = GoodsTmpItem()
        nid = response.meta['nid']
        retry = response.meta['retry']
        content = response.body
        pattern = re.search('"sellCount\\\\":\\\\"(.*?)\\\\"', content)
        # pattern = re.search(u'月销(.*?)笔', content)
        if pattern and retry < 100:
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
            items['dt'] = the_time
            yield items
        elif 'SUCCESS' in content and not pattern:
            pass
        elif retry > 100:
            pass
        else:
            # header = {
            #     'referer': 'https://detail.tmall.com/item.htm?spm=a230r.1.14.105.60fe4959AXOfeT&id={}&ns=1&abbucket=1'.format(
            #         nid)}
            # url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1511754610802&sign=f08f99aef1ded9754c0b2c9ecc56bbe0&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22ft%5C%22%3A%5C%22t%5C%22%2C%5C%22spm%5C%22%3A%5C%22a230r.1.14.5.5b5666b5SBcaMm%5C%22%2C%5C%22id%5C%22%3A%5C%22{}%5C%22%7D%22%2C%22itemNumId%22%3A%22{}%22%7D'.format(nid, nid)
            # url = 'http://hws.m.taobao.com/cache/wdetail/5.0/?id={}'.format(nid)
            url = 'https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{}%22%2C%22detail_v%22%3A%223.1.0%22%7D&ttid=142857@taobao_iphone_7.10.3'.format(
                 nid)
            #url = 'https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1460616725586&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B%22itemNumId%22%3A%22{}%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%228548526%5C%22%2C%5C%22wp_app%5C%22%3A%5C%22weapp%5C%22%7D%22%7D'.format(
             #   nid)
            # print url
            retry += 1
            yield scrapy.Request(url, callback=self.parse_sell, meta={'nid': nid, 'retry': retry},headers=header,
                                 dont_filter=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    