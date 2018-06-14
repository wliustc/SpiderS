# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

import scrapy
import time
import xlrd
from scrapy import Request
from scrapy.selector import Selector
import sys
from TianYanCha.items import ProtectiveFoodsItem

reload(sys)
sys.setdefaultencoding('utf8')
start_time = time.strftime('%Y-%m-%d', time.localtime())
header = {
    'Host': 'www.bjda.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.bjda.gov.cn/eportal/ui?pageId=331186',
}


class QiduoweiSpider(scrapy.Spider):
    name = "protective_foods"
    allowed_domains = ["bjda.gov.cn",'map.baidu.com']
    start_urls = ['http://www.bjda.gov.cn/eportal/ui?pageId=331186']

    def start_requests(self):
        url = 'http://www.bjda.gov.cn/eportal/ui?pageId=331186'
        yield Request(url, callback=self.parse_list, meta={'page': 1}, headers=header)

    def parse_list(self, response):
        page_meta = response.meta['page']
        sel = Selector(response)
        list_link = sel.xpath('//tr[@class="chaxun_con"]/td[last()]/a/@href')
        if list_link:
            for link in list_link:
                link = urljoin(response.url, ''.join(link.extract()))
                yield Request(url=link, callback=self.parse_detail, headers=header)
            if page_meta == 1:
                title = ''.join(re.findall('总记录数:(.*?),', response.body))
                if int(title) % 20 == 0:
                    page_title = int(title) / 20
                else:
                    page_title = int(title) / 20 + 1
                print page_title
                for page in xrange(2, page_title + 1):
                    body = 'filter_LIKE_TITLE=&filter_LIKE_XKZH=&filter_EQ_FZJG=&currentPage=%s&pageSize=20' % page
                    yield Request(url='http://www.bjda.gov.cn/eportal/ui?pageId=331186', callback=self.parse_list,
                                  method='POST', body=body, meta={'page': page}, headers=header)
            else:
                pass

    def parse_detail(self, response):
        content = response.body
        item = ProtectiveFoodsItem()
        # print content
		
        company_name = ''.join(re.findall('单位名称:</th>[\s\S]*?<td>(.*?)<', content))
        print company_name
        license_number = ''.join(re.findall('许可证号:</th>[\s\S]*?<td>(.*?)<', content))
        legal_representative = ''.join(re.findall('法定代表人或业主:</th>[\s\S]*?<td>(.*?)<', content))
        address = ''.join(re.findall('地址:</th>[\s\S]*?<td>(.*?)<', content))
        permissive_range = ''.join(re.findall('许可范围:</th>[\s\S]*?<td>(.*?)<', content))
        licence_issuing_authority = ''.join(re.findall('发证机关:</th>[\s\S]*?<td>(.*?)<', content))
        date_of_issue = ''.join(re.findall('发证日期:</th>[\s\S]*?<td>(.*?)<', content))
        valid_date = ''.join(re.findall('有效期至:</th>[\s\S]*?<td>(.*?)<', content))
        state_of_certificate = ''.join(re.findall('证件状态:</th>[\s\S]*?<td>(.*?)<', content))
        item['company_name'] = company_name
        item['license_number'] = license_number
        item['legal_representative'] = legal_representative
        item['address'] = address
        item['permissive_range'] = permissive_range
        item['licence_issuing_authority'] = licence_issuing_authority
        item['date_of_issue'] = date_of_issue
        item['valid_date'] = valid_date
        item['state_of_certificate'] = state_of_certificate
        item['link'] = response.url
        item['write_time'] = start_time
        # item['response_body'] = content
        # item['url'] = response.url
        # yield item
        # time.sleep(600)
        yield Request(
            url='http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=xml&address=%s&ak=Ma9iCTQK9o9Ps9rMjUPnyvNU5lNtWQuI' % address,
            meta={'item': item}, callback=self.parse_lng_lat,dont_filter=True)

    def parse_lng_lat(self, response):
        lng = ''.join(re.findall('<lng>(.*?)</lng>',response.body))
        lat = ''.join(re.findall('<lat>(.*?)</lat>',response.body))
        item = response.meta['item']
        item['lng'] = lng
        item['lat'] = lat
        address = item['address']
        district = re.findall('北京市(.*?县)|北京市(.*?区)', address)
        if district:
            district = ''.join(district[0])
            if district:
                item['district'] = district
                yield item
        else:
            yield Request(url='http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=%s,%s&output=json&pois=1&ak=Ma9iCTQK9o9Ps9rMjUPnyvNU5lNtWQuI' % (lat,lng),callback=self.parse_district,meta={'item':item},dont_filter=True)

    def parse_district(self,response):
        item = response.meta['item']
        district = re.findall('district":"(.*?)"',response.body)
        if district:
            district=district[0]
            item['district'] = district
            yield item

    def parse_error(self, failure):
        url = failure.request.url
        if 'search' in url:
            yield Request(url, callback=self.parse_list, dont_filter=True, meta=failure.request.meta,
                          errback=self.parse_error)
        else:
            yield Request(url, callback=self.parse_detail, dont_filter=True,
                          errback=self.parse_error)

    
    
    
    