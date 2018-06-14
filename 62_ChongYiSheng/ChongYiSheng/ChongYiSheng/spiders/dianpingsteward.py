# -*- coding: utf-8 -*-
import json
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC           # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
import datetime
from urlparse import urljoin
import time
import scrapy
import web
from scrapy import Request
from scrapy import FormRequest
from scrapy import Selector
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from ChongYiSheng.items import DianPingTuanDetailItem, TuanGouQuanItem, CalDateCountItem

_header = {
    'Host': 'e.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

_shop_info = {
    # "sycysdwyy": {"shop_id": "23618362", "pw": "Cexingpet8737", 'Cookie': Cookie_sycysdwyy},
    # "AnanpetMarketing": {"shop_id": "19156641", "pw": "Ananpet@2017", 'Cookie': Cookie_AnanpetMarketing},
    # "ananpet": {"shop_id": "67980409", "pw": "Ananpet2017", 'Cookie': Cookie_ananpet},
    # "myfamily": {"shop_id": "67985395", "pw": "walkrock10", 'Cookie': Cookie_myfamily},
    # "tjchongyishenggg": {"shop_id": "91020075", "pw": "qwe123456", 'Cookie': Cookie_tjchongyishenggg},
}

_shop_info_list = (
    {'dianping_account': 'sycysdwyy', 'dianping_pwd': 'Cexingpet2018', 'dianping_id': '23618362'},
    # {'dianping_account': 'AnanpetMarketing', 'dianping_pwd': 'Ananpet@2017', 'dianping_id': '19156641'},
    {'dianping_account': 'ananpet', 'dianping_pwd': 'Ananpet2017', 'dianping_id': '67980409'},
    {'dianping_account': 'myfamily', 'dianping_pwd': 'walkrock10', 'dianping_id': '67985395'},
    {'dianping_account': 'tjchongyishenggg', 'dianping_pwd': 'qwe123456', 'dianping_id': '91020075'},
)

_method = "POST"


TuanGouQuanItem_result = [
    'dpSailedTipMsg',
    'processId',
    'endDate',
    'mtDealGroupId',
    'ownerName',
    'mtSailedNum',
    'ownerTel',
    'channelStatus',
    'title',
    'mtUrl',
    'brief',
    'buttons',
    'dpSailedTip',
    'status',
    'outBizId',
    'mtSailedTip',
    'price',
    'dpSailedNum',
    'merchantType',
    'dpDealGroupId',
    'mtSailedTipMsg',
    'endTip',
    'ownerId',
    'dpUrl',
    'customerId',
    'dphospital_name',
    'dphospital_id',
    'mthospital_name',
    'mthospital_id',
    'write_time',
    'dphospital_list',
    'mthospital_list',
    'account'
]

# 艾贝尔采集
class DianpingBackgroundSpider(scrapy.Spider):
    name = "dianpingsteward"
    allowed_domains = ["dianping.com", "meituan.com"]
    start_urls = ['http://dianping.com/']

    def __init__(self, account_num='local', *args, **kwargs):
        super(DianpingBackgroundSpider, self).__init__(*args, **kwargs)
        self.account_num = account_num

    def start_requests(self):
        if self.account_num != 'local':
            db = web.database(dbn='mysql', db='pet_cloud', user='work', pw='phkAmwrF', port=3306, host='10.15.1.14')
            data = db.query(
                '''select distinct dianping_account,dianping_pwd from 
                hospital_base_information where dianping_id!=0 
                and dianping_account!='' and dianping_pwd!='' 
                and dianping_account not in ('tjchongyishenggg','myfamily','ananpet','sycysdwyy','18021617370','2422357436','18036816952',
                '18061439182','17317321790','15800900756','18020359009','couragefaith','ahcys2018')
                 limit %s;''' % self.account_num)
            # data = db.query('''select * from hospital_base_information where dianping_account='tjchongyishenggg';''')
        else:
            data = _shop_info_list
        for d in data:
            account_name = d.get('dianping_account')
            account_pwd = d.get('dianping_pwd')
            dianping_id = d.get('dianping_id')
            print account_name
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap[
                "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.get(
                "https://epassport.meituan.com/account/unitivelogin?bg_source=2&service=dpmerchantlogin&feconfig=dpmerchantlogin&leftBottomLink=https%3a%2f%2fe.dianping.com%2fshopaccount%2fphoneRegisterAccount&continue=https%3A%2F%2Fe.dianping.com%2Fshopaccount%2Flogin%2Fsetedper%3FtargetUrl%3Dhttps%253A%252F%252Fe.dianping.com%252Fshopportal%252Fpc%252Fnewindex")
            try:
                inputElement_user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login")))
                inputElement_user.send_keys(account_name)
                pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
                pwd.send_keys(account_pwd)
                # driver.get_screenshot_as_file('11.png')
                driver.find_element_by_xpath("//button[@type='submit']").click()
                time.sleep(5)
                cookie1 = driver.get_cookies()
                cookies = {}
                for cookie in cookie1:
                    name = cookie['name'].encode('utf-8')
                    value = cookie['value'].encode('utf-8')
                    cookies = {
                        name: value
                    }
                print cookies
                driver.quit()
                if 'edper' in cookies:
                    header_mtuangou = {
                        'Host': 'e.dianping.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': 'https://e.dianping.com/shopportal/pc/newindex',
                        'Cookie': 'edper=' + cookies['edper'],
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                    url = 'https://e.dianping.com/mtuangou/tuangoulogin'
                    # yield Request(url=url,
                    #               meta={'account_name': account_name, 'account_pwd': account_pwd, 'dianping_id': dianping_id},
                    #               method=_method, callback=self.parse_bsid, headers=header_mtuangou, dont_filter=True)




                    # data = requests.head(url, headers=header_mtuangou)
                    # data_headers = data.headers
                    try:
                    #     Set_Cookie = data_headers['Set-Cookie']
                    #     Set_Cookie_list = str(Set_Cookie).split('; ')
                    #     for set_cook in Set_Cookie_list:
                    #         set_cook_list = set_cook.split('=')
                    #         try:
                    #             if set_cook_list[0] == 'Path':
                    #                 cookie[set_cook_list[1].replace('/, ', '')] = set_cook_list[2]
                    #             else:
                    #                 cookie[set_cook_list[0]] = set_cook_list[1]
                    #         except:
                    #             pass
                        meta = {}
                    #     # meta = response.meta
                        meta['cookie'] = cookies
                        meta['account_name'] = account_name
                # url = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
                # yield Request(url, callback=self.parse_tuangou_shop, dont_filter=True,
                #               headers=_header, cookies=cookie, meta=meta)

                # 团购消费情况
                        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                        url = 'https://e.dianping.com/receiptreport/tuangouConsume?selectedDealId=0&selectedShopId=0&selectedBeginDate=' + yesterday + '%2000:00:00&selectedEndDate=' + yesterday + '%2023:59:59&page=1'
                        # url = 'https://e.dianping.com/receiptreport/tuangouConsume?selectedDealId=0&selectedShopId=0&selectedBeginDate=2017-09-13%2000:00:00&selectedEndDate=2017-09-31%2023:59:59&page=1'
                        tmp_header = _header
                        tuangou_count = 0
                        tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
                        meta['tuangou_count'] = tuangou_count
                        meta['pageIndex'] = 1
                        yield Request(url, callback=self.parse_tuangou, dont_filter=True,
                                      headers=tmp_header, cookies=meta['cookie'], meta=meta)

                        # 团购购买量情况
                        tmp_header = _header
                        url = 'https://e.dianping.com/merchant/load/dealgroup/list?status=1&pageIndex=1'
                        refer = 'https://e.dianping.com/merchant/list'
                        # tmp_header = _header
                        tmp_header['Referer'] = refer
                        tuandan_count = 0
                        meta['tuandan_count'] = tuandan_count
                        meta['pageIndex'] = 1
                        yield Request(url, callback=self.parse_tuandan, dont_filter=True, headers=tmp_header,
                                      cookies=meta['cookie'], meta=meta)

                        # 交易数据》销售数据》浏览
                        tmp_header = _header
                        url = 'https://e.dianping.com/receiptreport/dealview'
                        refer = 'https://e.dianping.com/tuanreceipt/dealsale'
                        tmp_header['Referer'] = refer

                        yield Request(url, callback=self.parse_browse, dont_filter=True, headers=tmp_header,
                                      cookies=meta['cookie'], meta=meta)
                    except Exception, e:
                        print 'error-------------------'
            except:
                pass
        else:
            print '登录失败'


    # 未使用
    def parse_tuangou_shop(self, response):
        meta = response.meta
        content = response.body
        shop_dict = {}
        shop_option = re.findall('option value="(.*?)".*?>(.*?)</option', content)
        for option in shop_option:
            shop_dict[option[1]] = option[0]
            # print type(option[1]+'医院')
        tuangou_count = 0
        meta['shop_dict'] = shop_dict
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        # url = 'https://e.dianping.com/tuanreceipt/tuangouConsume?selectedDealId=0&selectedShopId=0&selectedBeginDate=' + yesterday + '%2000:00:00&selectedEndDate=' + yesterday + '%2023:59:59&page=1'
        url = 'https://e.dianping.com/tuanreceipt/tuangouConsume?selectedDealId=0&selectedShopId=0&selectedBeginDate=2017-09-13%2000:00:00&selectedEndDate=2017-09-31%2023:59:59&page=1'
        tmp_header = _header
        tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/tuangouConsume'
        meta['tuangou_count'] = tuangou_count
        meta['pageIndex'] = 1
        yield Request(url, callback=self.parse_tuangou, dont_filter=True,
                      headers=tmp_header, cookies=meta['cookie'], meta=meta)

    # 团购消费情况
    def parse_tuangou(self, response):
        meta = response.meta
        content = response.body
        shop_dict = {}
        shop_option = re.findall('option value="(.*?)".*?>(.*?)</option', content)
        for option in shop_option:
            shop_dict[option[1]] = option[0]
            # print type(option[1]+'医院')
        tuangou_count = 0
        meta['shop_dict'] = shop_dict
        sel = Selector(response)
        verify_table = sel.xpath('//div[@class="table-list"]/table/thead/tr/td/a/@href')
        for verify in verify_table:
            url = ''.join(verify.extract())
            yield Request(url=urljoin(response.url, url), headers=_header, cookies=response.meta['cookie'],
                          callback=self.parse_tuandetail, meta=response.meta, dont_filter=True)

    # 团购消费具体情况
    def parse_tuandetail(self, response):
        meta = response.meta
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
                item['price'] = detail_list[4]
                item['business_privilege'] = detail_list[5]
                item['settlement_price'] = detail_list[6]
                item['shopname'] = detail_list[7]
                item['checkout_account'] = detail_list[8]
                print detail_list[7]
                print type(detail_list[7])
                item['shopId'] = meta['shop_dict'][str(detail_list[7])]
                item['write_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                item['account'] = meta['account_name']
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
                              headers=tmp_header, cookies=meta['cookie'],
                              meta=meta)

    # 团购购买情况
    def parse_tuandan(self, response):
        # print response.body
        tuandanlist = json.loads(response.body)
        meta = response.meta
        if tuandanlist['code'] == 200:
            tuandandata = tuandanlist['data']
            # print tuandandata
            tuandan_dealgroups = tuandandata['dealgroups']
            if tuandan_dealgroups:
                for tuandan_deal in tuandan_dealgroups:
                    # print tuandan_deal
                    item = TuanGouQuanItem()
                    # tuandan_deal = json.loads(tuandan_deal,encoding='utf-8')
                    for key, value in tuandan_deal.items():
                        if key in TuanGouQuanItem_result:
                            if value:
                                item[key] = value
                            else:
                                item[key] = ''
                    # print item
                    mtDealGroupId = item['mtDealGroupId']
                    # 判断有没有美团的团单id

                    item['mthospital_name'] = ''
                    item['mthospital_id'] = ''
                    item['mthospital_list'] = ''
                    dpDealGroupId = item['dpDealGroupId']
                    # 判断有没有大众点评的url，如果没有直接制空
                    if 0:
                        dpDealGroupId = item['dpDealGroupId']
                        url = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=%s&action=region' % dpDealGroupId
                        # yield Request(url=url, callback=self.parse_tuandan_city,
                        #               meta={'item': item})
                    else:
                        item['dphospital_name'] = ''
                        item['dphospital_id'] = ''
                        item['dphospital_list'] = ''
                        item['write_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        item['brief'] = ''
                        item['buttons'] = ''
                        item['account'] = meta['account_name']
                        yield item
                tuandan_count = meta['tuandan_count']
                tuandan_count = tuandan_count + len(tuandan_dealgroups)
                if tuandan_count < int(tuandandata['totalCount']):
                    pageIndex = meta['pageIndex'] + 1
                    meta['tuandan_count'] = tuandan_count
                    meta['pageIndex'] = pageIndex
                    print '#################'
                    yield Request(url=re.sub('pageIndex=(\d+)', '', response.url) + 'pageIndex=%s' % pageIndex,
                                  callback=self.parse_tuandan, headers=response.headers, cookies=meta['cookie'],
                                  meta=meta, dont_filter=True)

    def parse_browse(self, response):
        # print response.body
        data = re.findall('disabled([\s\S]*?)disabled', response.body)
        data = ''.join(data)
        data = re.findall('<option value="(\d+)"', data)
        meta = response.meta

        if data:
            for deal_id in data:
                meta['deal_id'] = deal_id

                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                # url = 'https://e.dianping.com/receiptreport/dealview?selectedDealGroupId=' + str(
                #     deal_id) + '&status=0&selectedBeginDate=2015-09-11&selectedEndDate=2018-09-14'
                url = 'https://e.dianping.com/receiptreport/dealview?selectedDealGroupId=' + str(
                    deal_id) + '&status=0&selectedBeginDate=' + yesterday + '&selectedEndDate=' + yesterday
                tmp_header = _header
                tmp_header['Referer'] = 'https://e.dianping.com/tuanreceipt/dealsale'

                yield Request(url=url, callback=self.parse_browse_count, meta=meta, dont_filter=True, headers=_header,
                              cookies=meta['cookie'])

    def parse_browse_count(self, response):
        pattern = '"calDate":"(.*?)","count":(\d+)}'
        data = re.findall(pattern, response.body)
        print data
        tasktime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if data:
            for d in data:
                item = CalDateCountItem()
                item['calDate'] = d[0]
                item['calCount'] = d[1]
                item['tasktime'] = tasktime
                item['deal_id'] = response.meta['deal_id']
                yield item







