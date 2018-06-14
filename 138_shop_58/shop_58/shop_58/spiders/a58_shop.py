# -*- coding: utf-8 -*-
import scrapy
import re
import json
from shop_58.items import Tongcheng58Item
import time
import logging


class A58ShopSpider(scrapy.Spider):
    name = "58_shop"
    allowed_domains = []
    start_urls = []
    handle_httpstatus_list = [302]

    def start_requests(self):
        url = 'http://www.58.com/changecity.html?catepath=shangpucz'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.58.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_city, dont_filter=True)

    def get_city(self, response):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        datas = response.xpath('//script[3]/text()').extract()[0]
        datas = re.search('independentCityList =(?P<name>(\s|.)+)', datas).groupdict()['name']
        datas = datas.split('var cityList = ')

        temps = list(map(lambda x: json.loads(x), datas))

        for i, datas in enumerate(temps):
            for provice in datas.keys():
                if i == 1:
                    data = datas[provice]
                    for city in data.keys():
                        url = 'http://' + data[city].split('|')[0] + '.58.com/shangpucz/'
                        header['host'] = data[city].split('|')[0] + '.58.com'
                        yield scrapy.Request(url, headers=header, callback=self.get_district, dont_filter=True, meta={
                            'item': {'city': city, 'host': header['host']}, 'page': 1, 'end_page': 0
                        })
                else:
                    data = datas[provice]
                    url = 'http://' + data.split('|')[0] + '.58.com/shangpucz/'
                    header['host'] = data.split('|')[0] + '.58.com'
                    yield scrapy.Request(url, headers=header, callback=self.get_district, dont_filter=True, meta={
                        'item': {'city': provice, 'host': header['host']}, 'page': 1, 'end_page': 0
                    })

    def get_district(self, response):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        dists = response.xpath('//dl[@class="secitem"][1]/dd/a')
        for i, dist in enumerate(dists):
            if i == 0:
                continue
            dist_name = dist.css('::text').extract()[0].strip()
            url = 'http://' + response.meta['item']['host'] + dist.css('::attr("href")').extract()[0]
            yield scrapy.Request(url, headers=header, callback=self.get_shop_list, dont_filter=True, meta={
                'item': {
                    'base_url': url,
                    'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                    'dist_name': dist_name}, 'page': 1, 'end_page': 0,
            })

    def get_shop_list(self, response):
        page = response.meta['page']
        end_page = response.meta['end_page']
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        lists_base = response.xpath('//div[@class="list-info"]/h2/a/@href').extract()
        if not end_page:
            try:
                end_page = int(response.xpath('//div[@class="pager"]/a[not(@class)]//text()').extract()[-1])
            except Exception as e:
                end_page = 1
        if page < end_page:
            page += 1
            header['host'] = response.meta['item']['host']
            url = response.meta['item']['base_url'] + 'pn%s/' % page
            yield scrapy.Request(url, headers=header, callback=self.get_shop_list, dont_filter=True, meta={
                'item': {'base_url': response.meta['item']['base_url'], 'city': response.meta['item']['city'],
                         'dist_name': response.meta['item']['dist_name'], 'host': header['host']},
                'page': page, 'end_page': end_page,
            })
        for url in lists_base:
            if url.split('/')[2] == 'jxjump.58.com':
                header['host'] = 'jxjump.58.com'
                yield scrapy.Request(url, callback=self.get_rediect_info, headers=header, dont_filter=True, meta={
                    'item': {'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                             'dist_name': response.meta['item']['dist_name']},
                    'request_item': lists_base
                })
            elif url.split('/')[2] == response.meta['item']['host']:
                header['host'] = response.meta['item']['host']
                yield scrapy.Request(url, callback=self.get_shop_item, headers=header, dont_filter=True, meta={
                    'item': {'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                             'dist_name': response.meta['item']['dist_name']},
                    'request_item': lists_base
                })
            elif url.split('/')[2] == 'short.58.com':
                header['host'] = 'short.58.com'
                yield scrapy.Request(url, callback=self.get_jing58_redect, headers=header, dont_filter=True, meta={
                    'item': {'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                             'dist_name': response.meta['item']['dist_name']},
                    'request_item': lists_base
                })
            else:
                header['host'] = url.split('/')[2]
                yield scrapy.Request(url, callback=self.get_shop_item, headers=header, dont_filter=True, meta={
                    'item': {'host': header['host'],
                             'place_recheck': True},
                    'request_item': lists_base
                })

    def get_jing58_redect(self, response):
        url = response.headers['Location'].decode()
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        header['host'] = url.split('/')[2]
        yield scrapy.Request(url, callback=self.get_rediect_info, headers=header, dont_filter=True, meta={
            'item': {'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                     'dist_name': response.meta['item']['dist_name']},
            'request_item': response.meta['request_item']
        })

    def get_rediect_info(self, response):
        url = response.headers['Location'].decode()
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        header['host'] = response.meta['item']['host']
        yield scrapy.Request(url, callback=self.get_shop_item, headers=header, dont_filter=True, meta={
            'item': {'city': response.meta['item']['city'], 'host': response.meta['item']['host'],
                     'dist_name': response.meta['item']['dist_name']},
            'request_item': response.meta['request_item']
        })

    def get_shop_item(self, response):
        item = Tongcheng58Item()
        html = response.body.decode()
        url = response.url
        data = re.findall('_trackParams":\[(.*?)\],"_trackPageview"', html)
        zuobiao = re.findall(r'[0-9]{2}\.[0-9]{2,}|[0-9]{3}\.[0-9]{2,}', ''.join(data))
        area = ''.join(re.findall(r'房屋面积:</span>.*?>(.*?)</span>', html, re.S))
        if 'place_recheck' in response.meta['item']:
            temp = response.xpath('//meta[@name="location"]/@content').extract()[0]
            item['city'] = temp.split(';')[0].split('=')[1]
            district = temp.split(';')[1].split('=')[1]
        else:
            item['city'] = response.meta['item']['city']
            district = response.meta['item']['dist_name']
        bdistrict = response.xpath('//ul[@class="house_basic_title_content"]/li[6]//text()').extract()[0]
        addr = ''.join((''.join(re.findall(r'<span class="house_basic_title_content_item3 xxdz-des">(.*?)</span>', html,
                                           re.S)).split())).replace('&nbsp;', '')
        if len(zuobiao) > 3:
            lng = zuobiao[1]
            lat = zuobiao[0]
        else:
            lng = ''
            lat = ''
        item['deal_id'] = response.meta['item']['host'].split('.')[0] + '|' + \
                          url.split('?')[0].split('/')[-1].split('.')[0]
        try:
            item['bdistrict'] = bdistrict
        except Exception as e:
            item['bdistrict'] = None
        item['url'] = url
        item['area'] = area
        item['district'] = district
        item['addr'] = addr
        item['lng'] = lng
        item['lat'] = lat
        item['title'] = response.xpath('//div[@class="house-title"]/h1/text()').extract()[0].strip()
        item['price'] = response.css('.house_basic_title_money_num::text').extract()[0]
        item['update_time'] = response.xpath('//p[@class="house-update-info"]/span[1]/text()').extract()[0]
        item['type'] = response.xpath(u'//span[contains(./text(), "类")]/following-sibling::*[1]//text()').extract()[0]
        item['miaoshu'] = ''.join(response.xpath(u'//h3[text()="描述"]/following-sibling::div[1]//text()').extract())
        item['connect'] = response.xpath('//div[@class="house_basic_jingji"]/p/span/text()').extract()[0].split('-')[-1]
        item['phone'] = response.css('.phone-num::text').extract()[0]
        item['statics'] = \
            response.xpath(u'//span[contains(./text(), "经营状态:")]/following-sibling::*[1]//text()').extract()[0].strip()
        item['img'] = ','.join(response.css('.general-pic-list img::attr("data-src")').extract())
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
        yield item
        '''
    o 临近（58上的描述）
    o 房源描述
    o 图片
        '''