# -*- coding: utf-8 -*-
import scrapy
import scrapy
import json
import time
import re
from ..items import DianpingShopItem
import random
from ..items import DianpingDealItem
import web
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.selector import Selector
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='localhost')
user_agent=[
    'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 520) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.11082',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/20100625 Firefox/3.6.7',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.78 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 6680.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.74 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.22.79_10013310) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true',
]
class DianpingGroupSpider(scrapy.Spider):
    name = "DianPing_group"
    allowed_domains = ["m.dianping.com"]
    start_urls = ['http://m.dianping.com/']
    handle_httpstatus_list = [302,403]

    def start_requests(self):
        url = 'https://m.dianping.com/'
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
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

            driver = webdriver.PhantomJS()
            driver.get(url)
            time.sleep(1)
            cookie=[]
            cooke_dict = driver.get_cookies()
            driver.close()
            # 字典化cookie
            for i in cooke_dict:
                cookie.append({'name': i["name"], 'value': i["value"],
                             'domain': '.dianping.com'})
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request('https://m.dianping.com/allcategory' ,cookies=cookie,headers=header,
                                 callback=self.goto_city, dont_filter=True, meta=
            {'item': {'city_name': city_name, 'pinyin': pinyin, 'city_id': city_id}, 'cookiejar': city_id})




    def goto_city(self, response):
        temp=response.xpath('//a[contains(text(), "宠物医院")]/@href').extract()[0]
        temp='https://m.dianping.com'+temp
        url ='https://mapi.dianping.com/searchshop.json?start=%s&categoryid=95&parentCategoryId=95&locatecityid=%s&limit=20&sortid=0&cityid=%s&regionid=0&maptype=0' % (
            0, response.meta['item']['city_id'],response.meta['item']['city_id'] )
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'mapi.dianping.com',
            'Referer':temp ,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }

        yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta=
        {'item': {'city_name': response.meta['item']['city_name'], 'pinyin': response.meta['item']['pinyin'],
                  'city_id': response.meta['item']['city_id'], 'page_num': 0},'base_url':temp, 'cookiejar': response.meta['cookiejar']})


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
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Host': 'm.dianping.com',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'Referer': response.meta['base_url'],
                'User-Agent': user_agent[int(response.meta['item']['city_id']) % len(user_agent)]
            }
            header['Referer']=response.url
            url = 'https://m.dianping.com/shop/%s' % item['shop_id']
            yield scrapy.Request(url, headers=header, callback=self.goto_shop, dont_filter=True, meta=
            {'item': item, 'cookiejar': response.meta['cookiejar']})
        if len(datas) >= 20:
            url = 'https://mapi.dianping.com/searchshop.json?start=%s&categoryid=95&parentCategoryId=95&locatecityid=%s&limit=20&sortid=0&cityid=%s&regionid=0&maptype=0' % (
            page_num, response.meta['item']['city_id'], response.meta['item']['city_id'])
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
                      'city_id': response.meta['item']['city_id'], 'page_num': page_num},
             'cookiejar': response.meta['cookiejar']})


    def goto_shop(self, response):
        # print(response.body.decode())
        if 'debug_flag' in response.meta:
            if not response.body.decode() and response.meta['debug_flag'] > 3:
                self.logger.error(response.meta['item']['shop_id'])
                return
        if (response.status in [302,403]) or (not response.body.decode()):
            if 'debug_flag' in response.meta:
                debug_flag = response.meta['debug_flag'] + 1
            else:
                debug_flag = 1
            if response.status in [302,403]:
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Host': 'm.dianping.com',
                    'Pragma': 'no-cache',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': user_agent[random.randint(0, len(user_agent) - 1)]
                }
                yield scrapy.Request('https://m.dianping.com/', headers=header, callback=self.shop_verify_avoid,
                                     dont_filter=True, meta=
                                     {'source_url': response.request.url, 'item': response.meta['item'],
                                      'cookiejar': response.meta['cookiejar'] + str(response.meta['item']['shop_id']),
                                      'debug_flag': debug_flag})
                return
        item = response.meta['item']
        item['shop_address'] = ''.join(
            response.xpath('//div[@class="J_address"]//a[@class="item"]//text()').extract()).strip()
        item['phone'] = ''.join(response.xpath('//a[@class="item "]//text()').extract()).strip()
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # yield item
        deals = response.css('.tuan-list a')
        print(deals)
        for deal in deals:
            deal_item = DianpingDealItem()
            deal_item['description'] = deal.css('.newtitle::text').extract()[0]
            deal_item['shop_id'] = str(item['shop_id'])
            deal_item['title'] = item['name']
            deal_item['city_name'] = item['city_name']
            deal_item['city_id'] = item['city_id']
            deal_item['new_price'] = deal.css('.price::text').extract()[0]
            deal_item['old_price'] = re.sub('[^0-9]+', '', deal.css('.o-price::text').extract()[0])
            deal_item['sales'] = re.sub('[^0-9]+', '', deal.css('.soldNum::text').extract()[0])
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
            {'item': deal_item, 'cookiejar': response.meta['cookiejar']})

    def goto_deal(self, response):
        item = response.meta['item']
        item['category'] = '宠物服务'
        # item['desc'] = response.css('.cont p::text').extract()[0]
        # item['type'] = re.sub('\s', '', '|'.join(response.xpath('//ul["advantage "]/li//text()').extract()))
        item['description'] = item['description'] + re.sub('\s', '',
                                ''.join(response.xpath('//div[contains(@class,"group-detail")]/div//text()').extract()))
        # item['buy_know'] = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
        #     '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
        buy_know = re.sub('\|+', '|', re.sub('\s', '', '|'.join(response.xpath(
            '//div[contains(@class,"buy-know")]//div[@class="purchase-notes"]//text()').extract()))).strip('|')
        buy_know = buy_know.split('|')
        if '有效期' in buy_know:
            buy_know = buy_know[buy_know.index('有效期') + 1].split('至')
            item['start_time'] = buy_know[0]
            item['end_time'] = buy_know[1]
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #item['tag'] = 'group'
        print(item)
        yield item

    def shop_verify_avoid(self,response):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'm.dianping.com',
            'Referer': 'https://m.dianping.com/',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent[random.randint(0,len(user_agent)-1)]
        }
        yield scrapy.Request(response.meta['source_url'], headers=header, callback=self.goto_shop,
                             dont_filter=True, meta=
                             {'item': response.meta['item'],
                              'cookiejar': response.meta['cookiejar'],
                              'debug_flag': response.meta['debug_flag']})