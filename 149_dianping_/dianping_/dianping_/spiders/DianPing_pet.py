# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from ..items import DianpingShopItem
import random
# from ..items import DianpingDealItem
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

star_dict = {10:'1',20:'2',30:'3',40:'4',50:'5',15:'1.5',25:'2.5',35:'3.5',45:'4.5'}
user_agent = [
    'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 520) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F5027d Safari/600.1.4',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/20100625 Firefox/3.6.7',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Mobile; rv:18.0) Gecko/18.0 Firefox/18.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 6680.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.74 Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.0.22.79_10013310) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true',
]
class DianpingGroupSpider(scrapy.Spider):
    name = 'DianPing_pet'
    allowed_domains = ['dianping.com']
    start_urls = ['http://dianping.com/']
    handle_httpstatus_list = [302]
    
    def start_requests(self):
        sql = '''select DISTINCT city_name,city_id from t_spider_dianping_city '''
        for i in db.query(sql):
            city_name = i.get('city_name')
            city_id = i.get('city_id')
            pinyin = i.get('pinyin')
            url = 'https://mapi.dianping.com/searchshop.json?start=%s&categoryid=95&parentCategoryId=95&locatecityid=%s&limit=20&sortid=0&cityid=%s&regionid=0&maptype=0' % (
                0, city_id, city_id)
            header = {
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Host':'mapi.dianping.com',
                'Pragma':'no-cache',
                'Referer':'https://m.dianping.com',
                'User-Agent': user_agent[random.randint(0,len(user_agent)-1)]
            }
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta=
            {'item': {'city_name': city_name,'city_id': int(city_id), 'page_num': 0,'pinyin':pinyin},'cookiejar': city_id})

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
            {'item': {'city_name': city_name, 'pinyin': pinyin, 'city_id': city_id}, 'cookiejar': city_id})


    def goto_city(self, response):
        url ='https://mapi.dianping.com/searchshop.json?start=%s&categoryid=95&parentCategoryId=95&locatecityid=%s&limit=20&sortid=0&cityid=%s&regionid=0&maptype=0' % (
            0, response.meta['item']['city_id'],response.meta['item']['city_id'] )
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
                  'city_id': response.meta['item']['city_id'], 'page_num': 0}, 'cookiejar': response.meta['cookiejar']})


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
            # if item['shopPower'] in star_dict:
            #     item['shopPower'] = star_dict[item['shopPower']]
            item["shopType"] = data['shopType']
            item["name"] = data['name']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'm.dianping.com',
                'Referer': 'https://m.dianping.com/',
                'Upgrade-Insecure-Requests': '1',
				'User-Agent': user_agent[random.randint(0,len(user_agent)-1)],
            }

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
               'User-Agent': user_agent[random.randint(0,len(user_agent)-1)]
            }
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta=
            {'item': {'city_name': response.meta['item']['city_name'], 'pinyin': response.meta['item']['pinyin'],
                      'city_id': response.meta['item']['city_id'], 'page_num': page_num},
             'cookiejar': response.meta['cookiejar']})

    def goto_shop(self, response):
        if 'debug_flag' in response.meta:
            if not response.body.decode() and response.meta['debug_flag']>3:
                self.logger.error(response.meta['item']['shop_id'])
                return
        if response.status==302 or (not response.body.decode()):
            if 'debug_flag' in response.meta:
                debug_flag=response.meta['debug_flag']+1
            else:
                debug_flag=1
            if response.status==302:
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Host': 'm.dianping.com',
                    'Pragma': 'no-cache',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
                }
                yield scrapy.Request('https://m.dianping.com/', headers=header, callback=self.shop_verify_avoid, dont_filter=True, meta=
                {'source_url':response.request.url,'item': response.meta['item'], 'cookiejar': response.meta['cookiejar']+str(response.meta['item']['shop_id']),'debug_flag':debug_flag})
                return
            
        cookiejar = response.meta['cookiejar']
        item = response.meta['item']
        item['shop_address'] = ''.join(
            response.xpath('//div[@class="J_address"]//a[@class="item"]//text()').extract()).strip()
        item['phone'] = ''.join(response.xpath('//a[@class="item "]//text()').extract()).strip()
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        shop_id = item['shop_id']
        url = 'https://m.dianping.com/shop/{}/map'.format(shop_id)
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'm.dianping.com',
            'Upgrade-Insecure-Requests': '1',
        	'User-Agent': user_agent[random.randint(0,len(user_agent)-1)],
            'Origin':'https://m.dianping.com',
            'Referer':'https://m.dianping.com/shop/{}/map'.format(shop_id),
            'Content-Type':'application/json'
        }
        yield scrapy.Request(url,meta={'item':item,'cookiejar':cookiejar},dont_filter=True,headers=header,callback=self.coordinates_parse)


    def coordinates_parse(self,response):
        html = response.body
        coor = re.findall('"shopLat":(.*?),"shopLng":(.*?),', html, re.S)
        if coor:
            shop_lat,shop_lng = coor[0]
        item = response.meta['item']

        item['shop_lat'] = shop_lat
        item['shop_lng'] = shop_lng
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        yield scrapy.Request(response.meta['source_url'], headers=header, callback=self.goto_shop,
                             dont_filter=True, meta=
                             {'item': response.meta['item'],
                              'cookiejar': response.meta['cookiejar'],
                              'debug_flag': response.meta['debug_flag']})
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    