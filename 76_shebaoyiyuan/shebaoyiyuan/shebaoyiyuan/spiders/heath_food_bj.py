# -*- coding: utf-8 -*-
import scrapy
import re
from shebaoyiyuan.items import HeathFoodbjItem

class HeathFoodBjSpider(scrapy.Spider):
    name = "heath_food_bj"
    allowed_domains = ["www.bjda.gov.cn"]

    def start_requests(self):
        urls=['http://www.bjda.gov.cn/eportal/ui?pageId=331184']
        yield scrapy.Request(urls[0],dont_filter=True)

    def parse(self, response):
        tmp=response.css('.Normal')[0].css('::text').extract()[1].split(',')[0]
        tmp=int(re.sub('[^0-9]+','',tmp))
        page=  tmp%20 and tmp//20+1 or tmp//20
        for i in range(0,page):
            yield scrapy.Request('http://www.bjda.gov.cn/eportal/ui?pageId=331184',method='POST',
                           body='filter_LIKE_XKZH=&filter_LIKE_TITLE=&filter_EQ_FZJG=&currentPage=%s&pageSize=20' %i,
                           callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        temps=response.css('.chaxun_con')
        print(len(temps))
        for temp in temps:
            item=HeathFoodbjItem()
            item['licensekey'] = temp.css('td')[1].css('::text').extract()[0]
            item['company'] = temp.css('td')[2].css('::text').extract()[0]
            item['date_issue'] = temp.css('td')[3].css('::text').extract()[0]
            item['term'] = temp.css('td')[4].css('::text').extract()[0]
            yield item


    