# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import time
import traceback
from meituan_pet_server.items import MeituanPetHospitalshopItem
from meituan_pet_server.items import MeituanPetAppdealIdItem
from meituan_pet_server.items import Meituan_to_Dp_Item
import sqlalchemy
import json


class PetHospitalFromLogSpider(scrapy.Spider):
    name = "pet_hospital_from_log"
    allowed_domains = ["www.meituan.com", "i.meituan.com"]

    def start_requests(self):
        conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                        connect_args={'charset': 'utf8'})
        cur = conn.connect()
        temps = cur.execute(
            'SELECT * FROM hillinsight.tuangou_pet_hospital_err where DATE(`dt`)=DATE(now());')  # where `dt`=DATE(now())
        temps = temps.fetchall()
        for i, temp in enumerate(temps):
            tmp = {}
            for key in temp.keys():
                tmp[key] = temp[key]
            temp = tmp
            if temp['kind'] == '1':
                url = temp['url']
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Host': temp['host'],
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                }
                temp['timerequest'] = 0
                yield scrapy.Request(url, headers=header, meta={'cookiejar': i, 'item': temp},
                                     callback=self.get_shop_item, dont_filter=True, errback=self.error_callback)
            else:
                if temp['url'].split('/')[-2][0] == 'c':
                    if temp['type'] == '/':
                        header = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Cache-Control': 'max-age=0',
                            'Host': temp['host'],
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        }
                        yield scrapy.Request(temp['url'], headers=header, meta={'cookiejar': i, 'item': temp},
                                             callback=self.get_district, dont_filter=True, errback=self.error_callback)
                    else:
                        header = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Cache-Control': 'max-age=0',
                            'Host': temp['host'],
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        }
                        yield scrapy.Request(temp['url'], headers=header, meta={'cookiejar': i, 'item': temp},
                                             callback=self.get_first_page, dont_filter=True,
                                             errback=self.error_callback)

    def get_shop_item(self, response):
        if response.status == 500:
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
            yield item
            url = 'https://i.meituan.com/'
            yield scrapy.Request(url, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            }, callback=self.get_app_deal_info, errback=self.error_callback,
                                 meta={'item': item, 'cookiejar': 'get_deal_id' + item['mtshop_id']},
                                 dont_filter=True)

    def error_callback(self, failure):
        request = failure.request
        if 'timerequest' not in request.meta.keys():
            request.meta['timerequest'] = 0
        request.meta['timerequest'] += 1
        if request.meta['timerequest'] > 100:
            self.logger.error('finally retrytime out %s', request.url)
            return
        yield request

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
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            yield scrapy.Request(url, headers=header, meta={"timerequest": 0, 'cookiejar': response.meta['cookiejar'],
                                                            'item': {'city_name': response.meta['item']['city_name'],
                                                                     'type': type,
                                                                     'host': response.meta['item']['host']}},
                                 callback=self.get_district,
                                 dont_filter=True, errback=self.error_callback)
            break

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
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            }

            url = response.url + 'pn%s' % i
            yield scrapy.Request(url, headers=header,
                                 meta={"timerequest": 0, 'cookiejar': response.meta['cookiejar'],
                                       'item': {'city_name': response.meta['item']['city_name'],
                                                'type': response.meta['item']['type'],
                                                'distract': response.meta['item']['distract'],
                                                'host': response.meta['item']['host']}
                                       },
                                 callback=self.get_shop_item,
                                 dont_filter=True, errback=self.error_callback)

    def get_app_deal_info(self, response):
        url = 'https://i.meituan.com/poi/%s' % response.meta['item']['mtshop_id']
        yield scrapy.Request(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }, callback=self.goto_shop_item, errback=self.error_callback, meta={'cookiejar': response.meta['cookiejar'],
                                                                            'item': {'shop_id': response.meta['item'][
                                                                                'mtshop_id']}},
                             dont_filter=True)

    def goto_shop_item(self, response):
        if response.status == 500:
            return
        datas = response.xpath('//body/dl[@class="list"]//dd//dd')
        for data in datas:
            item = MeituanPetAppdealIdItem()
            item['shop_id'] = response.meta['item']['shop_id']
            item['deal_id'] = data.css('a::attr("href")').extract()[0]
            item['deal_id'] = item['deal_id'].split('/')[-1].split('.')[0]
            item['title'] = data.css('a::attr("title")').extract()[0]
            item['price'] = re.sub('[^0-9]+', '', data.css('.price .strong::text').extract()[0])
            try:
                item['old_price'] = re.sub('[^0-9]+', '', data.css('del::text').extract()[0])
            except Exception as e:
                item['old_price'] = 0
            item['text'] = data.css('.title::text').extract()[0]
            item['sale'] = re.sub('[^0-9]+', '', data.css('.statusInfo::text').extract()[0])
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            yield item
            deal_id, shop_id = item['deal_id'], item['shop_id']
            url = 'https://i.meituan.com/general/platform/mttgdetail/mtdealbasegn.json?dealid=%s&shopid=%s&eventpromochannel=&stid=' % (
            deal_id, shop_id)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.get_item, errback=self.error_callback,
                                 meta={'cookiejar': 'get_meituan' + item['deal_id']},
                                 dont_filter=True)

    def get_item(self, response):
        if response.status == 500:
            return
        item = Meituan_to_Dp_Item()
        temps = json.loads(response.body)
        item['mtdealid'] = temps['mtDealGroupId']
        item['brandName'] = temps['brandName']
        item['solds'] = temps['solds']
        item['start_time'] = time.strftime("%Y-%m-%d", time.strptime(temps['start'], "%b %d, %Y %H:%M:%S %p"))
        item['end_time'] = time.strftime("%Y-%m-%d", time.strptime(temps['end'], "%b %d, %Y %H:%M:%S %p"))
        item['originalPrice'] = temps['originalPrice']
        item['title'] = temps['title']
        item['coupontitle'] = temps['coupontitle']
        item['price'] = temps['price']
        item['orderTitle'] = temps['orderTitle']
        item['dpDealGroupId'] = temps['dpDealGroupId']
        item['shop_id'] = temps['shop']['poiid']
        item['shop_name'] = temps['shop']['name']
        item['phone'] = temps['shop']['phone']
        item['addr'] = temps['shop']['addr']
        item['avgscore'] = temps['shop']['avgscore']
        item['dpShopId'] = temps['shop']['dpShopId']
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
        yield item
