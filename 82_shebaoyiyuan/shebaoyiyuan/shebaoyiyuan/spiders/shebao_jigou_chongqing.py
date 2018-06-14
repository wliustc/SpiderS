# -*- coding: utf-8 -*-
import scrapy
import re
import json
from shebaoyiyuan.items import ShebaoyuyuanItem
import time
class ShebaoJigouChongqingSpider(scrapy.Spider):
    name = "shebao_jigou_chongqing"
    allowed_domains = ["ggfw.cqhrss.gov.cn"]

    def start_requests(self):
        yield scrapy.Request('http://ggfw.cqhrss.gov.cn///ggfw/QueryBLH_mainSmXz.do?code=033',
                 headers={
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Accept-Encoding':'gzip, deflate, sdch',
                 'Accept-Language':'zh-CN,zh;q=0.8',
                 'Host':'ggfw.cqhrss.gov.cn',
                 'Upgrade-Insecure-Requests':'1',
                 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
                 },
                dont_filter=True, callback=self.get_country)

    def get_country(self,response):
        data=re.findall('jsonObj.+\{"[^\}]+}',response.body.decode('utf-8'))[0].split('=')[1]
        data=json.loads(data)
        for temp in data.keys():
            country=data[temp]
            value=temp
            yield scrapy.FormRequest(
                'http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do',
                 headers={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'ggfw.cqhrss.gov.cn',
            'Origin':'http://ggfw.cqhrss.gov.cn',
            'Referer':'http://ggfw.cqhrss.gov.cn///ggfw/QueryBLH_mainSmXz.do?code=033',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
                 },
                formdata={
                    'code': '033',
                    'ajbjg': value,
                    'bfwjgmc':'',
                     'afwjglx':'医院',
                     'ayydj':'',
                },
                meta={'item':{'countrycode':value}},
                dont_filter=True, callback=self.get_page_num)

    def get_page_num(self,response):
        data=json.loads(response.body)
        page_num=int(data['page']['pageCount'])
        for i in range(1,page_num+1):
            yield scrapy.FormRequest(
                'http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do',
                headers={
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'ggfw.cqhrss.gov.cn',
                    'Origin': 'http://ggfw.cqhrss.gov.cn',
                    'Referer': 'http://ggfw.cqhrss.gov.cn///ggfw/QueryBLH_mainSmXz.do?code=033',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                formdata={
                    'code': '033',
                    'ajbjg': response.meta['item']['countrycode'],
                    'bfwjgmc': '',
                    'afwjglx': '医院',
                    'ayydj': '',
                    'currentPage':str(i),
                    'goPage':'',
                },
                dont_filter=True, callback=self.get_item)

    def get_item(self,response):
        data = json.loads(response.body)
        temps=data['result']
        for temp in temps:
            item = ShebaoyuyuanItem()
            item['address']=temp['dz']
            item['kind']=temp['fwjglx']
            item['hospital']=temp['fwjgmc']
            item['sort']=temp['yydj']
            item['country']=temp['jbjgmc']
            item['type'] = '医疗机构'
            item['provice']='重庆'
            item['dt']=time.strftime('%Y-%m-%d', time.localtime())
            yield item

    
    
    
    
    
    