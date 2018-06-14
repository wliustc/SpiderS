# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import sqlalchemy
import json
from meituan_pet_server.items import MeituanPetHospitalItem
import time
class PetHospitalDealSpider(scrapy.Spider):
    name = "pet_hospital_deal"
    allowed_domains = ["www.meituan.com"]

    def start_requests(self):
        conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                        connect_args={'charset': 'utf8'})
        cur=conn.connect()
        temp=cur.execute('SELECT `mtshop_id`,`host` FROM tuangou_meituan_shop_info where `dt`=DATE(now());')
        temp=temp.fetchall()
        for tmp in temp:
            url='http://www.meituan.com/chongwu/%s/' %tmp[0]
            yield scrapy.Request(url, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            },
             meta={'item': {'shop_id': tmp[0],
                            'host':tmp[1]}},
             callback=self.get_shop_list,
             dont_filter=True)


    def get_shop_list(self, response):
        script = response.xpath('//body/script[1]/text()').extract()[0]
        script = re.search('{(.*[ \t\n\r\f]*)+', script)
        script = script.group().strip(';')
        script = json.loads(script)
        temps = script['groupDealList']['group']
        for temp in temps:
            item = MeituanPetHospitalItem()
            item['mtdeal_id'] = temp['id']
            item['deal_detail'] = temp['shortTips']
            item['price'] = temp['price']
            item['old_price'] = temp['value']
            item['sold'] = temp['sold']
            item['mtshop_id'] = response.meta['item']['shop_id']
            url = 'http://' + response.meta['item']['host'] + '/deal/%s.html' % item['mtdeal_id']
            yield scrapy.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
                                 meta={'item': {'item': item}},
                                 callback=self.get_shop_item, dont_filter=True)

    def get_shop_item(self, response):
        item = response.meta['item']['item']
        try:
            item['score'] = response.css('.deal-component-rating-stars::text').extract()[0]
        except Exception as e:
            item['score'] = None
        try:
            item['pingjia_num'] = response.css('.deal-component-rating-comment-count::text').extract()[0]
        except Exception as e:
            item['pingjia_num'] = None
        deal_detail = item['deal_detail']
        temp = re.findall(u'有效期.+', deal_detail)[0]
        temp = temp.split('：')[1].split(u'至')
        item['start_time'] = re.sub('\.', '-', temp[0]).strip()
        item['end_time'] = re.sub('\.', '-', temp[1]).strip()
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
        item['title'] = response.css(".sans-serif span::text").extract()[0] + \
                        response.css(".sans-serif h1::text").extract()[0]
        item['describe'] = response.css('.deal-component-description::text').extract()[0]
        yield item

    
    