# -*- coding: utf-8 -*-
import scrapy
from shebaoyiyuan.items import ShebaoyuyuanItem

class LingshouyaodianSpider(scrapy.Spider):
    name = "lingshouyaodian"

    def start_requests(self):
        urls=['http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_02_outline_new.jsp']
        yield scrapy.Request(urls[0],method='POST',body='SearchWord=&sword=&suoshu=00&x=28&y=2',dont_filter=True)

    def parse(self, response):
        item_nums=response.css('body > center > table:nth-child(3)')
        page=int(item_nums.css('table')[1].css('b font::text').extract()[1])
        for i in range(0,page):
            url='http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_02_outline_new.jsp?sno=%s&spage=0&epage=5&leibie=&suoshu=00&sword=' %(i*20)
            yield scrapy.Request(url,callback=self.parse_item,dont_filter=True)


    def parse_item(self, response):
        table = response.css('body > center > table:nth-child(3)')
        table = table.css('table')[2]
        trs=table.css('tr')
        print(len(trs))
        for i,tr in enumerate(trs):
            item = ShebaoyuyuanItem()
            if i==0:
                continue
            try:
                item['code']=tr.css('td')[0].css('a::text').extract()[0]
                item['hospital'] = tr.css('td')[1].css('a::text').extract()[0]
                item['county'] = tr.css('td')[2].css('span::text').extract()[0]
                item['kind'] = ''
                item['sort'] = ''
                item['address']=tr.css('td')[3].css('span::text').extract()[0]
                item['type'] = '零售药店'
                print(item['type'])
                yield item
            except Exception as e:
                print(e)
                pass

    
    