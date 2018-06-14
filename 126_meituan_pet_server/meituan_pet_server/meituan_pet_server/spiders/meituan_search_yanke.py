# -*- coding: utf-8 -*-
from meituan_pet_server.items import MeituanPetAppyankeItem
import scrapy
import json
import time
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class MeituanSearchYankeSpider(scrapy.Spider):
    name = "meituan_search_yanke"
    allowed_domains = ["www.meituan.com"]
    start_urls = ['http://www.meituan.com/']


    def start_requests(self):
        url = 'https://i.meituan.com/index/changecity'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_index_url, dont_filter=True)


    

    def get_index_url(self, response):
        url = 'https://i.meituan.com/index/changecity'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_city_id, dont_filter=True)


    def get_city_id(self, response):
        city_list = response.xpath('//div[@class="abc"]/ul/li/a')
        for i, city in enumerate(city_list):
            city_pinyin = city.css('::attr("href")').extract()[0].split('/')[3]
            url = city.css('::attr("href")').extract()[0]
            if city_pinyin != 'index':
                continue
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            url = 'https:' + url
            yield scrapy.Request(url, headers=header, callback=self.get_city_id_detail, dont_filter=True)


    def get_city_id_detail(self, response):
        temps = response.xpath('//div[@class="wrapper"]//li/a')
        for temp in temps:
            pinyin = temp.css('::attr("data-citypinyin")').extract()[0]
            city_name = temp.css('::text').extract()[0]
            url = 'https://i.meituan.com/%s/all/?cid=20693&cateType=poi' % pinyin
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.get_cateid, dont_filter=True, meta={'item':{'city_name': city_name,'pinyin': pinyin}})


    def get_cateid(self, response):
        cityid = response.xpath('//body/script[4]/text()').extract()[0]
        cityid = re.search('GLOBAL_cityId:.+', cityid).group()
        cityid = int(cityid.split(': ')[-1].strip("',"))
        temps = response.xpath('//script[@id="filterData"]/text()').extract()[0]
        temps = json.loads(temps)
        brand_list = ['眼科','爱尔眼科', '普瑞', '新视界', '光明', '何氏', '林顺潮', '华厦', '同仁', '东南', '爱瑞阳光', '尖峰眼科' ]
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        for s in brand_list:
            url_base = 'https://i.meituan.com/s/a?cid=-1&bid=-1&sid=defaults&p=%s&ciid=%s&bizType=area&csp=&nocount=true&stid_b=_b2&w=%s'
            url = url_base % (0, cityid, s)
            yield scrapy.Request(url, headers=header, callback=self.get_shop_url, dont_filter=True, meta={'item':{'city_name':response.meta['item']['city_name'],
                                                     'type': s,'url_base': url_base,'area_id': id,'cityid': cityid},'page_num': 0,'base_url': url_base})


    def get_shop_url(self, response):
        urls = response.css('.poi-list-item a.react::attr("href")').extract()
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        for url in urls:
            url = 'https:' + url
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True, meta={'item':{'city_name':response.meta['item']['city_name'],
                                                                            'type':response.meta['item']['type'],'area_id':response.meta['item']['area_id'],
                                                                            'cityid':response.meta['item']['cityid']}})
        if len(urls) < 20:
            pass
        else:
            cityid = response.meta['item']['cityid']
            s = response.meta['item']['type']
            page_num = response.meta['page_num'] + 1
            url_base = 'https://i.meituan.com/s/a?cid=-1&bid=-1&sid=defaults&p=%s&ciid=%s&bizType=area&csp=&nocount=true&stid_b=_b2&w=%s'
            url = url_base % (page_num, cityid, s)
            yield scrapy.Request(url, headers=header, callback=self.get_shop_url, dont_filter=True, meta={'item':{'city_name':response.meta['item']['city_name'],
                                                                                    'type': s,'area_id': id,'cityid':response.meta['item']['cityid']},
                                                                                    'page_num': page_num,'base_url': url_base})


    def get_item(self, response):
        item = MeituanPetAppyankeItem()
        try:
            item['shop_id'] = response.xpath('//div[@class="poi-banner"]/input[1]/@value').extract()[0]
        except Exception as e:
            self.logger.error('meituan page error in page %s ' % response.url)
            return
        detail = json.loads(response.xpath('//div[@id="poi-detail"]/@data-params').extract()[0])
        item['shop_name'] = detail['poi_shopname']
        item['category1_id'] = detail['categoryIds'][0]
        item['category2_id'] = detail['categoryIds'][1]
        item['city_id'] = response.meta['item']['cityid']
        item['city_name'] = response.meta['item']['city_name']
        item['address'] = response.xpath('//div[@class="kv-line-r"]//a[1]/div/text()').extract()[0]
        item['lng'] = detail['poi_lng']
        item['lat'] = detail['poi_lat']
        item['avg_price'] = response.xpath('//div[@class="rating"]/span[2]/text()').extract()[0].split('：')[-1].strip('¥')
        item['phone_no'] = response.xpath('//div[@class="kv-line-r"]/p/a/@data-tele').extract()[0]
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        try:
            item['avgscore'] = response.xpath('//span[@class="stars"]/em/text()').extract()[0]
        except Exception as e:
            item['avgscore'] = None
        try:
            item['comments_num'] = response.xpath('//span[@class="pull-right"]/text()').extract()[0]
        except Exception as e:
            item['comments_num'] = None
        item['brand'] = response.meta['item']['type']
        yield item

    
    
    
    
    
    
    
    