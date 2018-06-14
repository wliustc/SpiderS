# -*- coding: utf-8 -*-
import scrapy
from shebaoyiyuan.items import ShebaoyuyuanItem
import time
class ShebaoYaodianHljSpider(scrapy.Spider):
    name = "shebao_yaodian_hlj"
    allowed_domains = ["www.hl.lss.gov.cn"]

    def start_requests(self):
        yield scrapy.Request('http://www.hl.lss.gov.cn/hljsyb/list.jsp?type=yd', dont_filter=True)

    def parse(self, response):
        data_urls = response.xpath('//*[@class="list03"]//a')
        for data in data_urls:
            city = data.xpath('text()').extract()[0]
            url = 'http://www.hl.lss.gov.cn/hljsyb/' + data.xpath('@href').extract()[0]
            yield scrapy.Request(url, dont_filter=True,
                                 meta={'item': {'city': city}},
                                 callback=self.parser_country
                                 )

    def parser_country(self, response):
        temps = response.xpath('//select[@onchange="doChange(this.value)"]/option')
        for temp in temps:
            country = temp.xpath('text()').extract()[0]
            value = temp.xpath('@value').extract()[0]
            url = 'http://www.hl.lss.gov.cn/hljsyb/listView.jsp?type=yd&id=' + value
            yield scrapy.Request(url, dont_filter=True,
                                 meta={'item': {'city': response.meta['item']['city'], 'country': country}},
                                 callback=self.parser_item
                                 )

    def parser_item(self, response):
        temps = response.xpath('//table[@class="border"]//tr')
        for i, temp in enumerate(temps):
            if i==0:
                continue
            item = ShebaoyuyuanItem()
            item['code'] = temp.xpath('td[1]/text()').extract()[0].strip()
            item['hospital'] = temp.xpath('td[2]/text()').extract()[0].strip()
            item['address'] = temp.xpath('td[3]/text()').extract()[0].strip()
            item['provice'] = '黑龙江'
            item['city'] = response.meta['item']['city']
            item['country'] = response.meta['item']['country']
            item['kind'] = '零售药店'
            item['dt']=time.strftime('%Y-%m-%d', time.localtime())
            yield item

    
    
    