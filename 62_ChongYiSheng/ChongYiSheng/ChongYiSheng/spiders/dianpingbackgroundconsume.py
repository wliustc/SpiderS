# -*- coding: utf-8 -*-
import json
import re

import datetime
from urlparse import urljoin
import time
import scrapy
from scrapy import Request
from scrapy import FormRequest
from scrapy import Selector
from ChongYiSheng.items import DianPingTuanDetailItem, TuanGouQuanItem

_cookie = {
    "MerchantDataCurrentShopId": "19156641",
    "lastInputAccount": "AnanpetMarketing",
    "JSESSIONID": "5E0ADD283838E26CE750CFDAAE6728F5",
    "cye": "beijing",
    "PHOENIX_ID": "0a030e37-158f60136a1-1a8b69d",
    "__utmz": "1.1481596018.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "edper": "fbe78a9a8f9fc3a684704cc09b8f8536bf2b7d7a212a51c12fdf88d46db875c46f7ed7bb1696277efbb6217b2cec87e2"
}

_header = {
    'Host': 'e.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'Referer': 'https://e.dianping.com/merchant/list',
    # 'Cookie': '_hc.v="\"0f6e7827-bc24-4e37-a02d-22712123f3b9.1487061681\""; cy=8; cye=chengdu; __utma=1.1700841063.1489718969.1489718969.1489718969.1; __utmz=1.1489718969.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a030e37-15aeaa15661-4fb813; JSESSIONID=C0C00713A28664E20CC053D266988F34; cXUbkHsw%2FH0ScasTvo0lz7ujLy9lsf59e9bJyqvLIFw%3D=22656280; JxhdnmlB7e4JEYzOiSirmfHSquMJ3UMcWUKuI92hzyA%3D=6124971; r42gX%2FiLe8PTUEe3O3oF6uSM2hz7K4MaZ3WI87Tcv%2Bc%3D=40126992; _bc_u=JwiC8i3nAVtEb1UDka3BVEWvwhVNf%2F%2BAOD%2BVJXQ6f1xpZ8SsTq9s%2BOWHG6Uxtsw7l9gjFPU8Nu6Y8Ij3ijbinroWRXPFA0dDL%2F%2FCRVMKpg8lo%2FQ5dCQ1cn%2FT%2BQ6MwHeFeGmSSdUwtLiSeYX%2FnOYLlIBpThEWmviLh2WlIvRPGyTDx2%2B6lj9xLKbH%2B0mTHdS7HScQPvHSAdWqjH0%2B9OVxiIGDYP8B79h2g4kuqodQ7pdeF4voMXpaAARedLpPJdm9nkXKyGg2TVq6wpiyIc8ImEqjxxj1IApDEqP5jYAf%2BmvYOPk2z3Y8LR7zzzROiwa3hGya2%2FHi84c9ofcQelU0pSxBhZkSLgjNUxdQP9VnPsGWFbCGL7L%2Fgco7kYIFZ2WIZ2aFlN2gk%2FwTQPEQBkhi34RsS3AkSeixvZhBUqsVeTldh4GZ%2FaP0lggN4B5L7yg3AtH4tBhV0ZVr5xeRIJkWc%2FPKE2cC3jEwSVZhTSUD%2B8R1FMQfmPwycYMdGB7L6nQ%2B4s5WT5KvwRVdrXf%2BhSiFX0TQpL7vbIg7WOpzI7cFdh4%3D; mopay_popup_shown=3; hidesupertipsmerge=1; edper=kSN6wyZrHPKXiSMTPWZto7xccJCRReLs',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

Cookie_sycysdwyy = {
    'PHOENIX_ID': '0a030e37-15aeaa15661-4fb813',
    'JxhdnmlB7e4JEYzOiSirmfHSquMJ3UMcWUKuI92hzyA%3D': '6124971',
    'edper': 'kSN6wyZrHPKXiSMTPWZto7xccJCRReLs',
}

Cookie_ananpet = {
    'PHOENIX_ID': '0a030e37-15aff3642b7-17c6f6',
    'FItNeiu3PM0ua3O5hv13QHCJc14YNW9BNsrepmfoizk%3D': '67980409',
    'edper': 'oHajmCn4-JqXiSMTPWZto__2vsek-t9e',
}

Cookie_AnanpetMarketing = {
    'PHOENIX_ID': '0a030e37-15aff3642b7-17c6f6',
    'XY0w6isWSa36UbuxD0dp6GU04R%2FHrgtcviezHYxD2V0%3D': '69230980',
    'edper': 'Qxrmh9p79HiXiSMTPWZto5QUzEqg7NUM',
}

Cookie_myfamily = {
    'PHOENIX_ID': '0a030e37-15bae438fce-252d73c',
    'edper': 'USLjI0R-uW2XiSMTPWZto8yBq6Foh8Qg',
    'lxOAtgUjXs7yl01SqJ9O4A%2FzaEPTLMeZ8e8Lh%2BV08f8%3D': '27452514',
}

Cookie_tjchongyishenggg = {
    'PHOENIX_ID': '0a030e37-15bae438fce-252d73c',
    'edper': 'DSxcV-op0idGlsuA8z1pq7NdlPl2XCbY8XhaTM6C35pqIhbWgxeuJzvNi7-QfY7T-NtId-l7-aVjVAPyepqzCg;',
    'PboA3a3Sui7gxh8MnYYkW9DQEr3mbcXXa5mjWjI05Mc%3D': '91020075',
}

# cXUbkHsw%2FH0ScasTvo0lz7ujLy9lsf59e9bJyqvLIFw%3D=26784866; PboA3a3Sui7gxh8MnYYkW9DQEr3mbcXXa5mjWjI05Mc%3D=91020075; r42gX%2FiLe8PTUEe3O3oF6rEPKihSXjc%2BztcyZnIANA4%3D=40360985; _bc_u=Iotx6oVh09z7l45DjS8XLowAycrHaH9bSKQV2n2NEhxdTCRHva8qeBdvIbxbuIqOztiI1avsPo6poDIwSMaf3S%2Bdf0iXmaoxOz6gt5ku2CRVCpogOvoLgDh3mGyIa1HN0kqdJF6rJqyZXUoOJ8A4lU2UBppIVIr90xYK%2BS7y0zYSL%2FOBBJamwYEHnhCglFAoNHfaXBnGdQGEyq2lhIrcwom64eJSi1n8a6mW%2BLwrGEsape1wIugJJyG795nwCGsvGMODZ8qf7bgqt5IPDLPtRvbGWnoHwna2Z%2BN%2BWgw6wr%2BckLnxJjU72ltFJkCVu%2FbFdlw34Q4GabAlUhXPf2uYoFtrbwNIXEUJw2GoBeqbStLoOOKmsucc%2F0c%2FRIGQO5HJAIUZsxt%2B8YQNEl3loJiMz4tHDT3uuBa3BjCkQQZ9gHvn8pwDkYrmbEKteZBjZ4oTRvYQDfv86gmQIUQz9UH7uQfph1oFiaamADoHCamqdyRylf%2B%2F%2FG0T2zLMf30OKC2zn0j14IUswM6Ldzyw3csduTOwLYJb0pe1A9w4tnpvn6k%3D











_shop_info = {
    "sycysdwyy": {"shop_id": "23618362", "pw": "Cexingpet2018", 'Cookie': Cookie_sycysdwyy},
    #"AnanpetMarketing": {"shop_id": "19156641", "pw": "Ananpet@2017", 'Cookie': Cookie_AnanpetMarketing},
    #"ananpet": {"shop_id": "67980409", "pw": "Ananpet2017", 'Cookie': Cookie_ananpet},
    #"myfamily": {"shop_id": "67985395", "pw": "walkrock10", 'Cookie': Cookie_myfamily},
    #"tjchongyishenggg": {"shop_id": "91020075", "pw": "qwe123456", 'Cookie': Cookie_tjchongyishenggg},
}

_method = "POST"


class DianpingBackgroundSpider(scrapy.Spider):
    name = "dianpingbackgroundconsume"
    allowed_domains = ["dianping.com", "meituan.com"]
    start_urls = ['http://dianping.com/']

    def __init__(self, account='myfamily', *args, **kwargs):
        super(DianpingBackgroundSpider, self).__init__(*args, **kwargs)
        self.file_path = "./data/"
        self.platform_type_dict = {"0": "全部平台", "1": "大众点评", "2": "美团"}
        # self.less_shop = "ananpet"
        # self.much_shop = "AnanpetMarketing"
        self.account_name = account
        if account in _shop_info:
            self.account_info = _shop_info[account]
            self.cookie = _shop_info[account]['Cookie']
        else:
            self.account_name = None
        # self.cookie = Cookie1
        self.shop_dict = {}

    def start_requests(self):
        url = 'https://epassport.meituan.com/api/account/login?service=dpmerchantlogin&bg_source=2&loginContinue=https:%2F%2Fe.dianping.com%2Fshopaccount%2Flogin%2Fsetedper%3FtargetUrl%3Dhttps%253A%252F%252Fe.dianping.com%252Fshopportal%252Fpc%252Fnewindex'
        header = {
            'Host': 'epassport.meituan.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        }
        body = {"login": self.account_name, "password": self.account_info['pw'], "part_key": "", "captcha_code": "",
                "captcha_v_token": ""
            , "sms_verify": 0, "sms_code": ""}
        body = json.dumps(body)
        yield Request(url=url,body=body,
                                     method=_method,callback=self.parse_bsid,headers=header,dont_filter=True)

    def parse_bsid(self,response):
        print response.body
        response_json = json.loads(response.body)
        bsid = response_json.get('bsid')
        if bsid:

            print bsid
            header = {
                'Host': 'e.dianping.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://epassport.meituan.com/account/unitivelogin?bg_source=2&service=dpmerchantlogin&feconfig=dpmerchantlogin&continue=https%3A%2F%2Fe.dianping.com%2Fshopaccount%2Flogin%2Fsetedper%3FtargetUrl%3Dhttps%253A%252F%252Fe.dianping.com%252Fshopportal%252Fpc%252Fnewindex',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            url = 'https://e.dianping.com/shopaccount/login/setedper?targetUrl=https%3A%2F%2Fe.dianping.com%2Fshopportal%2Fpc%2Fnewindex&BSID='+bsid
            # data = requests.get(url, headers=header)
            # print data.content
            yield Request(url,headers=header,callback=self.make_requests_from_url,dont_filter=True)
        else:
            # time.sleep(5)
            # millis = int(round(time.time() * 1000))
            # url = 'https://epassport.meituan.com/account/needCaptchaV2?part_type=0&bg_source=2&nocache=%s&login=%s&part_key=' % (
            # millis, self.account_name)
            # header = {
            #     'Host': 'epassport.meituan.com',
            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
            #     'Accept': 'application/json',
            #     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            #     'Accept-Encoding': 'gzip, deflate, br',
            #     'X-Requested-With': 'XMLHttpRequest',
            #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            #     'Origin': 'https://epassport.meituan.com',
            #     'Connection': 'keep-alive'
            # }
            # yield Request(url, headers=header, callback=self.parse_uuid,dont_filter=True)
            pass
        
    def make_requests_from_url(self, response):
        if '账号登录中......' in response.body:
            print '登录成功'
            Cookiett = response.headers.getlist('Set-Cookie')
            print Cookiett
            self.cookie['PHOENIX_ID'] = ''.join(re.findall('PHOENIX_ID=(.*?);', ''.join(Cookiett)))
            self.cookie['edper'] = ''.join(re.findall('edper=(.*?);', ''.join(Cookiett)))
            url = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
            yield Request(url, callback=self.parse_tuangou_shop, dont_filter=True,
                          headers=_header, cookies=self.cookie)



        else:
            print '登录失败'

    def parse_tuangou_shop(self, response):
        content = response.body
        shop_option = re.findall('option value="(.*?)".*?>(.*?)</option', content)
        for option in shop_option:
            self.shop_dict[option[1]] = option[0]
            # print type(option[1]+'医院')
        tuangou_count = 0
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        #url = 'https://e.dianping.com/receiptreport/tuangouConsume?selectedDealId=0&selectedShopId=0&selectedBeginDate=' + yesterday + '%2000:00:00&selectedEndDate=' + yesterday + '%2023:59:59&page=1'
        url = 'https://e.dianping.com/receiptreport/tuangouConsume?selectedDealId=0&productType=0&selectedShopId=0&selectedBeginDate=2017-11-16%2000:00:00&selectedEndDate=2017-11-20%2023:59:59'

        tmp_header = _header
        tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
        yield Request(url, callback=self.parse_tuangou, dont_filter=True,
                      headers=tmp_header, cookies=self.cookie, meta={'tuangou_count': tuangou_count, 'pageIndex': 1})

    # 团购消费情况
    def parse_tuangou(self, response):
        # print response.body
        sel = Selector(response)
        verify_table = sel.xpath('//div[@class="table-list"]/table/thead/tr/td/a/@href')
        for verify in verify_table:
            url = ''.join(verify.extract())
            # print url
            yield Request(url=urljoin(response.url, url), headers=_header, cookies=self.cookie,
                          callback=self.parse_tuandetail)
        page_next = ''.join(sel.xpath('//div[@class="pages-wrap"]/div/a[last()]/@title').extract())
        if page_next:
            print page_next
            if page_next=='下一页':
                url = ''.join(sel.xpath('//div[@class="pages-wrap"]/div/a[last()]/@href').extract())
                url = urljoin(response.url,url)
                tmp_header = _header
                tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
                yield Request(url, callback=self.parse_tuangou, dont_filter=True,
                              headers=tmp_header, cookies=self.cookie,
                              meta={'pageIndex': 1})

    # 团购消费具体情况
    def parse_tuandetail(self, response):
        item = DianPingTuanDetailItem()
        sel = Selector(response)
        details_list = sel.xpath('//table[@id="consume-detail-list"]/thead/tr')
        for details in details_list:
            # print details
            detail_list = details.xpath('td').xpath('string(.)').extract()
            if detail_list:
                # for detail in detail_list:
                #     print detail
                item['Serial'] = detail_list[0]
                item['phone'] = detail_list[1]
                item['consume_time'] = detail_list[2]
                item['package_name'] = detail_list[3]
                item['deal_id'] = ''.join(re.findall('\[(\d+)\]',detail_list[3]))
                item['price'] = detail_list[4]
                item['business_privilege'] = detail_list[5]
                item['settlement_price'] = detail_list[6]
                item['shopname'] = detail_list[7]
                item['checkout_account'] = detail_list[8]
                print detail_list[7]
                print type(detail_list[7])
                item['shopId'] = self.shop_dict[str(detail_list[7])]
                item['write_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                item['account'] = self.account_name
                yield item

        page_next = ''.join(sel.xpath('//div[@class="pages-wrap"]/div/a[last()]/@title').extract())
        if page_next:
            print page_next
            if page_next == '下一页':
                url = ''.join(sel.xpath('//div[@class="pages-wrap"]/div/a[last()]/@href').extract())
                url = urljoin(response.url, url)
                tmp_header = _header
                tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/tuangouConsume'


                yield Request(url, callback=self.parse_tuandetail, dont_filter=True,
                              headers=tmp_header, cookies=self.cookie,
                              meta={'pageIndex': 1})

    
    
    
    
    
    
    
    
    
    
    
    
    
    