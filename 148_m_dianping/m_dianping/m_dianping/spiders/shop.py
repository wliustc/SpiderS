# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
import sys
from m_dianping.items import DianpingShopItem
from m_dianping.items import DianpingDealItem


class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["m.dianping.com"]
    start_urls = ['http://m.dianping.com/']

    def start_requests(self):
        url = 'https://m.dianping.com/citylist'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'm.dianping.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_index_url, dont_filter=True)

    def get_index_url(self, response):
        url = 'https://m.dianping.com/citylist'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'm.dianping.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_city_id, dont_filter=True)

    def get_city_id(self, response):
        city_list = response.xpath('//div[@class="hot-trade modebox" and @id]//li/a')
        for i, city in enumerate(city_list):
            city_pinyin = city.css('::text').extract()[0]
            url = city.css('::attr("href")').extract()[0]
            if city_pinyin != '更多':
                continue
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            url = 'https:' + url
            yield scrapy.Request(url, headers=header, callback=self.get_city_id_detail, dont_filter=True)

    def get_city_id_detail(self, response):
        temps = response.xpath('//ul[@class="J_citylist"]//li/a')
        for temp in temps:
            pinyin = temp.css('::attr("href")').extract()[0].split('/')[-1].split('?')[0]
            city_name = temp.css('::text').extract()[0]
            city_id = temp.css('::attr("data-id")').extract()[0]
            url = 'https:' + temp.css('::attr("href")').extract()[0]
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.goto_city, dont_filter=True, meta=
            {'item': {'city_name': city_name, 'pinyin': pinyin, 'city_id': city_id},'cookiejar':city_id})

    def goto_city(self, response):
        data=['诊所','卫生服务','医院','中医']
        for d in data:
            url = 'https://mapi.dianping.com/searchshop.json?start=%s&' \
                  'categoryid=0&parentCategoryId=0&limit=20&' \
                  'sortid=0&cityid=%s&keyword=%s&regionid=0&maptype=0' % (0, response.meta['item']['city_id'], d)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'mapi.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta=
            {'item': {'city_name': response.meta['item']['city_name'], 'pinyin': response.meta['item']['pinyin'],
                  'city_id': response.meta['item']['city_id'], 'page_num': 0,'search_word':d},'cookiejar':response.meta['cookiejar']})

    def get_item(self, response):
        page_num = response.meta['item']['page_num']
        page_num = page_num + 20
        searchword=response.meta['item']['search_word']
        datas = json.loads(response.body.decode())['list']
        for data in datas:
            item = DianpingShopItem()
            item["city_name"] = response.meta['item']['city_name']
            item["city_id"] = response.meta['item']['city_id']
            item["branchName"] = data['branchName']
            item["categoryId"] = data['categoryId']
            item["categoryName"] = data['categoryName']
            item["cityId"] = data['cityId']
            item["shop_id"] = data['id']
            item["matchText"] = data['matchText']
            item["name"] = data['name']
            item["priceText"] = re.sub('[^0-9]+,', '', data['priceText'])
            item["regionName"] = data['regionName']
            item["reviewCount"] = data['reviewCount']
            item["scoreText"] = data['scoreText']
            item["shopPower"] = data['shopPower']
            item["shopType"] = data['shopType']
            item["name"] = data['name']
            item['searchword']=searchword
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 61; Win64; x64) %s AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' %response.meta['item']['city_id'],
            }
            url = 'https://m.dianping.com/shop/%s' % item['shop_id']
            yield scrapy.Request(url, headers=header, callback=self.goto_shop, dont_filter=True, meta=
            {'item': item,'cookiejar':response.meta['cookiejar']})
        if len(datas) >= 20:
            url = 'https://mapi.dianping.com/searchshop.json?start=%s&' \
                  'categoryid=0&parentCategoryId=0&limit=20&' \
                  'sortid=0&cityid=%s&keyword=%s&regionid=0&maptype=0' % (
                  page_num, response.meta['item']['city_id'], searchword)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'mapi.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3239.132 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta=
            {'item': {'city_name': response.meta['item']['city_name'], 'pinyin': response.meta['item']['pinyin'],
                      'city_id': response.meta['item']['city_id'], 'page_num': page_num,'search_word':searchword},'cookiejar':response.meta['cookiejar']})

    def goto_shop(self, response):
        item = response.meta['item']
        item['shop_address'] = ''.join(
            response.xpath('//div[@class="J_address"]//a[@class="item"]//text()').extract()).strip()
        item['phone'] = ''.join(response.xpath('//a[@class="item "]//text()').extract()).strip()
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item
        deals = response.css('.tuan-list a')
        for deal in deals:
            deal_item = DianpingDealItem()
            deal_item['title'] = deal.css('.newtitle::text').extract()[0]
            deal_item['shop_id'] = item['shop_id']
            deal_item['price'] = deal.css('.price::text').extract()[0]
            deal_item['oldprice'] = re.sub('[^0-9]+', '', deal.css('.o-price::text').extract()[0])
            deal_item['soldNum'] = re.sub('[^0-9]+', '', deal.css('.soldNum::text').extract()[0])
            deal_item['deal_id'] = re.search("dealgrp_id:.+'", deal.css('::attr("onclick")').extract()[0]) \
                .group().split(':')[-1].strip("'")
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }
            url = 'https://m.dianping.com/tuan/deal/' + deal_item['deal_id']
            yield scrapy.Request(url, headers=header, callback=self.goto_deal, dont_filter=True, meta=
            {'item': deal_item,'cookiejar':response.meta['cookiejar']})

    def goto_deal(self, response):
        item = response.meta['item']
        item['desc'] = response.css('.cont p::text').extract()[0]
        item['type'] = re.sub('\s', '', '|'.join(response.xpath('//ul["advantage "]/li//text()').extract()))
        item['detail'] = re.sub('\s', '',
                                ''.join(response.xpath('//div[contains(@class,"group-detail")]/div//text()').extract()))
        item['buy_know'] = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
            '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
        buy_know = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
            '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
        buy_know = buy_know.split('|')
        if '有效期' in buy_know:
            buy_know = buy_know[buy_know.index('有效期') + 1].split('至')
            item['start_time'] = buy_know[0]
            item['end_time'] = buy_know[1]
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item








    
    
    
    
    