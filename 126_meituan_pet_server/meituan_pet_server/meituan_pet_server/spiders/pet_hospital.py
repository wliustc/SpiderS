# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import time
import re
import json
import traceback
import sqlalchemy
from meituan_pet_server.items import MeituanPetHospitalshopItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class PetHospitalSpider(scrapy.Spider):
    handle_httpstatus_list = [500, 503]
    name = "pet_hospital"
    allowed_domains = ["http://www.meituan.com"]

    def start_requests(self):
        url = 'http://www.meituan.com/index/changecity/initiative'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'www.meituan.com',
            'Upgrade-Insecure-Requests': '1'
        }
        yield scrapy.Request(url, self.get_city_url, headers=header, dont_filter=True)

    def get_city_url(self, response):
        city_list = response.css('.citieslist a')
        for i, city in enumerate(city_list):
            city_name = city.css('::text').extract()[0]
            url = city.css('::attr("href")').extract()[0]
            header = {
                'Host': url.split('/')[-1].split('?')[0],
                'Referer': 'http://www.meituan.com/index/changecity/initiative',
                'Upgrade-Insecure-Requests': '1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'
            }

            yield scrapy.Request(url, headers=header,
                                 meta={"timerequest": 0, 'cookiejar': i, 'item': {'city_name': city_name, 'host':
                                     url.split('/')[-1].split('?')[0]}}, callback=self.goto_pet, dont_filter=True,
                                 errback=self.error_callback)

    def goto_pet(self, response):
        if response.status == 500 or response.status == 503:
            return
        brand = u'宠物医院'
        temps = response.xpath(
            '//div[contains(@class,"category-nav-detail")]/div[@class="detail-area"]/div[@class="detail-content"]/a[text()="%s"]' % brand)
        for temp in temps:
            type = temp.css('::text').extract()[0]
            url = temp.css('::attr("href")').extract()[0]
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': response.meta['item']['host'],
                'Referer': response.url,
                'Upgrade-Insecure-Requests': '1',}
            yield scrapy.Request(url, headers=header, meta={"timerequest": 0, 'cookiejar': response.meta['cookiejar'],
                                                            'item': {'city_name': response.meta['item']['city_name'],
                                                                     'type': type,
                                                                     'host': response.meta['item']['host']}},
                                 callback=self.get_district,
                                 dont_filter=True, errback=self.error_callback)

    def get_district(self, response):  # 进了宠物页面,
        if response.status == 500 or response.status == 503:
            return
        try:
            category=response.xpath('//span[@class="header-categorys-cate"]/text()').extract()[0].split(' ')[-1]
        except Exception as e:
            self.logger.error('meituan category error %s', response.request.url)
            return
        if category!='宠物':
            return
        if response.xpath('//span[@class="current-city"]/text()').extract()[0] != response.meta['item']['city_name']:
            return
        temps = response.xpath('//div[@class="filter-section-wrapper"]/div[1]/div[@class="tags"]/div/div')
        for temp in temps:
            tmps = response.xpath('//div[@class="filter-section-wrapper"]/div[2]/div[@class="tags"]/div/div')
            for i, tmp in enumerate(tmps):
                if i == 0:
                    continue
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Host': response.meta['item']['host'],
                    'Referer': response.url,
                    'Upgrade-Insecure-Requests': '1',
                }
                url = 'http:' + temp.xpath('a/@href').extract()[0]
                type = temp.xpath('a/span/text()').extract()[0]
                url_distact = tmp.css('a::attr("href")').extract()[0].split('/')[-2]
                url = url.strip('/')
                url = url + url_distact + '/'
                distact = tmp.css('a span::text').extract()[0]
                city_name = response.meta['item']['city_name']
                yield scrapy.Request(url, headers=header,
                                     meta={"timerequest": 0, 'cookiejar': response.meta['cookiejar'],
                                           'item': {'city_name': city_name,
                                                    'type': type,
                                                    'distract': distact, 'host': response.meta['item']['host']}},
                                     callback=self.get_first_page, errback=self.error_callback,
                                     dont_filter=True)

    def get_first_page(self, response):
        if response.status == 500 or response.status == 503:
            return
        try:
            page_length = int(response.css('.pagination-item.num-item a::text').extract()[-1])
        except Exception as e:
            print("page_length can't find")
            page_length = 0
        for i in range(1, page_length + 1):
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': response.meta['item']['host'],
                'Referer': 'http://' + response.meta['item']['host'] + '/',
                'Upgrade-Insecure-Requests': '1',
            }

            url = response.url + 'pn%s' % i
            yield scrapy.Request(url, headers=header,
                                 meta={"timerequest": 0, 'cookiejar': response.meta['cookiejar'],
                                       'item': {'city_name': response.meta['item']['city_name'],
                                                'type': response.meta['item']['type'],
                                                'distract': response.meta['item']['distract'],
                                                'host': response.meta['item']['host']}
                                       },
                                 callback=self.get_item,
                                 dont_filter=True, errback=self.error_callback)

    def get_item(self, response):
        if response.status == 500 or response.status == 503:
            return
        temps = response.css('.abstract-item.clearfix')
        for temp in temps:
            item = MeituanPetHospitalshopItem()
            item['mtshop_name'] = temp.css('.list-item-desc-top a::text').extract()[0]
            item['shop_url'] = 'http:' + temp.css('.list-item-desc-top a::attr("href")').extract()[0]
            item['mtshop_id'] = item['shop_url'].split('/')[-2]
            try:
                item['score'] = temp.xpath('//div[contains(@class, "item-eval-info")]/span[1]/text()').extract()[0]
            except Exception as e:
                traceback.print_exc()
                item['score'] = None
            try:
                item['pinglun_num'] = temp.xpath('//div[contains(@class, "item-eval-info")]/span[2]/text()').extract()[
                    0]
            except Exception as e:
                traceback.print_exc()
                item['pinglun_num'] = None
            try:
                item['shop_sale_num'] = \
                temp.xpath('//div[contains(@class, "item-eval-info")]/span[3]/text()').extract()[0]
            except Exception as e:
                traceback.print_exc()
                item['shop_sale_num'] = None
            try:
                item['dist'] = temp.xpath('//div[contains(@class, "item-site-info")]/span[1]/text()').extract()[2]
            except Exception as e:
                traceback.print_exc()
                item['dist'] = None

            try:
                item['address'] = temp.xpath('//div[contains(@class, "item-site-info")]/span[2]/text()').extract()[0]
            except Exception as e:
                traceback.print_exc()
                item['address'] = None
            try:
                item['avg_price'] = temp.xpath('//div[contains(@class, "item-site-info")]/span[2]/text()').extract()[0]
            except Exception as e:
                traceback.print_exc()
                item['avg_price'] = None
            item['host'] = response.meta['item']['host']
            item['city_name'] = response.meta['item']['city_name']
            item['type'] = response.meta['item']['type']
            item['distract'] = response.meta['item']['distract']
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            url = 'http://www.meituan.com/chongwu/%s/' % item['mtshop_id']
            yield item

    def error_callback(self, failure):
        request = failure.request
        if 'timerequest' not in request.meta.keys():
            request.meta['timerequest'] = 0
        if request.meta['timerequest'] > 10:
            error_info = {}
            error_info['url'] = request.url
            error_info['host'] = request.meta['item']['host']
            error_info['city_name'] = request.meta['item']['city_name'].decode()
            error_info['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if request.url.split('/')[-1] == '':
                error_info['kind'] = 0
            else:
                error_info['kind'] = 1
            if 'type' in request.meta['item'].keys():
                error_info['type'] = request.meta['item']['type']
            else:
                error_info['type'] = '/'
            if 'distract' in request.meta['item'].keys():
                error_info['distract'] = request.meta['item']['distract']
            else:
                error_info['distract'] = '/'
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_pet_hospital_err', metadata,
                                           sqlalchemy.Column('url', sqlalchemy.String(100)),
                                           sqlalchemy.Column('city_name', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('type', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('host', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('distract', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('kind', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(1000)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(error_info)
            self.logger.error('qfliu retrytime out %s', request.url)
            return
        if failure.check(HttpError):
            response = failure.value.response
            request.meta['timerequest'] += 1
            request.meta['cookiejar'] = request.url + str(request.meta['timerequest'])
            header = {
                'Host': request.headers['Host'],
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
            }
            yield scrapy.Request(request.url, headers=header,
                                 meta=request.meta,
                                 callback=request.callback,
                                 dont_filter=True, errback=self.error_callback)
            self.logger.error('HttpError on %s ,%s,       cookiejar %s,proxy %s', response.url, response.status,
                              request.meta['cookiejar'], request.meta['proxy'])
        elif failure.check(TimeoutError, TCPTimedOutError):
            request.meta['timerequest'] += 1
            request.meta['cookiejar'] = request.url + str(request.meta['timerequest'])
            header = {
                'Host': request.headers['Host'],
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
            }
            yield scrapy.Request(request.url, headers=header,
                                 meta=request.meta,
                                 callback=request.callback,
                                 dont_filter=True, errback=self.error_callback)
            self.logger.error('TimeoutError on %s ,       cookiejar %s,proxy %s', request.url,
                              request.meta['cookiejar'], request.meta['proxy'])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    