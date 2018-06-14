# -*- coding: utf-8 -*-
import scrapy
import web
import random
from scrapy.selector import Selector
db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
def ua():
    user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    Ua = random.choice(user_agent_list)
    headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Connection': 'keep-alive',
        'User-Agent':Ua
    }
    return headers

class HomeSpider(scrapy.Spider):
    name = "home"
    allowed_domains = ["meituan.com"]
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(HomeSpider,self).__init__(*args,**kwargs)

    def start_requests(self):
        sql = '''select city_name,name,province,href from meituan  '''
        for i in db.query(sql):
            city_name = i.get('city_name')
            province = i.get('province')
            href = i.get('href')
            name = i.get('name')
            yield scrapy.Request(href,meta={'url':href,'province':province,'city_name':city_name,'name':name,'ua':ua()},headers=ua(),dont_filter=True)

    def parse(self, response):
        html = response.body
        if response.status != 200:

            yield scrapy.Request(response.meta['url'], headers=response.meta['ua'],callback=self.parse, meta=response.meta, dont_filter=True)
        if  len(''.join(Selector(text=html).xpath('//*[@class="info"]/div/span[@class="biz-level"]/strong/text()').extract())) == 0:
            yield scrapy.Request(response.meta['url'], headers=response.meta['ua'], callback=self.parse,
                                 meta=response.meta, dont_filter=True)
        else:
            score = ''.join(Selector(text=html).xpath('//*[@class="info"]/div/span[@class="biz-level"]/strong/text()').extract())
            count = ''.join(Selector(text=html).xpath('//*[@class="counts"]/div/a/text()').extract())
            addr = ''.join(Selector(text=html).xpath('//*[@class="under-title"]/span/text()').extract())
            tel = ''.join(Selector(text=html).xpath('//*[@class="fs-section__left"]/p[2]/text()').extract())
            county = ''.join(Selector(text=html).xpath('//*[@class="bread-nav"]/a[4]/text()').extract())
            trading_area = ''.join(Selector(text=html).xpath('//*[@class="bread-nav"]/a[5]/text()').extract())
            item = {}
            item['score'] = score
            item['count'] = count
            item['addr'] = addr
            item['tel'] = tel
            item['county'] = county
            item['trading_area'] = trading_area
            item['province'] = response.meta['province']
            item['city_name'] = response.meta['city_name']
            item['url'] = response.meta['url']
            item['name'] = response.meta['name']
            yield item