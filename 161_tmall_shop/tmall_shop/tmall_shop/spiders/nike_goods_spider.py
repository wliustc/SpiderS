# -*- coding: utf-8 -*-
import scrapy
import web
import re
import time
import json
import sys
from tmall_shop.items import TmallShopGoodsItem
reload(sys)
sys.setdefaultencoding('utf-8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
_mapping = {
    'sellCount': re.compile(r'\\"sellCount\\":\\"(\d+)\\"'),
}


def get_regex_group1(key, _str, default=None):
    p = _mapping[key]
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
            tmp = get_json_hierarchy(tmp_json, ['price', 'price', 'priceText'])
            if tmp:
                if '-' in tmp:
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

def format_list(data):
    result = []
    if data:
        for item in data:
            tmp = ''
            if item:
                if type(item) == unicode:
                    tmp = item.encode('utf-8')
                    tmp = tmp.replace('\u0001', '')
                    tmp = tmp.replace('\n', ' ')
                    tmp = tmp.replace('\t', ' ')
                    tmp = tmp.replace('\r', ' ')
                    tmp = tmp.strip()
                elif type(item) == int:
                    tmp = str(item)
                elif type(item) == str:
                    tmp = item.encode('utf-8').replace("\u0001", '')
                    tmp = tmp.replace('\n', ' ')
                    tmp = tmp.replace('\t', ' ')
                    tmp = tmp.replace('\r', ' ')
                    tmp = tmp.decode('utf-8').strip()
                else:
                    tmp = item
            result.append(tmp)
    return result


def get_brand(content):
    brand_info_list = get_json_hierarchy(content, ['detail', 'eleParameterList'])
    for bd in brand_info_list:
        if bd.has_key(u'主体'):
            brand_name = bd[u'主体'][0]['snparameterVal']
            return brand_name
    return None


class Nike_Goods_Spider(scrapy.Spider):

    name = 'nike_goods_spider'
    handle_httpstatus_list = [420, 419]

    def start_requests(self):
        the_date = time.strftime('%Y-%m-%d', time.localtime())
        result_list = db.query("select nid from t_spider_tmallshop_goodsnid where dt='{}' and user_id='890482188'".format(the_date))
        for result in result_list:
            nid = result.nid
            url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1511754610802&sign=f08f99aef1ded9754c0b2c9ecc56bbe0&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22ft%5C%22%3A%5C%22t%5C%22%2C%5C%22spm%5C%22%3A%5C%22a230r.1.14.5.5b5666b5SBcaMm%5C%22%2C%5C%22id%5C%22%3A%5C%22{}%5C%22%7D%22%2C%22itemNumId%22%3A%22{}%22%7D'.format(
                nid, nid)
            yield scrapy.Request(url, dont_filter=True, callback=self.detail_parse, meta={'nid': nid})

    def detail_parse(self, response):
        nid = response.meta['nid']
        if 'FAIL_SYS_USER_VALIDATE' in response.body:
            url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1511754610802&sign=f08f99aef1ded9754c0b2c9ecc56bbe0&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22ft%5C%22%3A%5C%22t%5C%22%2C%5C%22spm%5C%22%3A%5C%22a230r.1.14.5.5b5666b5SBcaMm%5C%22%2C%5C%22id%5C%22%3A%5C%22{}%5C%22%7D%22%2C%22itemNumId%22%3A%22{}%22%7D'.format(
                nid, nid)
            yield scrapy.Request(url, dont_filter=True, callback=self.detail_parse, meta={'nid': nid})
        else:
            content = re.findall('mtopjsonp1\(([\s\S]*?}})\)', response.body)[0]
            content = json.loads(content)
            apiStack = parse_apiStack(get_json_hierarchy(content, ['data', 'apiStack']))
            # title
            title = get_json_hierarchy(content, ['data', 'item', 'title'])
            # view_price
            view_price = get_json_hierarchy(apiStack, ['view_price'])
            # month_sale
            month_sale = get_regex_group1('sellCount', json.dumps(content))
            extra_info = ''
            props_json = get_json_hierarchy(content, ['data', 'props', 'groupProps'])
            if props_json:
                for i in props_json:
                    if u'基本信息' in i:
                        extra_info = i[u'基本信息']
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
            kuanhao = ''
            for i in extra_info:
                if i.get(u'款号'):
                    kuanhao = i.get(u'款号')
                    break
            # 货号
            huohao = ''
            for i in extra_info:
                if i.get(u'货号'):
                    huohao = i.get(u'货号')
                    break
            # 吊牌价
        	tag_price = ''
            for i in extra_info:
                if i.get(u'吊牌价'):
                    tag_price = i.get(u'吊牌价')
                    break
            url = 'https://detail.tmall.com/item.htm?id={}'.format(nid)
            shop_name = 'NIKE官方旗舰店'
            items = TmallShopGoodsItem()
            items['url'] = url
            items['title'] = title
            items['nid'] = nid
            items['shop_name'] = shop_name
            items['price'] = view_price
            items['month_sale'] = month_sale
            items['kuanhao'] = kuanhao
            items['huohao'] = huohao
            items['time_to_market'] = time_to_market
            items['tag_price'] = tag_price
            items['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            yield items

    
    
    