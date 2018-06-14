# -*- coding: utf-8 -*-
import scrapy
import sys
import re
import web
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy import Selector
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Connection':'keep-alive',
           'Host':'db.yaozh.com',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(HomeSpider,self).__init__(*args,**kwargs)
        self.home = '''https://db.yaozh.com/hmap/39762.html'''

    def start_requests(self):
        sql = '''SELECT DISTINCT url  FROM `t_spider_yaozhi` limit 100 '''
        for i in db.query(sql):
            # url = self.home
            url = i.get('url')
            # print url
            yield scrapy.Request(url,headers=headers,meta={'url':url})


    def parse(self, response):
        html = response.body
        item = {}
        hosp_name =  ''.join(''.join(re.findall('医院名称</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        alias = ''.join(''.join(re.findall('医院别名</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>', html, re.S)).split())
        level = ''.join(''.join(re.findall('医院等级</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        type_ = ''.join(''.join(re.findall('医院类型</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        create_year = ''.join(''.join(re.findall('建院年份</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        beds = ''.join(''.join(re.findall('床位数</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        amount = ''.join(''.join(re.findall('门诊量(日)</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        province = ''.join(''.join(re.findall('省</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        city = ''.join(''.join(re.findall('市</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        counties = ''.join(''.join(re.findall('县</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        tel = ''.join(''.join(re.findall('电话</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        address = ''.join(''.join(re.findall('医院地址</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        postcode = ''.join(''.join(re.findall('邮编</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        way = ''.join(''.join(re.findall('经营方式</th>.*?<td>.*?<span class="toFindImg">(.*?)</span>',html,re.S)).split())
        item['hosp_name']=hosp_name
        item['level']= level
        item['type_'] =type_
        item['create_year'] = create_year
        item['beds'] = beds
        item['amount'] = amount
        item['province'] = province
        item['city'] = city
        item['counties'] = counties
        item['tel'] = tel
        item['address'] =address
        item['postcode'] = postcode
        item['url'] = response.meta['url']
        item['alias'] = alias
        item['way'] = way
        if len(item['hosp_name']):
            yield item
        else:
            url = item['url']
            yield scrapy.Request(url, headers=headers, meta={'url': url},callback=self.parse)


