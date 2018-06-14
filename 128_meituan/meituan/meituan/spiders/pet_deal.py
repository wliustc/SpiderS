# -*- coding: utf-8 -*-
import json

import scrapy
import web
from scrapy import Request
import re
from meituan.items import MeituanItem

header = {
    'Host': 'i.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

db = web.database(dbn='mysql', db='travel', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class PetDealSpider(scrapy.Spider):
    name = "pet_deal"
    allowed_domains = ["meituan.com"]
    start_urls = ['http://meituan.com/']

    def start_requests(self):
        data = db.query('select city_pinyin from travel.t_meituan_citylist;')
        for d in data:
            city_pinyin = d.get('city_pinyin')
            url = 'http://i.meituan.com/%s?cid=20691&sid=start&cateType=poi&p=1' % city_pinyin
            yield Request(url, callback=self.parse_shops_deals, headers=header, dont_filter=True)
            # yield Request(url='https://i.meituan.com/general/platform/mttgdetail/mtdealbasegn.json?dealid=42774143',
            #               callback=self.parse_deal, headers=header)

    def parse_shops_deals(self, response):
        content = response.body
        shop_id_list = re.findall('data-href="//i.meituan.com/poi/(\d+)', content)
        print shop_id_list
        if shop_id_list:
            for shop_id in shop_id_list:
                shop_url = 'http://i.meituan.com/poi/%s' % shop_id
                yield Request(shop_url, callback=self.parse_shop, dont_filter=True, headers=header)
                comment_url = 'http://www.meituan.com/ptapi/poi/getcomment?id=%s&pageSize=30&mode=0&starRange=&userId=&sortType=0&offset=00' % shop_id
                yield Request(comment_url,callback=self.parse_comment, dont_filter=True, headers=header,meta={'shop_id':shop_id})
            url = response.url
            url_list = url.split('&p=')
            url = url_list[0] + '&p=%s' % (int(url_list[1]) + 1)
            # yield Request(url, callback=self.parse_shops_deals, headers=header, dont_filter=True)
            deal_id_list = re.findall('data-href="//i.meituan.com/deal/(\d+).html"', content)
            if deal_id_list:
                for deal_id in deal_id_list:
                    deal_url = 'https://i.meituan.com/general/platform/mttgdetail/' \
                               'mtdealbasegn.json?dealid=%s&eventpromochannel=' % deal_id
                    yield Request(deal_url, callback=self.parse_deal, headers=header, dont_filter=True)

    def parse_shop(self, response):
        content = response.body
        item = MeituanItem()
        item['content'] = content
        item['meituantype'] = 'shop'
        yield item

    def parse_deal(self, response):
        content = response.body
        try:
            content_json = json.loads(content)
            item = MeituanItem()
            item['content'] = content
            item['meituantype'] = 'deal'
            yield item
        except:
            pass

    def parse_comment(self,response):
        content = response.body
        try:
            content_json = json.loads(content)
            item = MeituanItem()
            item['content'] = content
            item['meituantype'] = response.meta['shop_id']
            yield item
            total = content_json.get('content_json')
            page_ = divmod(int(total),30)
            if page_[0]:
                pages = page_[0] + 1
                for i in xrange(1, pages):
                    offset = i * 30
                    print offset
                    url = response.url
                    url = url.split('&offset=')
                    comment_url = url[0]+'&offset=%s' % offset
                    print comment_url
                    yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                                  meta=response.meta)
        except:
            pass