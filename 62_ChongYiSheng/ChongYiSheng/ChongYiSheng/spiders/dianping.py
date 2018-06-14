# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Request
from urlparse import urljoin
import re, json
from scrapy.selector import Selector
from ChongYiSheng.items import ChongyishengItem
from scrapy.loader.processors import MapCompose
import sys

reload(sys)
sys.setdefaultencoding('utf8')


ChongYiSheng_list = [
    ['47', '宠颐生沈阳爱克威分院', '6124971', '3969'],
    ['48', '宠颐生沈阳瑞嘉分院', '23618362', '4331'],
    ['133', '宠颐生盘锦益友分院', '6007930', '3438'],
    ['139', '宠颐生北京爱之都分院', '4663168', '2082'],
    ['140', '宠颐生北京爱福分院', '16092628', '1503'],
    ['141', '宠颐生北京爱佳分院', '1772629', '3064'],
    ['142', '宠颐生成都宠福来分院', '43615785', '3788'],
    ['143', '萌家人成都九里堤分院', '67985395', '1863'],
    ['144', '萌家人成都牛市口分院', '27452514', '1875'],
    ['145', '萌家人成都高新一分院', '77333775', '1879'],
    ['157', '宠颐生北京京冠分院', '36848655', '8582'],
    ['158', '宠颐生北京爱之源分院', '13949683', '8597']
]


class DianpingSpider(scrapy.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]

    # start_urls = ['http://dianping.com/']

    def start_requests(self):
        # with open('chongyisheng.csv', 'r') as f:
        list_all = ChongYiSheng_list
        for informations_list in ChongYiSheng_list:
            information_list = {}
            # informations_list = ll.replace('\n', '').split(',')
            if len(informations_list) > 2:
                information_list['id'] = informations_list[0]
                information_list['clinic_name'] = informations_list[1]
                information_list['dianping_id'] = informations_list[2]
                information_list['system_id'] = informations_list[3]
                yield Request(url='https://www.dianping.com/shop/' + information_list['dianping_id'],
                              callback=self.parse, meta={'information_list': information_list})
                # information_list = {'id': 143, 'clinic_name': '萌家人成都九里堤分院', 'dianping_id': 67985395, 'system_id': 1863}
                # yield Request(url='https://www.dianping.com/shop/67985395', callback=self.parse,
                #               meta={'information_list': information_list})

    def parse(self, response):
        content = response.body
        meta = response.meta
        shopId = self.regex_str('shopId: (\d+),', content)
        shopCityId = self.regex_str('shopCityId: (\d+),', content)
        shopName = self.regex_str('shopName: "(.*?)",', content)
        mainCategoryId = self.regex_str('mainCategoryId:(.*?),', content)
        power = self.regex_str('power:(\d*),', content)
        shopType = self.regex_str('shopType:(\d*),', content)
        meta['shopId'] = shopId
        meta['shopCityId'] = shopCityId
        meta['shopName'] = shopName
        meta['mainCategoryId'] = mainCategoryId
        meta['power'] = power
        meta['shopType'] = shopType
        if shopId != '' and shopCityId != '' and shopName != '' and mainCategoryId != '':
            yield Request(url='https://www.dianping.com/ajax/json/shopDynamic'
                              '/reviewAndStar?shopId=%s&cityId=%s&mainCateg'
                              'oryId=%s' % (shopId, shopCityId, mainCategoryId),
                          callback=self.parse_hosptial, meta=meta)

    def parse_hosptial(self, response):
        content = response.body
        meta = response.meta
        meta['hospital'] = content
        yield Request(url='https://www.dianping.com/ajax/json/shopDynamic/promoInfo?'
                          'shopId=%s&cityId=%s&shopName=%s&power=%s&mainCategoryId=%s'
                          '&shopType=%s' % (meta['shopId'], meta['shopCityId'],
                                            meta['shopName'], meta['power'],
                                            meta['mainCategoryId'], meta['shopType']),
                      callback=self.parse_tuan, meta=meta)

    def parse_tuan(self, response):
        content = json.loads(response.body)
        # print content
        meta = response.meta
        print meta
        meta['dealDetail'] = content
        if 'dealMoreDetails' in content:
            dealMoreDetails = content['dealMoreDetails']
            for deal in dealMoreDetails:
                deal_href = deal['href']
                # print deal_href
                yield Request(url=deal_href, meta=meta, callback=self.parse_num)
        if 'dealDetails' in content:
            dealDetails = content['dealDetails']
            for deal in dealDetails:
                deal_href = 'http://t.dianping.com/deal/%s' % deal['id']
                # print deal_href
                yield Request(url=deal_href, meta=meta, callback=self.parse_num)

    def parse_num(self, response):
        sel = Selector(response)
        meta = response.meta
        print meta
        item = ChongyishengItem()
        package_name = self.is_exist(sel.xpath('//ul[@class=" Hide"]/li/a/span/text()').extract())
        package_num = self.is_exist(sel.xpath('//span[@class="J_dealCount"]/text()').extract()).replace('\r','').replace('\n','').replace('\t','').replace('份','').strip()
        item['package_name'] = package_name
        item['package_num'] = package_num
        item['package_id'] = response.url[response.url.index('deal/') + 5:]
        item['clinic_name'] = meta['information_list']['clinic_name']
        item['id'] = meta['information_list']['id']
        item['dianping_id'] = meta['information_list']['dianping_id']
        item['system_id'] = meta['information_list']['system_id']
        item['hospital'] = meta['hospital']
        item['dealDetail'] = meta['dealDetail']
        item['write_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        yield item

    def is_exist(self, _tuple):
        if _tuple:
            return _tuple[0]
        else:
            return ''

    def regex_str(self, pattern, content):
        result = re.findall(pattern, content)
        return self.is_exist(result)
