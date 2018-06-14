# -*- coding: utf-8 -*-
import scrapy
from shebaoyiyuan.items import ShebaoyuyuanItem
import time
class ShebaoYaodianShanghaiSpider(scrapy.Spider):
    name = "shebao_yaodian_shanghai"
    allowed_domains = ["www.12333sh.gov.cn"]


    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ybj.sh.gov.cn',
            'Origin': 'http://ybj.sh.gov.cn',
            'Referer': 'http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        }
        yield scrapy.FormRequest('http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
                                 formdata={'pageno': '1', 'qxcode': '01', 'grade': '',
                                           'unitname': '', 'address': ''},
                                 headers=headers, dont_filter=True,
                                 meta={'item': {'addresscode': 1, 'provice': '上海'}},
                                 callback=self.get_countrycode)


    def get_countrycode(self, response):
        options = response.xpath("//select[@name='qxcode']/option")
        for data in options:
            value = data.xpath('@value').extract()[0]
            country = data.xpath('text()').extract()[0]
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'ybj.sh.gov.cn',
                'Origin': 'http://ybj.sh.gov.cn',
                'Referer': 'http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            }
            yield scrapy.FormRequest('http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
                                     formdata={'pageno': '1', 'qxcode': value, 'grade': '', 'unitname': '',
                                               'address': ''},
                                     headers=headers, dont_filter=True,
                                     meta={'item': {'addresscode': value, 'provice': '上海'}},
                                     callback=self.get_pagenum)


    def get_pagenum(self, response):
        try:
            page=response.css('.yypages a')
            page = page[-2]
            page = int(page.xpath('text()').extract()[0])
        except Exception as e:
            page=1
        for i in range(1, page + 1):
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'ybj.sh.gov.cn',
                'Origin': 'http://ybj.sh.gov.cn',
                'Referer': 'http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            }
            yield scrapy.FormRequest('http://ybj.sh.gov.cn/xxcx/ddyd.jsp',
                                     formdata={'pageno': '%s' % i, 'qxcode': '%s' % response.meta['item']['addresscode'],
                                               'grade': '', 'unitname': '', 'address': ''
                                               },
                                     headers=headers, dont_filter=True, meta=response.meta,
                                     callback=self.parse_item)


    def parse_item(self, response):
        trs = response.xpath("//table//tr[@bgcolor='#FFFFFF']")
        for tr in trs:
            item = ShebaoyuyuanItem()
            if tr.xpath('td[2]/text()').extract()[0] != 'null':
                item['provice'] = response.meta['item']['provice']
                item['city'] = response.meta['item']['provice']
                item['country'] = tr.xpath('td[1]/text()').extract()[0]
                item['hospital'] = tr.xpath('td[2]/text()').extract()[0]
                item['address'] = tr.xpath('td[3]/text()').extract()[0]  
                item['type'] = '零售药店'
                item['dt']=time.strftime('%Y-%m-%d', time.localtime())

            yield item
    
    
    
    
    
    
    
    
    
    
    