# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

import scrapy
import time
import xlrd
from scrapy import Request
from scrapy.selector import Selector
import sys
from TianYanCha.items import LicensedPharmacistItem
reload(sys)
sys.setdefaultencoding('utf8')



header ={
'Host': 'www.bjda.gov.cn',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'http://www.bjda.gov.cn/eportal/ui?pageId=331201',
}



class QiduoweiSpider(scrapy.Spider):
    name = "licensed_pharmacist"
    allowed_domains = ["bjda.gov.cn"]
    # start_urls = ['http://www.bjda.gov.cn/eportal/ui?pageId=331186']

    def start_requests(self):
        url = 'http://www.bjda.gov.cn/eportal/ui?pageId=331201'
        yield Request(url,callback=self.parse_list,meta={'page':1})

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
                    yield Request(url='http://www.bjda.gov.cn/eportal/ui?pageId=331201', callback=self.parse_list,
                                  method='POST', body=body, meta={'page': page}, headers=header)
            else:
                pass

    def parse_detail(self,response):
        content = response.body
        item = LicensedPharmacistItem()
        # print content

        name = ''.join(re.findall('姓名:</th>[\s\S]*?<td>(.*?)<',content))
        qualification_certificate_number = ''.join(re.findall('资格证书编号:</th>[\s\S]*?<td>(.*?)<', content))
        sex = ''.join(re.findall('性别:</th>[\s\S]*?<td>(.*?)<', content))
        practice_units_name = ''.join(re.findall('执业单位名称:</th>[\s\S]*?<td>(.*?)<', content))
        registered_certificate_number = ''.join(re.findall('注册证书号:</th>[\s\S]*?<td>(.*?)<', content))
        item['name'] = name
        item['qualification_certificate_number'] = qualification_certificate_number
        item['sex'] = sex
        item['practice_units_name'] = practice_units_name
        item['registered_certificate_number'] = registered_certificate_number

        yield item
        # time.sleep(600)

    def parse_error(self,failure):
        url = failure.request.url
        if 'search' in url:
            yield Request(url,callback=self.parse_list,dont_filter=True,meta=failure.request.meta,errback=self.parse_error)
        else:
            yield Request(url, callback=self.parse_detail, dont_filter=True,
                          errback=self.parse_error)
