# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import json
import time
import re
from meituan_pet_server.items import MeituanPetHospitalshopItem

class MeituanAppHospitalSpider(scrapy.Spider):
    name = "meituan_app_hospital"
    allowed_domains = ["i.meituan.com"]
    start_urls = ['http://i.meituan.com/']

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
        yield scrapy.Request(url, headers=header, callback=self.get_index_url,dont_filter=True)

    def get_index_url(self,response):
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
        yield scrapy.Request(url, headers=header, callback=self.get_city_id,dont_filter=True)

    def get_city_id(self,response):
        city_list=response.xpath('//div[@class="abc"]/ul/li/a')
        for i,city in enumerate(city_list):
            city_pinyin=city.css('::attr("href")').extract()[0].split('/')[3]
            url=city.css('::attr("href")').extract()[0]
            if city_pinyin!='index':
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
            url='https:'+url
            yield scrapy.Request(url, headers=header, callback=self.get_city_id_detail, dont_filter=True)

    def get_city_id_detail(self, response):
        temps=response.xpath('//div[@class="wrapper"]//li/a')
        for temp in temps:
            pinyin=temp.css('::attr("data-citypinyin")').extract()[0]
            city_name=temp.css('::text').extract()[0]
            url='https://i.meituan.com/%s/all/?cid=20693&cateType=poi' %pinyin
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, callback=self.get_cateid, dont_filter=True,meta={'item':
                                                                        {'city_name':city_name}})

    def get_cateid(self,response):
        cityid = response.body.decode()
        cityid=re.search('GLOBAL_cityId:.+',cityid).group()
        cityid=int(cityid.split(': ')[-1].strip("',"))
        temps=response.xpath('//script[@id="filterData"]/text()').extract()[0]
        temps=json.loads(temps)
        area_list=temps['BizAreaList']
        for area in area_list:
            id=area['id']
            if id==-1:
                continue
            district=area['name']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'api.mobile.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            url_base= 'http://api.mobile.meituan.com/group/v4/poi/pcsearch/%s?limit=32&offset=%s&cateId=20691&areaId=%s'
            url = url_base% (cityid,0,id)  # 宠物医院
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True,meta={'item':
                                                                        {'city_name':response.meta['item']['city_name'],
                                                                         'district':district,
                                                                         'type':'宠物医院','url_base':url_base,
                                                                         'area_id': id,'cityid':cityid}})
            url_base_2='http://api.mobile.meituan.com/group/v4/poi/pcsearch/%s?limit=32&offset=%s&cateId=20692&areaId=%s'
            url_2 = url_base_2 % (cityid,0,id)  # 宠物店
            yield scrapy.Request(url_2, headers=header, callback=self.get_item, dont_filter=True,meta={'item':
                                                                        {'city_name':response.meta['item']['city_name'],
                                                                         'district':district,
                                                                         'type':'宠物店','url_base':url_base_2,
                                                                         'area_id':id,'cityid':cityid}})
    def get_item(self,response):
        temp=json.loads(response.body.decode())
        data_his=response.meta['item']
        cityid=response.meta['item']['cityid']
        if 'count' not in data_his:
            count=int(temp['data']['totalCount'])
        else:
            count=data_his['count']
        if 'count_now' not in data_his:
            count_now=0
        else:
            count_now=data_his['count_now']
        if count==0:
            return
        for tmp in temp['data']['searchResult']:
            item=MeituanPetHospitalshopItem()
            item['address']=tmp['address']
            item['mtshop_name'] = tmp['title']
            item['shop_url'] ='http://www.meituan.com/chongwu/%s/' %tmp['id']
            item['mtshop_id'] = tmp['id']
            item['score'] = tmp['avgscore']
            item['pinglun_num'] = tmp['comments']
            item['shop_sale_num'] = ''
            item['dist'] = tmp['areaname']
            item['avg_price'] = tmp['avgprice']
            item['host'] = ''
            item['city_name'] = response.meta['item']['city_name']
            item['type'] = response.meta['item']['type']
            item['distract'] = response.meta['item']['district']
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            yield item
        count_now+=32
        if count_now<count:
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'api.mobile.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }

            url = response.meta['item']['url_base'] % (cityid,count_now, response.meta['item']['area_id'])
            yield scrapy.Request(url, headers=header, callback=self.get_item, dont_filter=True,meta={'item':
                                                                        {'city_name':response.meta['item']['city_name'],
                                                                         'district':response.meta['item']['district'],
                                                                         'type':response.meta['item']['type'],
                                                                         'url_base':response.meta['item']['url_base'],
                                                                         'area_id': response.meta['item']['area_id'],
                                                                         'count':count,'count_now':count_now,
                                                                         'cityid':cityid}})

    
    
    