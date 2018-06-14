# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy import Selector
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')
ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

class HaodfSpider(scrapy.Spider):
    name = 'haodf'
    allowed_domains = []
    start_urls = ['http://www.haodf.com/keshi/list.htm']
    def __init__(self,*args,**kwargs):
        super(HaodfSpider,self).__init__(*args,**kwargs)
        self.url_dict = {u'眼科':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys568SUOWWDnLVkjst/daifu.htm',
                        '小儿眼科':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5PF-eJrfCtvjPWZm/daifu.htm',
                        '眼底':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5tBZ1r1eSOXJtQ6V/daifu.htm',
                        '角膜科':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5uVyfRVn-PGnW0KU/daifu.htm',
                        '青光眼':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5dPG7te0ZbpmRkBw/daifu.htm',
                        '白内障':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5BeC8w0mKcdfllDR/daifu.htm',
                        '眼外伤':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys58uK4ViVGr578RFJ/daifu.htm',
                        '眼眶及肿瘤':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5FfzhUmaHTMT0nH8/daifu.htm',
                        '屈光':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys5evHgmJTyVycem-7/daifu.htm',
                        '眼整形':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys76BZ1r1eSOXJtQ6V/daifu.htm',
                        '中医眼科':'http://haoping.haodf.com/keshi/DE4r0u-lSI6BDys7tPG7te0ZbpmRkBw/daifu.htm'
                        }
    def start_requests(self):
        for i in self.url_dict:
            name = i
            name_url = self.url_dict.get(i)
            yield scrapy.Request(name_url,meta={'name':name,'url':name_url},dont_filter=True,headers=ua,callback=self.parse)

    def parse(self, response):
        # print response.body
        if response.status == 200:
            yk_type = response.meta['name']
            html = response.body.decode('gb2312','ignore').encode('utf8')
            city = Selector(text=html).xpath('//*[@class="fz_default-list"]/li/a/text()').extract()
            city_url = Selector(text=html).xpath('//*[@class="fz_default-list"]/li/a/@href').extract()
            for i in zip(city,city_url)[1:]:
                url = i[1]
                yield scrapy.Request(url,meta={'yk_type':yk_type,'city':i[0],'city_url':i[1]},dont_filter=True,callback=self.city_parse)

    def city_parse(self,response):
        if response.status ==200:
            yk_type = response.meta['yk_type']
            city = response.meta['city']

            html = response.body.decode('gb2312','ignore').encode('utf8')
            pag = Selector(text=html).xpath('//*[@class="p_bar"]/a/text()').extract()
            doctor_name = Selector(text=html).xpath('//*[@class="good_doctor_list_td"]//td/a[@class="blue"]/text()').extract()
            doctor_url = Selector(text=html).xpath('//*[@class="good_doctor_list_td"]//td/a[1]/@href').extract()

            for i in zip(doctor_name,doctor_url):
                url = i[1]
                yield scrapy.Request(url,meta={'yk_type':yk_type,'city':city,'doctor_name':i[0],'doctor_url':doctor_url},dont_filter=True,callback=self.doctor_parse)

            if len(pag):
                parameter = ''.join(Selector(text=html).xpath('//*[@class="p_bar"]/a[2]/@href').extract())[0:-1]
                for i in range(2,int(pag[-4])+1):
                    url = parameter+str(i)
                    response.meta['pag_url']=url
                    yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.pag_parse)

    def pag_parse(self,response):
        if response.status == 200:
            yk_type = response.meta['yk_type']
            city = response.meta['city']

            html = response.body.decode('gb2312','ignore').encode('utf8')
            doctor_name = Selector(text=html).xpath('//*[@class="good_doctor_list_td"]//td/a[@class="blue"]/text()').extract()
            doctor_url = Selector(text=html).xpath('//*[@class="good_doctor_list_td"]//td/a[1]/@href').extract()

            for i in zip(doctor_name,doctor_url):
                url = i[1]

                yield scrapy.Request(url,
                                     meta={'yk_type': yk_type, 'city': city, 'doctor_name': i[0],
                                           'doctor_url': doctor_url}, dont_filter=True, callback=self.doctor_parse)


    def doctor_parse(self,response):
        if response.status == 200:
            # htmls = response.body.decode('gb2312','ignore')
            html =response.body.decode('gb2312','ignore').encode('utf8')
            BP = ''.join(Selector(text=html).xpath('//*[@id="gray"]/script/text()').extract())

            bp = codecs.decode(BP, 'unicode_escape').replace('\\', '')

            href = ''.join(Selector(text=bp).xpath('/html/body/div[4]/div/div[3]/a[4]/@href').extract())
            # level = ''.join(Selector(text=bp).xpath('/html/body/div[5]/div[2]/div/table[1]/tbody/tr[2]/td[3]/text()').extract())
            try:
                level = re.findall('<td valign="top">(.*?) </td>',bp)[0]
            except:
                level = re.findall('<td valign="top">(.*?)</td>',bp)[2]


            url = 'http://www.haodf.com' + href
            response.meta['href_url'] = url
            response.meta['level']=level
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.hospital_parse,)


    def hospital_parse(self,response):
        item = {}
        yk_type = response.meta['yk_type']
        city = response.meta['city']
        doctor_name = response.meta['doctor_name']
        level = response.meta['level']
        if response.status == 200:
            html = response.body.decode('gb2312', 'ignore').encode('utf8')
            cdx = ''.join(re.findall('<p class="f18">(.*?):</p>', html))
            if len(cdx):
                item['yk_type'] = yk_type
                item['province'] = city
                item['doctor_name'] = doctor_name
                item['level'] = level
                item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                yield item
            else:
                hospital_name = ''.join(Selector(text=html).xpath('//*[@id="contentA"]/div[1]/div[1]/ul/li/p/a/text()').extract())
                hospital_level = Selector(text=html).xpath('//*[@id="contentA"]/div[1]/div[1]/ul/li/p/text()').extract()
                item['hospital_name'] = hospital_name
                item['hospital_level'] = ''.join(hospital_level).replace(' ','').replace('(','').replace(')','')
                item['yk_type'] = yk_type
                item['province'] = city
                item['doctor_name'] = doctor_name
                item['level']= level
                item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                yield item
       

