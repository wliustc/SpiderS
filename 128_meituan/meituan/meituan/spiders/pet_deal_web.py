# -*- coding: utf-8 -*-
import json
import sys

import time

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import web
from scrapy import Request
import re
from meituan.items import MeituanItem
dt = time.strftime('%Y-%m-%d', time.localtime())

header = {
    'Host': 'bt.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

header_comment = {
    'Host': 'i.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

db = web.database(dbn='mysql', db='travel', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class PetDealSpider(scrapy.Spider):
    name = "pet_deal_web"
    allowed_domains = ["meituan.com"]
    start_urls = ['http://meituan.com/']

    def start_requests(self):
        data = db.query('select city_pinyin,city_id from travel.t_meituan_citylist;')
        for d in data:
            city_pinyin = d.get('city_pinyin')
            city_id = d.get('city_id')
            url = 'http://i.meituan.com/%s?cid=20691&sid=start&cateType=poi&p=1' % city_pinyin
            print url
            yield Request(url, callback=self.parse_area, headers=header, dont_filter=True, meta={'region': city_pinyin,'city_id':city_id})
            # yield Request(url='https://i.meituan.com/general/platform/mttgdetail/mtdealbasegn.json?dealid=42774143',
            #               callback=self.parse_deal, headers=header)
            # url = 'http://i.meituan.com/%s?cid=20691' % 'beijing'
            # yield Request(url, callback=self.parse_area, headers=header, dont_filter=True,meta={'region':'shanghai'})

    def parse_area(self, response):
        content = response.body
        if 'poiname' in content:
            d_cw = re.findall('宠物', content)
            if len(d_cw) > 5:
                content = ''.join(re.findall('id="filterData">(.*?)</script>', content))
                content_json = json.loads(content)
                print content_json
                BizAreaList = content_json.get('BizAreaList')
                if BizAreaList:
                    for biz in BizAreaList:
                        id = biz.get('id')
                        if id != -1:
                            city_id = response.meta['city_id']
                            url = 'http://api.mobile.meituan.com/group/v4/poi/pcsearch/%s?userid=-1&limit=1000&offset=0&areaId=%s&cateId=20691' % (city_id,id)
                            yield Request(url, callback=self.parse_shop_deals)
                            # url = 'http://i.meituan.com/%s?cid=20691&bid=%s&p=1' % (response.meta['region'], id)
                            # print url
                            # with open('url_list.csv', 'a')as f:
                            #     f.write(str(url) + '\n')
                            # yield Request(url, callback=self.parse_shops_deals1)
                else:
                    with open('no_bizarealist', 'a')as f:
                        f.write(str(response.url) + '\n')

    def parse_shop_deals(self, response):
        content_json = json.loads(response.body)
        data = content_json.get('data')
        if data:
            searchResult = data.get('searchResult')
            if searchResult:
                for result in searchResult:
                    shop_id = result.get('id')
                    shop_url = 'http://i.meituan.com/poi/%s' % shop_id
                    yield Request(shop_url, callback=self.parse_shop, dont_filter=True, headers=header)
                    # comment_url = 'http://www.meituan.com/ptapi/poi/getcomment?id=%s&pageSize=30&mode=0&starRange=&userId=&sortType=0&offset=00' % shop_id
                    # yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                    #               meta={'shop_id': shop_id, 'page_sign': 1})

                    comment_url = 'http://i.meituan.com/poi/%s/feedbacks/page_1' % shop_id
                    yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                                  meta={'shop_id': shop_id, 'page': 1})


                    deals = result.get('deals')
                    if deals:
                        for deal in deals:
                            deal_id = deal.get('id')
                            deal_url = 'https://i.meituan.com/general/platform/mttgdetail/' \
                                       'mtdealbasegn.json?dealid=%s&eventpromochannel=' % deal_id
                            yield Request(deal_url, callback=self.parse_deal, headers=header_comment, dont_filter=True)
            else:
                with open('no_searchResult', 'a')as f:
                    f.write(str(response.url) + '\n')
        else:
            with open('no_data', 'a')as f:
                f.write(str(response.url) + '\n')

    def parse_shops_deals1(self, response):
        print response.url
        content = response.body
        shop_id_list = re.findall('data-href="//i.meituan.com/poi/(\d+)', content)
        print shop_id_list
        if shop_id_list:
            for shop_id in shop_id_list:
                shop_url = 'http://i.meituan.com/poi/%s' % shop_id
                yield Request(shop_url, callback=self.parse_shop, dont_filter=True, headers=header)
                # comment_url = 'http://www.meituan.com/ptapi/poi/getcomment?id=%s&pageSize=30&mode=0&starRange=&userId=&sortType=0&offset=00' % shop_id
                # yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                #               meta={'shop_id': shop_id, 'page_sign': 1})
                comment_url = 'http://i.meituan.com/poi/%s/feedbacks/page_1' % shop_id
                yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                              meta={'shop_id': shop_id, 'page': 1})
            url = response.url
            url_list = url.split('&p=')
            url = url_list[0] + '&p=%s' % (int(url_list[1]) + 1)
            yield Request(url, callback=self.parse_shops_deals1, headers=header, dont_filter=True)
            deal_id_list = re.findall('data-href="//i.meituan.com/deal/(\d+).html"', content)
            if deal_id_list:
                for deal_id in deal_id_list:
                    deal_url = 'https://i.meituan.com/general/platform/mttgdetail/' \
                               'mtdealbasegn.json?dealid=%s&eventpromochannel=' % deal_id
                    yield Request(deal_url, callback=self.parse_deal, headers=header_comment, dont_filter=True,)

    def parse_shop(self, response):
        content = response.body
        item = MeituanItem()
        item['content'] = content
        item['meituantype'] = 'shop'
        item['dt'] = dt
        yield item

    def parse_deal(self, response):
        content = response.body
        try:
            content_json = json.loads(content)
            item = MeituanItem()
            item['content'] = content
            item['meituantype'] = 'deal'
            item['dt'] = dt
            yield item
        except:
            pass

    def parse_comment1(self, response):
        content = response.body
        try:
            content_json = json.loads(content)
            item = MeituanItem()
            item['content'] = content
            shop_id = response.meta['shop_id']
            item['meituantype'] = shop_id
            yield item
            page_sign = response.meta['page_sign']
            if page_sign:
                total = content_json.get('content_json')
                page_ = divmod(int(total), 30)
                if page_[0]:
                    pages = page_[0] + 1
                    for i in xrange(1, pages):
                        offset = i * 30
                        print offset
                        url = response.url
                        url = url.split('&offset=')
                        comment_url = url[0] + '&offset=%s' % offset
                        print comment_url
                        comment_url = comment_url
                        yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                                      meta={'shop_id': shop_id, 'page_sign': 0})
        except:
            pass

    def parse_comment(self, response):
        content = response.body
        data = re.findall('<weak class="username">(.*?)</weak>', content)
        if data:
            item = MeituanItem()
            item['content'] = content
            shop_id = response.meta['shop_id']
            item['meituantype'] = shop_id
            item['dt'] = dt
            yield item
            if len(data) == 15:
                url = response.url
                page = response.meta['page']
                page = page + 1
                url_list = url.split('page_')
                comment_url = url_list[0] + 'page_' + str(page)
                shop_id = response.meta['shop_id']
                yield Request(comment_url, callback=self.parse_comment, dont_filter=True, headers=header,
                              meta={'shop_id': shop_id, 'page': page})
