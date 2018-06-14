# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy import Selector
import re
import random
from jd_comment.items import JdSkuItem
USER_AGENTS=[
    'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)',
    'Mozilla/5.0 (Linux; Android 6.0; MP1512 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.4 (Baidu; P1 6.0)',
    'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; X9007 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone 6s; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.6.0 Mobile/14E304 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Xplay6 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-A9000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 6.0.1)',
    'Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 6.0.1)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN',
    'Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11t Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043307 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN',
    'Mozilla/5.0 (iPhone 6s; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.5.1 Mobile/13G36 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 3X Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36'
]


class JdMallSpider(scrapy.Spider):
    name = 'jd_mall'
    allowed_domains = []
    start_urls = []

    def __init__(self,*args,**kwargs):
        super(JdMallSpider,self).__init__(*args,**kwargs)
        self.the_name_url = '''http://shop.m.jd.com/search/searchWareAjax.json?r={times}&shopId={shopid}&searchSort=0&jdDeliver=0&searchPage={page}'''
        self.particulars = '''https://item.jd.com/{}.html'''
    def start_requests(self):
        mall_dict = {
            #'滔搏户外旗舰店':'629970',
            '百丽集团官方旗舰店': '29668',
            '滔搏运动官方旗舰店': '607805',
            '百丽集团男鞋旗舰店': '22990',
            '优购运动旗舰店': '28289',
            '滔搏运动户外专营店': '85184'
                     }
        for i in mall_dict:
            the_name = i
            uid = mall_dict.get(i)
            url = self.the_name_url.format(times=int(time.time()),shopid=uid,page=1)
            yield scrapy.Request(url,dont_filter=True,meta={'the_name':the_name,'url':url,'uid':uid},headers={'User-Agent':random.choice(USER_AGENTS)})
        # url = 'https://item.jd.com/16923816798.html'
        # yield scrapy.Request(url,dont_filter=True,callback=self.get_detail_item,meta={'shop_name':'滔搏运动户外专营店','name':'adidas neo阿迪休闲2017年新款男子BP NEOPARK MIX系列双肩包CD9 藏青 F','sku':'16923816798'})


    def parse(self, response):
        shop_name = response.meta['the_name']
        html = json.loads(response.body)
        max_page = html['results']['totalPage']
        pages = html['results']['pageIdx']
        if int(pages) <= int(max_page):
            for i in html['results']['wareInfo']:
                name = i.get('wname')
                price = i.get('jdPrice')
                sku = i.get('wareId')
                url = self.particulars.format(sku)
                yield scrapy.Request(url,meta={'url':url,'name':name,'price':price,'sku':sku,'shop_name':shop_name},dont_filter=True,callback=self.get_detail_item)
            page_url = response.meta['url']
            page_url = page_url.split('searchPage=')
            page = int(page_url[1])+1
            uid = response.meta['uid']
            urls = self.the_name_url.format(times=int(time.time()),shopid=uid,page=page)

            yield scrapy.Request(urls,meta={'the_name':shop_name,'url':urls,'uid':uid},dont_filter=True,callback=self.parse,headers={'User-Agent':random.choice(USER_AGENTS)})

    def get_detail_item(self, response):
        html = response.body.decode('gb18030').encode('utf8')
        bd =''.join(Selector(text=html).xpath('//*[@id="parameter-brand"]/li/a/text()').extract())
        try:
            datas = re.search('colorSize: (?P<name>.+\])', response.body.decode('gbk')).groupdict()['name']
            datas = eval(datas)
            for data in datas:
                #item ={}
                item = JdSkuItem()
                item['sku'] = data['skuId']
                item['shop_name'] = response.meta['shop_name']
                item['brand'] = bd
                item['title'] = response.meta['name']
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                item['chicun'] = data['尺码']
                # item['price'] = response.meta['price']
                try:
                    item['yanse'] = data['颜色']
                except Exception as e:
                    item['yanse'] = ''
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                yield item

            pass
        except:
            url = response.url
            name = response.meta['name']
            sku = response.meta['sku']
            shop_name = response.meta['shop_name']
            yield scrapy.Request(url, meta={'url':url,'name':name,'sku':sku,'shop_name':shop_name},
                                 dont_filter=True, callback=self.brand)




    def brand(self,response): #详情页
        item = JdSkuItem()
        #item = {}
        html = response.body.decode('gb18030').encode('utf8')
        bd =''.join(Selector(text=html).xpath('//*[@id="parameter-brand"]/li/a/text()').extract())
        item['brand'] = bd
        item['title'] = response.meta.get('name')
        if item['title'] ==None:
            item['title'] = ''.join(re.findall('<title>(.*?)</title>',html))
        item['sku'] = response.meta['sku']
        # item['price'] = response.meta['price']
        item['shop_name'] = response.meta['shop_name']
        item['dt'] = time.strftime("%Y-%m-%d", time.localtime())
        yield item



    
    