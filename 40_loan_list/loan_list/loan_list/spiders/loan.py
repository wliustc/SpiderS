# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector 
import json
import re
import datetime
import time
import db
from loan_list.items import LoanListItem
reload(sys)
sys.setdefaultencoding( "utf-8" )

task_date = datetime.date.today().strftime("%Y-%m-%d")
db.create_engine(host='10.15.1.24',database='hillinsight',user='writer',password='hh$writer',charset='utf8')

def get_city_list():
    sql = "select LOWER(city_name) as city_name from t_cyclical_auto_rong360_city where city_name in ('Shanghai','Beijing','Shenzhen','Wuhan','Tianjin','Guangzhou','Hangzhou','Xian','Chengdu','Changsha','Shenyang','Nanjing','Chongqing','Haerbin','Xiamen','Qingdao','Taiyuan')"
    cities = db.select(sql)
    return cities

_headers = {
    "Host":"www.rong360.com",
    "Connection":"keep-alive",
    "Accept":"ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cookie":"",
    "Upgrade-Insecure-Requests": 1
    }

_cookie = {
    "RONGID":"444b88f6dbd696a95d71c6ee192c174e",
    "abclass":"1480928889_5",
    "__jsluid":"43cfbb42b157d6723a00ada9755099a0",
    "PHPSESSID":"vkrtemr3sm44d3m53tfgq55bm2",
    "__gads":"ID=aa14a8d1e716b2f3:T=1480995290:S=ALNI_MYEctwhWHwNZv-3uLYbYtN25tOQkA",
    "my_city":"",
    '__utmz':"1481107400.utmcsr=(direct)|utmcmd=(direct)",
    "_atype":"9",
    "cityDomain":"",
    }
_method = 'POST'
_form_d={
    'loan_limit':'',
    'loan_term':'',
    'interest':'{$calInfo.interest}',
    'month_add':'{$calInfo.month_add}',
    'once_add':'{$calInfo.once_add}',
}

