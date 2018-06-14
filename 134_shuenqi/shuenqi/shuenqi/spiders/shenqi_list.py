# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import random
import web
import re
from ..items import ShuenqiItem
#from ..items import ElongItem
USER_AGENTS=[
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host':'www.11467.com',
    'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    'Upgrade-Insecure-Requests':'1'
}

# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



class ShenqiSpider(scrapy.Spider):
    name = 'shuen_list'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(ShenqiSpider,self).__init__(*args,**kwargs)
    def start_requests(self):
        #sql = '''select min_type_href,province,type_name,min_type from t_spider_qishuen WHERE min_type_href='http://www.11467.com/nanjing/dir/h65.htm' '''
        sql = '''select min_type_href,province,type_name,min_type from t_spider_qishuen WHERE  province='直辖市' '''
        # sql = '''SELECT * FROM `t_spider_qishuen` WHERE type_name LIKE '%南京%' OR type_name like '%杭州%' OR type_name LIKE '%济南%' OR type_name LIKE '%武汉%' OR type_name LIKE '%深圳%' OR province='直辖市' '''
        # sql = '''select min_type_href,province,type_name,min_type from t_spider_qishuen  '''
        for i in db.query(sql):
            url = i.get('min_type_href')
            province = i.get('province')
            type_name = i.get('type_name')
            min_type = i.get('min_type')
            headers['User-Agent'] = headers['User-Agent'].format(random.choice(USER_AGENTS))
            i['min_type_href'] = url
            yield scrapy.Request(url,meta={
                'min_type_href':url,
                'province':province,
                'type_name':type_name,
                'min_type':min_type},dont_filter=True,headers=headers)#
    def parse(self, response):
        html = response.body
        min_type_href = response.meta['min_type_href']
        province = response.meta['province']
        type_name = response.meta['type_name']
        min_type = response.meta['min_type']
        title = Selector(text=html).xpath('//*[@class="f_l"]/h4/a/text()').extract()
        if len(title) ==0:
           if '可能您访问的有点快了' in response.body:
                url = response.meta['min_type_href']
                yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse)
        elif len(title):
            t_d = 1
            for i in title:
                sp_href = '''//*[@id="il"]/div/div//li[{}]//a[@class="shop"]/@href'''.format(str(t_d))
                href_xp = '''//*[@id="il"]/div/div/ul/li[{}]//h4/a/@href'''.format(str(t_d))
                city = ''.join(Selector(text=html).xpath('//*[@class="navleft"]/a[3]/text()').extract()).replace('黄页','')
                href = ''.join(Selector(text=html).xpath(sp_href).extract())
                if len(href):
                    url = 'http:'+''.join(Selector(text=html).xpath(href_xp).extract())
                    sp_url = href
                    name = i
                    headers['User-Agent'] = headers['User-Agent'].format(random.choice(USER_AGENTS))
                    yield scrapy.Request(url=href,meta={'min_type_href':min_type_href,
                                                        'province':province,
                                                        'type_name':type_name,
                                                        'min_type':min_type,
                                                        'url':url,
                                                        'city':city,
                                                        'sp_url':sp_url,
                                                        'name':name},dont_filter=True,callback=self.parse_sp,headers=headers)
                else:
                    href = 'http:'+''.join(Selector(text=html).xpath(href_xp).extract())
                    url = href
                    name = i
                    headers['User-Agent'] = headers['User-Agent'].format(random.choice(USER_AGENTS))
                    yield scrapy.Request(url=href,meta={'data':{'min_type_href':min_type_href,
                                                        'province':province,
                                                        'city':city,
                                                        'type_name':type_name,
                                                        'min_type':min_type,
                                                        'url':url,
                                                        'name':name}},dont_filter=True,callback=self.parse_home,headers=headers)
                t_d+=1
            if '-p' in min_type_href:
                url_split = min_type_href.split('-p')
                page_ = int(url_split[1].replace('.htm',''))+1
                url = url_split[0]+'-p'+str(page_)+'.htm'
                min_type_href = url

            elif  '-' in min_type_href:
                url_split = min_type_href.split('-')
                page_ = int(url_split[1].replace('.htm', '')) + 1
                url = url_split[0] + '-' + str(page_) + '.htm'
                min_type_href = url
            else:
                # page = Selector(text=html).xpath('//*[@class="pages"]/span/text()').extract()
                page = Selector(text=html).xpath('//*[@id="il"]/div/a/@href').extract()
                if len(page):
                    url = 'https:'+page[1]
                    min_type_href = url
            headers['User-Agent'] = headers['User-Agent'].format(random.choice(USER_AGENTS))
            yield scrapy.Request(min_type_href, meta={'min_type_href': min_type_href,
                                            'province': province,
                                            'type_name': type_name,
                                            'min_type': min_type}, dont_filter=True, callback=self.parse,headers=headers)#
        else:
            print response.url,'###@'

    def parse_sp(self, response):
        item = {}
        html = response.body
        data = response.meta
        item['url'] = data['url']
        item['name'] = data['name']
        item['sp_url'] = data['sp_url']
        item['min_type_href'] = data['min_type_href']
        item['province'] = data['province']
        item['city'] = data['city']
        item['type_name'] = data['type_name']
        item['min_type'] = data['min_type']
        item['addr'] = ''.join(re.findall('<li>公司地址：(.*?)</li>', html))
        item['tel'] = ''.join(re.findall('<li>固定电话：(.*?)</li>', html))
        item['contact'] = ''.join(re.findall('<li>经理：(.*?)</li>', html))
        item['cellphone'] = ''.join(re.findall('<li>联系人移动电话：(.*?)</li>', html))
        item['mail'] = ''.join(re.findall('<li>电子邮件：(.*?)</li>', html))
        item['facsimile'] = ''.join(re.findall('<li>传真号码：(.*?)</li>', html))
        item['license'] = ''.join(re.findall('营业执照号码：</dt><dd>(.*?)</dd>', html))
        item['legal_person'] = ''.join(re.findall('法人代表：</dt><dd>(.*?)</dd>', html))
        item['operate'] = ''.join(re.findall('<dt>经营模式：</dt><dd>(.*?)</dd>', html))
        item['founding_time'] = ''.join(re.findall('成立时间：</dt><dd>(.*?) </dd>', html))
        item['capital'] = ''.join(re.findall('注册资本：</dt><dd>(.*?) 人民币 ', html))
        url = item['url']
        headers['User-Agent'] = headers['User-Agent'].format(random.choice(USER_AGENTS))
        yield scrapy.Request(url=url,meta={'data':item},dont_filter=True,callback=self.parse_home,headers=headers)#

    def parse_home(self,response):
        html = response.body
        #item = ElongItem()
        item = ShuenqiItem()
        # item = response.meta['data']
        addr_re = re.compile('<dl class="codl"><dt>.*?</dt><dd>(.*?)</dd>')
        addr = re.findall(addr_re, html)
        if len(addr) >1:
            item['addr'] = addr[0]
        else:
            item['addr']=''.join(''.join(addr))
        item['tel'] = ''.join(re.findall('固定电话：</dt><dd>(.*?)</dd>', html)).replace(' ','')
        contact_re = re.compile('经理：</dt><dd>(.*?)</dd>|老板：</dt><dd>(.*?)</dd>|联系人：</dt><dd>(.*?)</dd>')
        contact = re.findall(contact_re, html)
        if len(contact):
            item['contact'] = ''.join(contact[0]).replace(' ', '')
        else:
            item['contact'] = ''
        item['mail'] = ''.join(re.findall('电子邮件：</dt><dd>(.*?)</dd>', html))
        item['state'] = ''.join(re.findall('经营状态：</td><td>(.*?)</td>', html))
        item['set_up'] = ''.join(re.findall('成立时间：</td><td>(.*?)</td>', html))
        item['capital'] = ''.join(re.findall('注册资本：</td><td>(.*?)</td>', html))
        item['license'] = ''.join(re.findall('营业执照号码：</td><td>(.*?)</td>', html))
        item['certificate'] = ''.join(re.findall('发证机关：</td><td>(.*?)</td>', html))
        item['audit'] = ''.join(re.findall('核准日期：</td><td>(.*?)</td>', html))
        item['operate'] = ''.join(re.findall('经营期限：</td><td>(.*?)</td>', html))
        item['district'] = ''.join(re.findall('所属城市：</td><td><a href=.*?>.*?href=".*?">(.*?)</a> ', html))
        item['cellphone'] = ''.join(re.findall('联系电话为：(.*?)">', html))
        item['url'] = response.meta['data'].get('url')
        item['name'] = response.meta['data'].get('name')
        item['sp_url'] = response.meta['data'].get('sp_url')
        item['min_type_href'] = response.meta['data'].get('min_type_href')
        item['province'] = response.meta['data'].get('province')
        item['city'] = response.meta['data'].get('city')
        item['type_name'] = response.meta['data'].get('type_name')
        item['min_type'] = response.meta['data'].get('min_type')
        item['facsimile'] = response.meta['data'].get('facsimile')
        item['legal_person'] = response.meta['data'].get('legal_person')
        item['founding_time'] = response.meta['data'].get('founding_time')
        item['dd'] =0
        if len(item['addr']) == 0 and item['dd'] !=3:
            item['dd'] = item['dd']+1
            print '###################'
            yield scrapy.Request(item['url'],meta={'data':item},dont_filter=True,callback=self.parse_home)
        else:
            yield item



    
    
    
    
    
    