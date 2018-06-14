# -*- coding: utf-8 -*-
import scrapy
import json
import re
import execjs
import time
import copy
from gongjiao_8684.items import Gongjiao8684Item
class GongjiaoSpider(scrapy.Spider):
    name = "gongjiao"
    allowed_domains = ["www.8684.cn"]
    start_urls = ['http://js.8684.cn/citys/city_boxInf.min.js']


    def parse(self, response):
        temps=re.search('{.+',response.body.decode('utf8')).group().strip(';')
        temps=execjs.eval(temps)
        for key in temps.keys():
            provice=copy.deepcopy(key)
            temp=temps[key]
            for key in temp:
                url='http://'+key+'.8684.cn/'
                yield scrapy.Request(url,dont_filter=True,callback=self.in_city,meta={'item':{'provice':provice,'city':temp[key]}})

    def in_city(self,response):
        temps=response.xpath('//div[@class="bus_layer"][1]/div[4]/div/a')
        for temp in temps:
            tran_type=temp.css("::text").extract()[0]
            url=response.url.strip('/')+temp.css("::attr('href')").extract()[0]
            yield scrapy.Request(url, dont_filter=True, callback=self.in_tran_type,
                                 meta={'item': {'provice': response.meta['item']['provice'],
                                                'city': response.meta['item']['city'],
                                                'tran_type':tran_type}})

    def in_tran_type(self,response):
        temps=response.xpath('//div[@id="con_site_1"]/a')
        url_base=response.url.split('/')[2]
        for temp in temps:
            url='http://'+url_base+temp.css('::attr("href")').extract()[0]
            line_name=temp.css('::text').extract()[0]
            yield scrapy.Request(url, dont_filter=True, callback=self.in_line_num,
                                 meta={'item': {'provice': response.meta['item']['provice'],
                                                'city': response.meta['item']['city'],
                                                'tran_type': response.meta['item']['tran_type'],
                                                'line_name':line_name}})

    def in_line_num(self,response):
        data_bus=response.xpath('//div[@class="bus_i_content"]')
        title=data_bus.xpath('//div[@class="bus_i_t1"]//text()').extract()[0]
        transform_time= data_bus.xpath('//p[@class="bus_i_t4"][1]//text()').extract()[0]
        piaojia = data_bus.xpath('//p[@class="bus_i_t4"][2]//text()').extract()[0]
        try:
        	company = data_bus.xpath('//p[@class="bus_i_t4"][3]/a/text()').extract()[0]
        except Exception as e:
            company = ''
        update_time=data_bus.xpath('//p[@class="bus_i_t4"][4]//text()').extract()[0]
        try:
            descript=response.xpath('//div[@class="bus_label "]//text()').extract()[0]
        except Exception as e:
            descript=''
        for temp in response.xpath('//div[@class="bus_line_top "]'):
            direct=temp.xpath('//strong/text()').extract()[0]
            bus_sum_num=temp.xpath('//span[@class="bus_line_no"]/text()').extract()[0]
            bus_sum_num=re.sub('[^0-9]+','',bus_sum_num)
            for i in temp.xpath('following-sibling::div[@class="bus_line_site "][1]//div[not(@class)]'):
                item = Gongjiao8684Item()
                item['provice'] = response.meta['item']['provice']
                item['city'] = response.meta['item']['city']
                item['tran_type'] = response.meta['item']['tran_type']
                item['line_name'] = response.meta['item']['line_name']
                item['title'] = title
                item['transform_time'] = transform_time
                item['piaojia'] = piaojia
                item['company'] = company
                item['update_time'] = update_time
                item['descript'] = descript
                item['direct'] = direct
                item['bus_sum_num'] = bus_sum_num
                item['port_num'] = i.xpath('//i/text()').extract()[0]
                try:
                	item['port_name'] =  i.css('a::text').extract()[0]
                except Exception as e:
                    item['port_name'] = ''
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                yield item
    
    
    