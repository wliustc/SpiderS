# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

import scrapy
import time
import xlrd
from scrapy import Request
from scrapy.selector import Selector
import sys
from TianYanCha.items import AdministrativePenaltyItem

reload(sys)
sys.setdefaultencoding('utf8')

header = {
    'Host': 'www.bjda.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.bjda.gov.cn/eportal/ui?pageId=331186',
}

'''
行政处罚
'''


class QiduoweiSpider(scrapy.Spider):
    name = "administrative_penalty"
    allowed_domains = ["bjda.gov.cn"]
    start_urls = ['http://www.bjda.gov.cn/eportal/ui?pageId=331216&currentPage=1&filter_LIKE_TITLE=&filter_LIKE_XKZH=']

    def start_requests(self):
        url = 'http://www.bjda.gov.cn/eportal/ui?pageId=331216&currentPage=1&filter_LIKE_TITLE=&filter_LIKE_XKZH='
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
                title = ''.join(re.findall('总记录数:(\d+)', response.body))
                if int(title) % 20 == 0:
                    page_title = int(title) / 20
                else:
                    page_title = int(title) / 20 + 1
                print page_title
                for page in xrange(2, page_title + 1):
                    yield Request(
                        url='http://www.bjda.gov.cn/eportal/ui?pageId=331216&'
                            'currentPage=%s&filter_LIKE_TITLE=&filter_LIKE_XKZH=' % page,
                        callback=self.parse_list, method='GET', meta={'page': page}, headers=header)
            else:
                pass

    def parse_detail(self, response):
        content = response.body
        item = AdministrativePenaltyItem()
        administrative_penalty_decision_number = ''.join(re.findall('行政处罚决定书文号:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        legal_case_name = ''.join(re.findall('案件名称:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        party_name = ''.join(re.findall('当事人名称:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        organization_code = ''.join(re.findall('组织机构代码或身份证号:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        legal_representative = ''.join(re.findall('法定代表人:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        main_facts = ''.join(re.findall('违反法律、法规或规章的主要事实:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        legal_basis = ''.join(re.findall('行政处罚种类、依据:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        methods_of_performance = ''.join(re.findall('履行方式和期限:</th>[\s\S]*?<td>([\s\S]*?)<', content))
        penalty_organ = ''.join(re.findall('作出处罚的机关和决定日期:</th>[\s\S]*?<td>([\s\S]*?)<', content))


        item['administrative_penalty_decision_number'] = administrative_penalty_decision_number
        item['legal_case_name'] = legal_case_name
        item['party_name'] = party_name
        item['organization_code'] = organization_code
        item['legal_representative'] = legal_representative
        item['main_facts'] = main_facts
        item['legal_basis'] = legal_basis
        item['methods_of_performance'] = methods_of_performance
        item['penalty_organ'] = penalty_organ
        # item['url'] = response.url
        yield item
        # time.sleep(600)

    def parse_error(self, failure):
        url = failure.request.url
        if 'search' in url:
            yield Request(url, callback=self.parse_list, dont_filter=True, meta=failure.request.meta,
                          errback=self.parse_error)
        else:
            yield Request(url, callback=self.parse_detail, dont_filter=True,
                          errback=self.parse_error)

    