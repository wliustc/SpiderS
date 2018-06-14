# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
import sys
from ..items import DianpingShopItem
from ..items import DianpingDealItem
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

brand = ['良品铺子','索味','魔呀','戴永红','王小贱','小嘴零食','自然派','来伊份','小口大口',
         '座上客','零食工坊','老婆大人','星巴克','面包新语','85度c','仟吉','巴黎贝甜','罗莎蛋糕',
         '好利来','多乐之日','酵墅','克里斯汀','皇冠蛋糕','可莎蜜儿','塞拉维','米旗','超港烘焙',
         '礼颂','肯德基','麦当劳','汉堡王','德克士','周黑鸭','廖记棒棒鸡','喜茶','奈雪的茶','卡旺卡']
class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["m.dianping.com"]
    start_urls = ['http://m.dianping.com/']

    def start_requests(self):
        sql = '''select DISTINCT city_name,city_id from t_spider_dianping_city limit 1'''
        for i in db.query(sql):
            city_name = i.get('city_name')
            city_id = i.get('city_id')
            pinyin = i.get('pinyin')
            for brands in brand:
                url = 'https://mapi.dianping.com/searchshop.json?start=%s&' \
                      'categoryid=0&parentCategoryId=0&limit=20&' \
                      'sortid=0&cityid=%s&keyword=%s&regionid=0&maptype=0' % (0, city_id, brands)
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
                {'item': {'city_name': city_name, 'pinyin': pinyin,
                          'city_id': city_id, 'page_num': 0},
                 'cookiejar': city_id,'brands':brands})


    def get_item(self, response):
        page_num = response.meta['item']['page_num']
        page_num = page_num + 20
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
            item['brand'] = response.meta['brands']
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
            brands = response.meta['brands']
            url = 'https://mapi.dianping.com/searchshop.json?start=%s&' \
                  'categoryid=0&parentCategoryId=0&limit=20&' \
                  'sortid=0&cityid=%s&keyword=%s&regionid=0&maptype=0' % (
                  page_num, response.meta['item']['city_id'], brands)
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
                      'city_id': response.meta['item']['city_id'], 'page_num': page_num},'cookiejar':response.meta['cookiejar'],'brands':brands})

    def goto_shop(self, response):
        item = response.meta['item']
        item['shop_address'] = ''.join(
            response.xpath('//div[@class="J_address"]//a[@class="item"]//text()').extract()).strip()
        item['phone'] = ''.join(response.xpath('//a[@class="item "]//text()').extract()).strip()
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield item




    #团购劵数据抓取
    #     deals = response.css('.tuan-list a')
    #     for deal in deals:
    #         deal_item = DianpingDealItem()
    #         deal_item['title'] = deal.css('.newtitle::text').extract()[0]
    #         deal_item['shop_id'] = item['shop_id']
    #         deal_item['price'] = deal.css('.price::text').extract()[0]
    #         deal_item['oldprice'] = re.sub('[^0-9]+', '', deal.css('.o-price::text').extract()[0])
    #         deal_item['soldNum'] = re.sub('[^0-9]+', '', deal.css('.soldNum::text').extract()[0])
    #         deal_item['deal_id'] = re.search("dealgrp_id:.+'", deal.css('::attr("onclick")').extract()[0]) \
    #             .group().split(':')[-1].strip("'")
    #         header = {
    #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #             'Accept-Encoding': 'gzip, deflate, br',
    #             'Accept-Language': 'zh-CN,zh;q=0.8',
    #             'Cache-Control': 'max-age=0',
    #             'Host': 'm.dianping.com',
    #             'Upgrade-Insecure-Requests': '1',
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    #         }
    #         url = 'https://m.dianping.com/tuan/deal/' + deal_item['deal_id']
    #         yield scrapy.Request(url, headers=header, callback=self.goto_deal, dont_filter=True, meta=
    #         {'item': deal_item,'cookiejar':response.meta['cookiejar']})
    #
    # def goto_deal(self, response):
    #     item = response.meta['item']
    #     item['desc'] = response.css('.cont p::text').extract()[0]
    #     item['type'] = re.sub('\s', '', '|'.join(response.xpath('//ul["advantage "]/li//text()').extract()))
    #     item['detail'] = re.sub('\s', '',
    #                             ''.join(response.xpath('//div[contains(@class,"group-detail")]/div//text()').extract()))
    #     item['buy_know'] = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
    #         '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
    #     buy_know = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
    #         '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
    #     buy_know = buy_know.split('|')
    #     if '有效期' in buy_know:
    #         buy_know = buy_know[buy_know.index('有效期') + 1].split('至')
    #         item['start_time'] = buy_know[0]
    #         item['end_time'] = buy_know[1]
    #     item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    #     yield item








    
    