# -*- coding: utf-8 -*-
import scrapy
import random
import sys
from scrapy.http.request import Request
import re

import json
reload(sys)
sys.setdefaultencoding('utf-8')
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'User-Agent,Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'User-Agent,Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent,Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
]

class StaccatoSpider(scrapy.Spider):
    name = 'staccato'
    # allowed_domains = ['https://module-jshop.jd.com/module/allGoods/goods.html?sortType=0&appId=664492&pageInstanceId=64797879&searchWord=&pageNo=1&direction=1&instanceId=100203718&modulePrototypeId=55555&moduleTemplateId=905542&refer=https%3A%2F%2Fmall.jd.com%2Fview_search-664492-0-99-1-24-1.html']
    # start_urls = ['http://https://module-jshop.jd.com/module/allGoods/goods.html?sortType=0&appId=664492&pageInstanceId=64797879&searchWord=&pageNo=1&direction=1&instanceId=100203718&modulePrototypeId=55555&moduleTemplateId=905542&refer=https%3A%2F%2Fmall.jd.com%2Fview_search-664492-0-99-1-24-1.html/']
    def start_requests(self):
        url = 'https://module-jshop.jd.com/module/allGoods/goods.html?appId=664492&pageInstanceId=64797879&searchWord=&pageNo=1&instanceId=100203718&modulePrototypeId=55555&moduleTemplateId=905542'
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        yield Request(url, headers=headers, dont_filter=True)

    def parse(self, response):
        count = response.xpath('//div[@id="J_topPage"]/span/i/text()').extract()
        if count:
            count = count[0]
            count = int(count) + 1
            for i in xrange(1, count):
                url = 'https://module-jshop.jd.com/module/allGoods/goods.html?appId=664492&pageInstanceId=64797879&searchWord=&pageNo='+ str(i) +'&instanceId=100203718&modulePrototypeId=55555&moduleTemplateId=905542'
                headers = {
                    'User-Agent': random.choice(USER_AGENTS)
                }
                yield scrapy.Request(url, headers=headers, callback=self.parse_content,dont_filter=True)

    def parse_content(self, response):
        url_list = response.xpath('//div[@class="gl-i-wrap"]/div[@class="jPic"]/a/@href').extract()
        for base_url in url_list:
            base_url = 'https:' + base_url
            headers = {
                'User-Agent': random.choice(USER_AGENTS)
            }
            yield scrapy.Request(base_url, headers=headers, meta={'base_url': base_url}, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        product_code = ''
        dianpu_name = ''
        shop_name = ''
        # li = response.xpath('//div[@class="p-parameter"]/ul[2]').extract()
        # li = ''.join(li)
        html = response.body.decode('gbk')
        code = re.search(u'<li.*>货号：(.*?)</li>', html)
        # code = re.search(u"<li.*='(\d.*)>货号'",li)
        if code:
            product_code = code.group(1)
        dianpu = re.search(u'<li.*>店铺：.<a.*?>(.*?)</a>', html)
        if dianpu:
            dianpu_name = dianpu.group(1)
        shop = re.search(u'<li.*>商品名称：(.*)</li>', html)
        if shop:
            shop_name = shop.group(1)

        base_url = response.meta.get('base_url')
        id = re.search(r'\d+', base_url)
        if id:
            shop_id = id.group()
            # 24149008437   24149008437
            url = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(shop_id)
            headers = {
                'User-Agent': random.choice(USER_AGENTS)
            }
            meta_info = {'id': shop_id, 'base_url': base_url, 'product_code': product_code, 'dianpu_name': dianpu_name,'shop_name': shop_name}
            yield scrapy.Request(url, headers=headers, meta=meta_info, callback=self.parse_all, dont_filter=True)

    def parse_all(self, response):
        item = {}
        html = response.body
#        html = html.encode('utf-8')
#         prices = re.search(r'\"p\":"(.*?)\"', html)
        json_obj = json.loads(html)
        if json_obj:
            json_obj = json_obj[0]
            if json_obj:
                prices = json_obj.get('p')
                if prices:
                    item["price"] = prices
        else:
            prices = re.search(r'\"p\":"(.*?)\"', html)
            if prices:
                item["price"] = prices.group(1)
        meta_info = response.meta
        item["shop_id"] = meta_info.get('id')
        item['base_url'] = meta_info.get('base_url')
        item['product_code'] = meta_info.get('product_code')
        item['dianpu_name'] = meta_info.get('dianpu_name')
        item['shop_name'] = meta_info.get('shop_name')
        yield item





