# -*- coding: utf-8 -*-
import scrapy
import sys
from shebaoyiyuan.items import ShebaoyuyuanItem
import time

class ShebaoJigouBjSpider(scrapy.Spider):
    name = "shebao_jigou_bj"
    allowed_domains = ["www.hl.lss.gov.cn"]
    
    def start_requests(self):
        urls=['http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_01_outline_new.jsp']
        yield scrapy.Request(urls[0],method='POST',body='SearchWord=&sword=&suoshu=00&leibie=00&x=14&y=11',dont_filter=True)

    def parse(self, response):
        item_nums=response.css('body > center > table:nth-child(3)')
        page=int(item_nums.css('table')[1].css('b font::text').extract()[1])
        for i in range(0,page):
            url='http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_01_outline_new.jsp?sno=%s&spage=0&epage=10&leibie=00&suoshu=00&sword=' %(i*20)
            yield scrapy.Request(url,callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        table = response.css('body > center > table:nth-child(3)')
        table = table.css('table')[2]
        trs=table.css('tr')
        for i,tr in enumerate(trs):
            item = ShebaoyuyuanItem()
            if i==0:
                continue
            try:
                item['code']=tr.css('td')[0].css('a::text').extract()[0].encode('utf-8')
                item['hospital'] = tr.css('td')[1].css('a::text').extract()[0].encode('utf-8')
                item['country'] = tr.css('td')[2].css('span::text').extract()[0].encode('utf-8')
                item['kind'] = tr.css('td')[3].css('span::text').extract()[0].encode('utf-8')
                item['sort'] = tr.css('td')[4].css('span::text').extract()[0].encode('utf-8')
                item['type'] = '医疗机构'
                item['provice']='北京'
                item['address']=''
                item['lng']=''
                item['lat']=''
                item['dt']=time.strftime('%Y-%m-%d', time.localtime())
                item['city']='北京'
                yield item
            except Exception as e:
                pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    