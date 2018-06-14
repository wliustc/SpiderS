# -*- coding: utf-8 -*-
import scrapy
import re
from shebaoyiyuan.items import ShebaoyuyuanItem
import time
class ShebaoJigouGzSpider(scrapy.Spider):
    name = "shebao_jigou_gz"
    allowed_domains = ["www.gzyb.net"]

    def start_requests(self):
        yield scrapy.FormRequest('http://www.gzyb.net/infoquery/QueryDdyljgData.action',
                                 method='POST',
                                 formdata={'pageSize': '20', 'pageNo': '1', 'mis_name': '', 'mis_area': '',
                                           'mis_grade': ''},
                                 dont_filter=True, callback=self.parse)

    def parse(self, response):
        body=response.body.decode('GBK')
        itemcount=int(re.search('pager.itemCount.+=[ ]+(?P<number>[0-9]+)',body).group('number'))
        page_count=0
        if itemcount:
            page_count=(itemcount-1)//20+1
        for i in range(1,page_count+1):
            yield scrapy.FormRequest('http://www.gzyb.net/infoquery/QueryDdyljgData.action',
                                 method='POST',
                                 formdata={'pageSize':'20','pageNo':str(i),'mis_name':'','mis_area':'','mis_grade':''},
                                 dont_filter=True,callback=self.parse_item)

    def parse_item(self,response):
        trs=response.xpath("//div[@class='mima03']/table[1]//tr")
        item=ShebaoyuyuanItem()
        for i,tr in enumerate(trs):
            if i==0:
                continue
            item['hospital']=tr.xpath('td[2]/text()').extract()[0].strip()
            item['country'] = tr.xpath('td[8]/text()').extract()[0].strip()
            item['sort'] = tr.xpath('td[3]/text()').extract()[0].strip()
            item['kind'] = tr.xpath('td[4]/text()').extract()[0].strip()
            item['address'] = tr.xpath('td[7]/text()').extract()[0].strip()
            item['type'] = '医疗机构'
            item['city'] = '广州'
            item['provice'] = '广东'
            item['dt']=time.strftime('%Y-%m-%d', time.localtime())
            yield item
    
    
    