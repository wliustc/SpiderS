# -*- coding: utf-8 -*-
import scrapy
import web
import json
import re
import time
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class HomeTaobaoSpider(scrapy.Spider):
    name = 'home_taobao_test'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(HomeTaobaoSpider,self).__init__(*args,**kwargs)
        self.home_test = '''https://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t={times}&sign=04b5eb36c2ccfebe0d39dab46de5ec18&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=&data=%7B"itemNumId"%3A"{uid}"%2C"exParams"%3A"%7B%5C"id%5C"%3A%5C"8548526%5C"%2C%5C"wp_app%5C"%3A%5C"weapp%5C"%7D"%7D'''
        self.home_api = '''https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t={times}&sign=f08f99aef1ded9754c0b2c9ecc56bbe0&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B"exParams"%3A"%7B%5C"ft%5C"%3A%5C"t%5C"%2C%5C"spm%5C"%3A%5C"a230r.1.14.5.5b5666b5SBcaMm%5C"%2C%5C"id%5C"%3A%5C"{uid}%5C"%7D"%2C"itemNumId"%3A"{uid_}"%7D'''
        self.home = '''https://item.taobao.com/item.htm?ft=t&id={}'''
    def start_requests(self):
        sql = '''SELECT * FROM `t_spider_xianhua_id` WHERE sag='天猫'  '''
        # sql = '''select * from t_spider_xianhua_id WHERE uid='561318088484' '''
        for i in db.query(sql):
            uid = i.get('uid')
            key_word = i.get('key_word')
            url = self.home.format(uid)
            yield scrapy.Request(url,meta={'uid':uid,'key_word':key_word,'url':url},dont_filter=True)
        # url = self.home.format('55681668469')
        # uid = '55681668469'
        # key_word = '多'
        # yield scrapy.Request(url,meta={'uid':uid,'key_word':key_word,'url':url},dont_filter=True)


    def parse(self, response):
        try:
            html = response.body.decode('gbk')
        except:
            html = response.body
        if re.findall(u'很抱歉，您查看的宝贝不存在，可能已下架或者被转移|很抱歉，您查看的商品找不到了',html):
            print '#######################################'
        elif re.findall('<title>(.*?)</title>',html,re.S):
            uid = response.meta['uid']
            # url = self.home_api.format(uid=uid,uid_=uid,times=str(int(round(time.time() * 1000))))
            url = self.home_test.format(uid=uid,times=str(int(round(time.time() * 1000))))
            response.meta['url'] = url
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse_home)
        else:
            url = response.meta['url']
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse)

    def parse_home(self, response):
        item = {}
        html = response.body
        item['uid'] = response.meta['uid']
        item['key_word'] = response.meta['key_word']
        # html = html.replace('mtopjsonp1(', '')[:-1]

        try:
            item['price_all'] = json.loads(json.loads(html)['data']['apiStack'][0]['value'])['skuCore']['sku2info']['0']['price'][
                'priceText']
            data = json.loads(html)['data']['item']
            title = data['title']
            item['commentCount'] = data['commentCount']
            body_ = html
            html = html.replace('\\', '')
            item['sellCount'] = ''.join(re.findall('sellCount":"(.*?)",', html, re.S))
            item['brand'] = ''.join(re.findall(r'{"品牌":"(.*?)"},', html, re.S))
            dingyu = ''.join(re.findall(u'订阅|包月', title))
            merchandise_type =  ''.join(re.findall(u'送礼|礼品|礼物', title))
            if len(dingyu):
                item['dingyu']=u'订阅'
            if len(merchandise_type):
                item['merchandise_type']=u'礼品花'
            else:
                item['merchandise_type']=u'日常花'
            item['title'] = title
            if len(item['sellCount'])==0:
                item['sellCount'] = 0
            uid_data = json.loads(json.loads(body_)['data']['apiStack'][0]['value'])['skuCore']['sku2info']
            skus = json.loads(body_).get('data').get('skuBase').get('skus')
            data_dict = {}
            try:
                if skus:
                    del uid_data['0']
                    skus_values = json.loads(body_).get('data').get('skuBase').get('props')[0]['values']
                    for i in uid_data:
                        price = uid_data.get(i).get('price').get('priceText')
                        for sku in skus:
                            skuid = sku.get('skuId')
                            if skuid == i:
                                sku_id = sku.get('propPath').split(';')[0].split(':')[1]
                                data_dict[skuid] = price
                                for values in skus_values:
                                    vid = values.get('vid')
                                    if sku_id == vid:
                                        names = values.get('name')
                                        data_dict[skuid] = names + ',' + price
                elif len(uid_data) == 1:
                    data_dict['0'] = uid_data.get('0').get('price').get('priceText')
                    item['sellCount'] = ''.join(re.findall('sellCount":"(.*?)"},', html, re.S))
            except:
                del uid_data['0']
                for i in uid_data:
                    data_dict[i] = uid_data.get(i).get('price').get('priceText')

            if data_dict:
                for i in data_dict:
                    item['sku'] = i
                    std = data_dict.get(i).split(',')
                    if len(std) >1:
                        item['names'] = std[0]
                        item['price'] = std[1]
                    else:
                        item['price'] = std[0]
                    item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    yield item
        except:
            print response.body,'#'*100
            uid = response.meta['uid']
            times = str(int(round(time.time() * 1000)))
            url = self.home_test.format(uid=uid,times=times)
            yield scrapy.Request(url, meta=response.meta, dont_filter=True,callback=self.parse_home)




    
    
    
    
    
    