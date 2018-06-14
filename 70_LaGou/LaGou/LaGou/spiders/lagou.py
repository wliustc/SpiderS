# -*- coding: utf-8 -*-
import json
import re
import scrapy
import time
from scrapy import Request
import sys
from scrapy import FormRequest
from LaGou.items import LagouItem
from scrapy.selector import Selector
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

header = {
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
Cookie = {'LGUID': '20170802174242-ee540c0b-7766-11e7-92d7-525400f775ce;'}

#company_info = {'北京指南针': '67389',
#                '上海万得信息技术股份有限公司': '3174',
#                '大智慧': '2858',
#                '恒生电子': '22805',
#                '东方财富': '35179',
#                '同花顺': '325',
#                '浙江核新同花顺网络信息股份有限公司': '35512',
#                }
company_info = {'益盟操盘手合肥': '53365',
                '益盟操盘手上海': '3348',
                '益盟操盘手广州': '37363',
                '益盟操盘手杭州': '139801',
                '益盟操盘手北京': '122217'}


company_name_list = ['同花顺', '东方财富', '恒生电子', '大智慧', '万得信息技术(Wind)', '益盟', '指南针']
# company_name_list = ['国美互联网']
job_type_list = ['技术', '产品', '设计', '运营', '市场与销售', '职能', '金融']

keyword_list = ['数据分析', '量化策略', '大数据', '机器学习']
keyword_pattern = u'数据分析|量化策略|大数据|机器学习'

_header = {
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': '13bb5fc8-1255-4518-b91d-d9d64e953905',
    'X-Anit-Forge-Code': '68193195',
    'Referer': 'https://www.lagou.com/gongsi/j67389.html',
    'Content-Length': '73',
    # 'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499142498,1500263759,1501666948; _ga=GA1.2.1729670787.1499142498; user_trace_token=20170704122817-33e7924c-6071-11e7-88ed-525400f775ce; LGUID=20170704122817-33e79504-6071-11e7-88ed-525400f775ce; JSESSIONID=ABAAABAAAGFABEF522A3A08B58D80653628123D06902C6A; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501669013; _gid=GA1.2.429803829.1501666948; LGRID=20170802181652-b443ecce-776b-11e7-92e2-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=19a1d02aa4f64a57b603006077d91e22; _gat=1; LGSID=20170802181453-6d3fe772-776b-11e7-bf5a-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F67389.html; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2Fj67389.html',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

_header1 = {
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': '13bb5fc8-1255-4518-b91d-d9d64e953905',
    'X-Anit-Forge-Code': '68193195',
    # 'Referer': 'https://www.lagou.com/gongsi/j67389.html',
    # 'Content-Length': '72',
    # 'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499142498,1500263759,1501666948; _ga=GA1.2.1729670787.1499142498; user_trace_token=20170704122817-33e7924c-6071-11e7-88ed-525400f775ce; LGUID=20170704122817-33e79504-6071-11e7-88ed-525400f775ce; JSESSIONID=ABAAABAAAGFABEF522A3A08B58D80653628123D06902C6A; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501669013; _gid=GA1.2.429803829.1501666948; LGRID=20170802181652-b443ecce-776b-11e7-92e2-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=19a1d02aa4f64a57b603006077d91e22; _gat=1; LGSID=20170802181453-6d3fe772-776b-11e7-bf5a-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F67389.html; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2Fj67389.html',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}
_headers = {
    "Host": "www.lagou.com",
    "Connection": "keep-alive",
    "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": "",
    "Upgrade-Insecure-Requests": 1,
    "Referer": "https://www.lagou.com/gongsi/j35512.html"
}

_cookie = {
    # 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1499142498,1500263759,1501666948;',
    # '_ga': 'GA1.2.1729670787.1499142498;',
    # 'user_trace_token': '20170704122817-33e7924c-6071-11e7-88ed-525400f775ce;',
    # 'LGUID': '20170704122817-33e79504-6071-11e7-88ed-525400f775ce;',
    # 'JSESSIONID': 'ABAAABAAAGFABEF522A3A08B58D80653628123D06902C6A;',
    # 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1501669013;',
    # '_gid': 'GA1.2.429803829.1501666948;',
    # 'LGRID': '20170802181652-b443ecce-776b-11e7-92e2-525400f775ce;',
    # 'TG-TRACK-CODE': 'index_search;',
    # 'SEARCH_ID': '19a1d02aa4f64a57b603006077d91e22;',
    # '_gat': '1;',
    # 'LGSID': '20170802181453-6d3fe772-776b-11e7-bf5a-5254005c3644;',
    # 'PRE_UTM': '',
    # 'PRE_SITE':'',
    # 'PRE_LAND':'',
    # 'PRE_HOST':""
    'LGUID': '20170704122817-33e79504-6071-11e7-88ed-525400f775ce;',
    'TG-TRACK-CODE': 'index_search;',
    'LGSID': '20170802181453-6d3fe772-776b-11e7-bf5a-5254005c3644;'
}


class LagouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]

    def start_requests1(self):
        # for company_name, companyId in company_info.items():
        companyId = '67389'
        url = 'https://www.lagou.com/gongsi/searchPosition.json'
        # body = 'companyId=%s&positionFirstType=%s&pageNo=%s&pageSize=10' % (companyId, '全部', 1)
        # _cookie['PRE_SITE']='https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F'+str(companyId)+'.html'
        # _cookie['PRE_LAND'] = 'https%3A%2F%2Fwww.lagou.com%2Fgongsi%2Fj'+str(companyId)+'.html'

        # yield Request(url=url, body=body, method='POST', callback=self.parse_job_list,
        #               headers=_header,
        #               cookies=_cookie,
        #               meta={'job_type': '全部', 'pageNo': 1, 'companyId': companyId})
        body = {'companyId': companyId, 'positionFirstType': '全部',
                'pageNo': '1', 'pageSize': '10'}
        _header1['Referer'] = 'https://www.lagou.com/gongsi/j%s.html' % companyId
        # print _header
        print body
        yield FormRequest(url=url, formdata=body, callback=self.parse_job_list,
                          headers=_header1,
                          # cookies=_cookie,
                          meta={'job_type': '全部', 'pageNo': 1,
                                'companyId': companyId})
            # yield

    def start_requests(self):
        url = 'https://www.lagou.com/jobs/companyAjax.json?needAddtionalResult=false'
        # for company_name in company_name_list:
        for company_name,company_id in company_info.items():
            body = 'first=true&pn=1&kd=%s' % company_name
            _head = _header1
            _head['Referer'] = 'https://www.lagou.com/gongsi/j'+str(company_id)+'.html'
            print _head
            yield Request(url=url, body=body, method='POST', callback=self.parse, headers=_head, cookies=_cookie,meta={'company_id':company_id})
        # _head = _header1
        # _head['Referer'] = 'https://www.lagou.com/gongsi/j'+str(325)+'.html'

        # body = 'first=true&pn=1&kd=%s' % '同花顺'
        # yield Request(url=url, body=body, method='POST', callback=self.parse, headers=_head, cookies=_cookie,meta={'company_id':325})

    def parse(self, response):
        print response.body
        content_body = response.body
        content_json = json.loads(content_body)
        content = content_json.get('content')
        if content:
            result = content.get('result')
            if result:
                for result_child in result:
                    companyId = result_child.get('companyId')
                    if companyId:
                        for job_type in job_type_list:
                            url = 'https://www.lagou.com/gongsi/searchPosition.json'
                            body = 'companyId=%s&positionFirstType=%s&pageNo=%s&pageSize=10' % (companyId, job_type, 1)
                            _head = _header1
                            _head['Referer'] = 'https://www.lagou.com/gongsi/j' + str(response.meta['company_id']) + '.html'
                            yield Request(url=url, body=body, method='POST', callback=self.parse_job_list,
                                          headers=_head,
                                          cookies=Cookie,
                                          meta={'job_type': job_type, 'pageNo': 1, 'companyId': companyId})

    def parse_job_list(self, response):
        # print response.body
        content_body = response.body
        if 'clientIp' in content_body:
            print 'parse_jbo_list'+content_body+str(response.headers)
        content_json = json.loads(content_body)
        content = content_json.get('content')
        meta = response.meta
        _head = _header1
        _head['Referer'] = 'https://www.lagou.com/gongsi/j' + str(response.meta['companyId']) + '.html'

        if content:
            data = content.get('data')
            if data:
                page = data.get('page')
                if page:
                    result = page.get('result')
                    if result:
                        for result_child in result:
                            item = LagouItem()
                            companyId = result_child.get('companyId')
                            positionId = result_child.get('positionId')
                            jobNature = result_child.get('jobNature')
                            financeStage = result_child.get('financeStage')
                            item['company'] = result_child.get('companyFullName')
                            companySize = result_child.get('companySize')
                            industryField = result_child.get('industryField')
                            item['Job_title'] = result_child.get('positionName')
                            item['recruiting_city'] = result_child.get('city')
                            item['release_time'] = result_child.get('createTime')
                            item['payment'] = result_child.get('salary')
                            item['experience'] = result_child.get('workYear')
                            item['learn'] = result_child.get('education')
                            item['Job_type'] = meta['job_type']
                            item['source'] = 'lagou'
                            item['number'] = ''
                            yield Request(url='https://www.lagou.com/jobs/%s.html' % positionId, meta={'item': item},
                                          headers=_head, callback=self.parse_detail)
                        if len(result) == 10:
                            companyId = meta['companyId']
                            job_type = meta['job_type']
                            pageNo = meta['pageNo']
                            pageNo = int(pageNo) + 1
                            url = 'https://www.lagou.com/gongsi/searchPosition.json'
                            body = 'companyId=%s&positionFirstType=%s&pageNo=%s&pageSize=10' % (
                                companyId, job_type, pageNo)
                            yield Request(url=url, body=body, method='POST', callback=self.parse_job_list,
                                          headers=_head,
                                          cookies=Cookie,
                                          meta={'job_type': job_type, 'pageNo': pageNo, 'companyId': companyId})

    def parse_detail(self, response):
        item = response.meta['item']
        sel = Selector(response)
        keyword = sel.xpath('//ul[@class="position-label clearfix"]').xpath('string(.)')
        keyword = ''.join(keyword.extract())
        item['keyword'] = self.extract_data(keyword)

        Job_describe = ''.join(sel.xpath('//dd[@class="job_bt"]').xpath('string(.)').extract())
        item['Job_describe'] = self.extract_data(Job_describe)
        keyword_re = re.findall(keyword_pattern, item['keyword'] + item['Job_describe'])
        if keyword_re:
            keyword_re_str = ','.join(keyword_re)
            item['keyword'] = keyword_re_str
        item['task_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['release_time'] = self.format_release_time(item['release_time'])
        yield item

    def extract_data(self, data):
        data = data.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        return data

    def format_release_time(self, release_time):
        if '-' in release_time:
            return release_time
        else:
            return time.strftime("%Y-%m-%d", time.localtime())

    
    