class LoanListSpider(scrapy.Spider):
    name = "rong360_loan_list"
    allowed_domains = ["rong360.com"]
    start_urls = (
        'http://www.rong360.com/',
    )

    def __init__(self, *args, **kwargs):
        self.basic_url = 'http://www.rong360.com'
        self.city_list = get_city_list()
        self.interest_url = 'http://www.rong360.com/api/detailCal'
        # 贷款金额从5万元到30万元,步长为5万元
        self.loan_amt_min = 5
        self.loan_amt_max = 30
        self.loan_amt_gap = 5
        # 贷款期限从12个月到36个月,步长为12个月
        self.loan_duration_min  = 12
        self.loan_duration_max  = 36
        self.loan_duration_gap  = 12
        # 贷款类型：0-零首付贷款 3-家用新车贷款
        self.zero_payment_loan = 0
        self.household_loan = 3
    
    def start_requests(self):
        for cl in self.city_list:
            # print cl['city_name']
            city = cl['city_name']
            tmp_cookie = _cookie
            tmp_cookie['cityDomain'] = city
            tmp_cookie['my_city'] = city
            tmp_header = _headers
            tmp_header['Cookie'] = tmp_cookie
            # 家用新车贷款类型
            url = self.basic_url + '/' + city + '/chedai/'
            yield scrapy.FormRequest(url,
                            cookies = tmp_cookie,
                            headers = tmp_header,
                            meta = {'city':city},
                            callback = self.parse_household,
                            dont_filter = True,
                            )
            # 零首付贷款类型
            for loan_amt in range(self.loan_amt_min, self.loan_amt_max + 1, self.loan_amt_gap):
                for loan_duration in range(self.loan_duration_min, self.loan_duration_max + 1, self.loan_duration_gap):
                    tmp = _form_d
                    tmp['loan_limit']   = str(loan_amt)
                    tmp['loan_term']    = str(loan_duration)
                    url = self.basic_url + '/' + city + '/search.html?loan_limit=%s&loan_term=%s'%(loan_amt,loan_duration)
                    yield scrapy.FormRequest(url,
                        formdata = tmp,
                        cookies = tmp_cookie,
                        headers = tmp_header,
                        method = _method,
                        meta = {'city':city, 'loan_amt':loan_amt, 'loan_duration':loan_duration},
                        callback = self.parse_list,
                        dont_filter = True,
                        )

    def parse_household(self, response):
        tmp = response.xpath('//div[@class="p-list wrap-clear"]/div[1]/div[2]/*[@class="item"]/*/*/@href').extract()
        loan_list = list(set(tmp))
        city = response.meta['city']
        for loan_id in loan_list:
            item = LoanListItem()
            loan_list = loan_id.split('p_')
            item['loan_id'] = loan_list[1]
            item['dt'] = task_date
            item['city'] = city
            item['loan_type'] = self.household_loan
            tmp_cookie = _cookie
            tmp_cookie['cityDomain'] = city
            tmp_cookie['my_city'] = city
            url = self.basic_url + "/" + loan_id
            yield scrapy.FormRequest(url,
                            cookies = tmp_cookie,
                            headers = _headers,
                            meta = {'item':item},
                            callback = self.parse_detail,
                            dont_filter = True,
                            )
    def parse_detail(self, response):
        loan_name = response.xpath('//h1/text()').extract()
        if not loan_name:
            loan_name = ""
        else:
            loan_name = loan_name[0].strip().replace(" ","")
        mortgage_info = response.xpath('//span[@class="item doc-color-red"]/span/text()').extract()
        if not mortgage_info:
            mortgage_info = ""
        else:
            mortgage_info = mortgage_info[0].strip().replace(" ","")
        identity_limit = response.xpath('//span[@class="spec can-reg"]/text()').extract()
        if not identity_limit:
            identity_limit = ""
        else:
            identity_limit = identity_limit[0].strip().replace(" ","")
        lending_time_info = response.xpath('//span[@class="spec fangkuan"]/text()').extract()
        if not lending_time_info:
            lending_time_info = ""
        else:
            lending_time_info = lending_time_info[0].strip()
        prepayment_requirement = response.xpath('//span[@class="doc-color-tail"]/*/@hover-tip').extract()
        if not prepayment_requirement:
            prepayment_requirement = response.xpath('//span[@class="doc-color-tail"]/span/text()').extract()
            if prepayment_requirement:
                prepayment_requirement = prepayment_requirement[0].strip()
            else:
                prepayment_requirement = ""
        else:
            prepayment_requirement = Selector(text=prepayment_requirement[0]).xpath("//span/text()").extract()[0]
            prepayment_requirement = prepayment_requirement.strip()
        extra_info = response.xpath('//meta[@name="description"]/@content').extract()
        if extra_info:
            extra_info = extra_info[0].strip()
        else:
            extra_info = ""
        detail = response.xpath('//div[@class="pd_other_item_content"]/text()').extract()
        item = response.meta['item']
        item['loan_name'] = loan_name
        item['mortgage_info'] = mortgage_info
        item['identity_limit_info'] = identity_limit
        item['lending_time_info'] = lending_time_info
        item['extra_info'] = extra_info
        item['prepayment_requirement'] = prepayment_requirement
        requrement_detail = ""
        if detail:
            for dl in detail:
                requrement_detail += dl.strip()
        item['requirement_detail'] = requrement_detail
        tmp_cookie = _cookie
        tmp_cookie['cityDomain'] = item['city']
        tmp_cookie['my_city'] = item['city']
        referer = "http://www.rong360.com/p_" + item['loan_id']
        tmp_header = _headers
        tmp_header['Referer'] = referer
        if item['loan_type'] == self.household_loan:
            for loan_amt in range(self.loan_amt_min, self.loan_amt_max + 1, self.loan_amt_gap):
                for loan_duration in range(self.loan_duration_min, self.loan_duration_max + 1, self.loan_duration_gap):
                    tmp_form_data = _form_d
                    tmp_form_data['loan_limit']   = str(loan_amt)
                    tmp_form_data['loan_term']    = str(loan_duration)
                    yield scrapy.FormRequest(self.interest_url,
                                         formdata = tmp_form_data,
                                         cookies = tmp_cookie,
                                         headers = tmp_header,
                                         method = _method,
                                         meta = {'item':item},
                                         callback = self.parse_interest,
                                         dont_filter = True,
                                        )
        elif item['loan_type'] == self.zero_payment_loan:
            tmp_form_data = _form_d
            tmp_form_data['loan_limit']   = str(item['loan_amt'])
            tmp_form_data['loan_term']    = str(item['loan_duration'])
            yield scrapy.FormRequest(self.interest_url,
                                     formdata = tmp_form_data,
                                     cookies = tmp_cookie,
                                     headers = tmp_header,
                                     method = _method,
                                     meta = {'item':item},
                                     callback = self.parse_interest,
                                     dont_filter = True,
                                    )
        else:
            pass
        pass

    def parse_interest(self, response):
        if response:
            json_obj = json.loads(response.body)
            if not json_obj:
                return
            else:
                item = response.meta['item']
                item['once_add'] = json_obj['once_add']
                item['loan_amt'] = json_obj['loan_limit']
                item['once_add_expense'] = json_obj['once_add_expense']
                item['month_expense'] = json_obj['month_expense']
                item['interest_expense'] = json_obj['interest_expense']
                item['month_add'] = json_obj['month_add']
                item['month_interest_rate'] = json_obj['month_interest_rate']
                item['interest'] = json_obj['interest']
                item['total_expense'] = json_obj['total_expense']
                item['add_expense'] = json_obj['add_expense']
                item['day_expense'] = json_obj['day_expense']
                item['loan_duration'] = json_obj['loan_term']
                item['created_time'] = int(time.time())
                # print item
                yield item
                    
    def parse_list(self, response):
        loan_list = response.xpath('//div[@ra-data-pl]/@ra-data-pl').extract()
        city = response.meta['city']
        loan_amt = response.meta['loan_amt']
        loan_duration = response.meta['loan_duration']
        for loan_id in loan_list:
            item=LoanListItem()
            item['loan_id'] = loan_id
            item['dt'] = task_date
            item['city'] = city
            item['loan_type'] = self.zero_payment_loan
            item['loan_amt'] = loan_amt
            item['loan_duration'] = loan_duration
            tmp_cookie = _cookie
            tmp_cookie['cityDomain'] = city
            tmp_cookie['my_city'] = city
            url = self.basic_url + "/p_" + loan_id
            yield scrapy.FormRequest(url,
                            cookies = tmp_cookie,
                            headers = _headers,
                            meta = {'item':item},
                            callback = self.parse_detail,
                            dont_filter = True,
                            )
        next_page = response.xpath(u'//*[@id="page_section"]/*[text()="下一页"]/@href').extract()

        if next_page:
            url = self.basic_url + next_page[0]
            yield scrapy.FormRequest(url,
                            meta = {'city':city, 'loan_amt':loan_amt, 'loan_duration':loan_duration},
                            callback = self.parse_list,
                            dont_filter = True,
                            )
        else:
            pass

        pass

def _get_proxy():
    urls = db.select('''
    select url from t_hh_proxy_list where domain ='rong360.com' and valid>0 order by update_time desc ''')
    return [e['url'] for e in urls]

    
    
    
    
    