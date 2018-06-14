# -*- coding: utf-8 -*-
import scrapy
import json
import time
import datetime
import random
start_time = datetime.date.today()
oneday = datetime.timedelta(days=1)
start = start_time - oneday

ua =[   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
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
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
start_t = time.strftime("%Y-%m-%d %H:%M", time.localtime())


class Aso100IosSpider(scrapy.Spider):
    name = "aso100_ios"
    allowed_domains = []

    def __init__(self, *args, **kwargs):
        super(Aso100IosSpider, self).__init__(*args, **kwargs)
        self.url =  'https://old.qimai.cn/app/getDownloadFuture?appid={k}&appid={s}&sdate={start}&edate={stop}'
        start_urls = ['']

    def start_requests(self):
        ios_uid = ['570608623', '627781309', '766695512', '906632439', '952694580', '872341407', '453480684',
                   '620435874', '881766160', '1012877207', '714004498']
        name = [[u'腾讯体育', 273], [u'聚力体育', 8498], [u'懂球帝', 374], [u'虎扑体育', 512], [u'Keep', 209], [u'悦动圈', 264],
                [u'咕咚运动', 253], [u'乐动力', 303], [u'悦跑圈', 626], [u'咪咕善跑', 785], [u'黑鸟单车骑行软件', 9350]]
        for i in zip(name, ios_uid):
            url = self.url.format(k=i[1], s=i[1], start=start, stop=start_time)
            headers['User-Agent'] = headers['User-Agent'].format(random.choice(ua))
            yield scrapy.Request(url, meta={'name': i[0], 'url': url}, dont_filter=True,headers=headers)

    def parse(self, response):
        if response.status != 200:
            headers['User-Agent'] = headers['User-Agent'].format(random.choice(ua))
            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True,headers=headers)
        try:
            data = json.loads(response.body)
            item = {}
            if data['msg'] == u'成功':
                data = data.get('data')
                title = data.get('title')
                list = data.get('list')
                download = list[0]['data']
                for dow in download:
                    x = time.localtime(dow[0] / 1000)
                    date = time.strftime('%Y-%m-%d', x)
                    downloads = dow[1]
                    item['name'] = response.meta['name'][0]
                    item['Appid'] = response.meta['name'][1]
                    item['Aso_Name'] = title
                    item['Aso_Date'] = date
                    item['Aso_Downloads'] = downloads
                    item['task_time'] = start_t
                    # print item
                    yield item
        except:
            headers['User-Agent'] = headers['User-Agent'].format(random.choice(ua))
            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True,headers=headers)



    
    