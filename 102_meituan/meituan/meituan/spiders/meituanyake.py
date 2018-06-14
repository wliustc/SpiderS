# -*- coding: utf-8 -*-
import scrapy
import sys
import chaifen
import re
import requests
import web
from scrapy.selector import Selector
import random
reload(sys)
sys.setdefaultencoding('utf8')
import time
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
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
    return Ua
headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'User-Agent':ua(),
        }
def test(n,n1,host,origin,url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': host,
        'Origin': origin,
        'Referer':url,
        'User-Agent': ua(),
        'X-Requested-With': 'XMLHttpRequest'}
    data = {
        'poiidList':n,
        'bigImageMode':'true',
        'poiData':n1,
    }
    return headers,data

class MeituanyakeSpider(scrapy.Spider):
    name = "meituanyake"
    allowed_domains = ['meituan.com']
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(MeituanyakeSpider, self).__init__(*args, **kwargs)
        self.meituan = 'http://{}.meituan.com'
        self.Host = '{}.meituan.com'
        self.post_url = 'http://{}.meituan.com/index/poilist'
        self.get_url = 'http://{}.meituan.com/category/tijian?mtt=1.index%2Ffloornew.nc.122.j3wg54ee'
        self.pag_url = 'http://{}.meituan.com/category/tijian/all/page{}?mtt=1.index%2Fdefault%2Fpoi.0.0.j3zau5hh'
    def start_requests(self):
        sql = '''select city_name,city_jc,province_name from t_spider_meituan_business_area  '''
        for i in db.query(sql):
            city_name = i.get('city_name')
            city_jc = i.get('city_jc')
            province = i.get('province_name')
            url = self.get_url.format(city_jc)
            yield scrapy.Request(url,meta={'url':url,'city_name':city_name,'city_jc':city_jc,'province':province},dont_filter=True)
    def parse(self, response):
        html = response.body
        pag =Selector(text=html).xpath('//*[@id="content"]/div[2]/ul/li/a/text()').extract()
        if len(pag) < 1:
            yield scrapy.Request(response.meta['url'],meta=response.meta,dont_filter=True,callback=self.parse1)
        else:
            city_name = response.meta['city_name']
            city_jc = response.meta['city_jc']
            province = response.meta['province']
            for i in pag[0:-1]:
                url = self.pag_url.format(city_jc,i)
                yield scrapy.Request(url,meta={'url': url, 'city_name': city_name, 'city_jc': city_jc, 'province': province},callback=self.parse1)

    def parse1(self, response):
        if response.status != 200 and response.status != 503:
            yield scrapy.Request(response.meta['url'],callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            html = response.body
            city_url = response.meta.get('url')
            city_name = response.meta.get('city_name')
            city_jc = response.meta.get('city_jc')
            province = response.meta.get('province')
            host = self.Host.format(city_jc)
            origin = self.meituan.format(city_jc)
            data_list = Selector(text=html).xpath('//*[@data-component="poi-list"]/div/div/@data-async-params').extract()[0]
            datas = re.sub(r'\\', '', data_list)
            id_s = re.findall('poiidList":(.*?),"poiData"', datas)
            if len(id_s[0]) > 2:
                id_s=id_s[0][1:-1].split(',')
                data_lists = []
                from_data = re.findall('"poiData":(.*?),"limit":', datas)[0][1:-1].split(r'},')
                for i in from_data:
                    data_lists.append(i + '},')
                fu = data_lists[-1][0:-1]
                data_lists.remove(data_lists[-1])
                data_lists.append(fu)
                if len(id_s) > 10:
                    ci = len(id_s) / 10
                    ci += 2
                else:
                    ci =1
                for i in zip(chaifen.div_list(id_s, ci), chaifen.div_list(data_lists, ci)):
                    fu = i[1][-1][0:-1]
                    i[1].remove(i[1][-1])
                    i[1].append(fu)
                    a = "[" + ','.join(i[0]) + "]"
                    a1 = "[" + ''.join(i[1]) + "]"
                    headers,data = test(a,a1,host,origin,city_url)
                    url = self.post_url.format(city_jc)
                    html = requests.post(url,data=data,headers=headers)
                    while True:
                        if html.status_code == 200:
                            yield self.parse2(html.text,city_name,province)
                            break
                        else:
                            html = requests.post(url, data=data, headers=headers)
            else:
                print '1111'

    def parse2(self,html,city_name,province):
        itme ={}
        htmls = html.replace('\/','/')
        import json
        now = json.loads(htmls)
        htm = re.sub(u'\xa5','',now['data'])
        href = Selector(text=htm).xpath('//*[@class="poi-tile__info"]/div[@class="basic cf"]/a/@href').extract()
        name = Selector(text=htm).xpath('//*[@class="poi-tile__info"]/div[@class="basic cf"]/a/text()').extract()
        ratio = Selector(text=htm).xpath('//*[@class="rate"]/span[1]/span/@style').extract()
        comments = Selector(text=htm).xpath('//*[@class="rate"]/a/span[@class="num"]/text()').extract()
        for i in zip(name,href,ratio,comments):
            if re.findall(u'口腔|牙|齿',i[0]):
                itme['name'] = i[0]
                itme['province'] = province
                itme['city_name'] = city_name
                itme['href'] = i[1]
                itme['ratio'] = i[2].split(':')[1]
                itme['comments'] = i[3]
                # yield scrapy.Request(i[1],meta={'url':i[1],'province':province,'city_name':city_name,'name':name},dont_filter=True,callback=self.parse2)
                try:
                    db.insert('t_xsd_meituan_dental', **itme)
                except Exception as e:
                    print e
            else:
                itme['name'] = i[0]
                itme['province'] = province
                itme['city_name'] = city_name
                itme['href'] = i[1]
                itme['ratio'] = i[2].split(':')[1]
                itme['comments'] = i[3]
                try:
                    db.insert('meituan_tijian_tj', **itme)
                except Exception as e:
                    print e
    
    
    
    
    