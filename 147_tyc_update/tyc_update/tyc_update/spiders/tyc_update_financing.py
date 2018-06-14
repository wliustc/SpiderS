# -*- coding: utf-8 -*-
import json

import scrapy
import time
import web
from scrapy import Request
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {
            'Authorization': 'E2F9d42vNqlL'
        }

class TycUpdateFinancingSpider(scrapy.Spider):
    name = "tyc_update_financing"
    allowed_domains = ["open.api.tianyancha.com"]
    # start_urls = ['http://open.api.tianyancha.com/']

    def start_requests(self):
        data = db.query("select distinct company_name from "
                        "t_spider_hillhousecap_update_financing where company_name!='';")
        for d in data:
            company_name = d.get('company_name')
            # 融资历史
            url_findHistoryRongzi = 'https://open.api.tianyancha.com/services/v4/open/findHistoryRongzi.json?name=%s' % company_name
            yield Request(url_findHistoryRongzi,callback=self.parse_findHistoryRongzi,headers=headers,meta={'company_name':company_name})

            # 对外投资
            url_inverst = 'https://open.api.tianyancha.com/services/v4/open/inverst.json?name=%s' % company_name
            yield Request(url_inverst, callback=self.parse_inverst, headers=headers,meta={'company_name':company_name})

            # 投资事件
            url_findTzanli = 'https://open.api.tianyancha.com/services/v4/open/findTzanli.json?name=%s' % company_name
            yield Request(url_findTzanli, callback=self.parse_findTzanli, headers=headers,meta={'company_name':company_name})
        # url = 'https://open.api.tianyancha.com/services/v4/open/findTzanli.json?name=北京百度网讯科技有限公司'
        # yield Request(url, callback=self.parse_findTzanli, headers=headers)

    def parse_findHistoryRongzi(self, response):
        company_name = response.meta['company_name']
        try:
            data_json = json.loads(response.body)
            result = data_json.get('result')
            if result:
                items = result.get('items')
                if items:
                    for item in items:
                        result = {}
                        companyId = item.get('companyId')
                        companyName = item.get('companyName')
                        investorName = item.get('investorName')
                        money = item.get('money')
                        round = item.get('round')
                        date = item.get('date')
                        timeStr = time.strftime("%Y-%m-%d", time.localtime(date / 1000))
                        result['financing_year'] = timeStr
                        result['company_id'] = companyId
                        result['company_name'] = companyName
                        result['financing_participants'] = investorName
                        result['financing_amountunit'] = money
                        result['financing_lun'] = round
                        result['dt'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                        db.insert('t_spider_hillhousecap_tyc_financing', **result)
                    if len(items)==20:
                        url_list = response.url.split('&pageNum=')
                        if len(url_list)>1:
                            pageNum = int(url_list[1])+1
                            url_findHistoryRongzi = url_list[0]+'&pageNum=%s' % pageNum
                            yield Request(url_findHistoryRongzi, callback=self.parse_findHistoryRongzi, headers=headers,meta=response.meta)
                        else:
                            url_findHistoryRongzi = response.url + '&pageNum=2'
                            yield Request(url_findHistoryRongzi, callback=self.parse_findHistoryRongzi, headers=headers,meta=response.meta)
                else:
                    result = {}
                    result['company_name'] = company_name
                    result['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    db.insert('t_spider_hillhousecap_tyc_financing', **result)

        except Exception, e:
            print e

    def parse_inverst(self, response):
        company_name = response.meta['company_name']
        try:
            data_json = json.loads(response.body)
            result = data_json.get('result')
            if result:
                items = result.get('items')
                if items:
                    for item in items:
                        result = {}
                        orgType = item.get('orgType')
                        business_scope = item.get('business_scope')
                        percent = item.get('percent')
                        regStatus = item.get('regStatus')
                        estiblishTime = item.get('estiblishTime')
                        legalPersonName = item.get('legalPersonName')
                        type = item.get('type')
                        pencertileScore = item.get('pencertileScore')
                        legalPersonId = item.get('legalPersonId')
                        amount = item.get('amount')
                        id = item.get('id')
                        category = item.get('category')
                        regCapital = item.get('regCapital')
                        name = item.get('legalPnameersonId')
                        base = item.get('base')
                        creditCode = item.get('creditCode')
                        personType = item.get('personType')
                        result['orgType'] = orgType
                        result['business_scope'] = business_scope
                        result['percent'] = percent
                        result['regStatus'] = regStatus
                        result['estiblishTime'] = estiblishTime
                        result['legalPersonName'] = legalPersonName
                        result['type'] = type
                        result['pencertileScore'] = pencertileScore
                        result['legalPersonId'] = legalPersonId
                        result['amount'] = amount
                        result['company_id'] = id
                        result['category'] = category

                        result['regCapital'] = regCapital
                        result['name'] = name
                        result['base'] = base
                        result['creditCode'] = creditCode
                        result['personType'] = personType
                        result['company_name'] = company_name
                        result['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        db.insert('t_spider_hillhousecap_tyc_investments', **result)
                    if len(items)==20:
                        url_list = response.url.split('&pageNum=')
                        if len(url_list)>1:
                            pageNum = int(url_list[1])+1
                            url_inverst = url_list[0]+'&pageNum=%s' % pageNum
                            yield Request(url_inverst, callback=self.parse_inverst, headers=headers,meta=response.meta)
                        else:
                            url_inverst = response.url + '&pageNum=2'
                            yield Request(url_inverst, callback=self.parse_inverst, headers=headers,meta=response.meta)

        except Exception, e:
            print e

    def parse_findTzanli(self, response):
        company_name = response.meta['company_name']
        try:
            data_json = json.loads(response.body)
            result = data_json.get('result')
            if result:
                items = result.get('items')
                if items:
                    for item in items:
                        result = {}
                        result['company'] = item.get('company')
                        result['company_id'] = item.get('company_id')
                        result['graph_id'] = item.get('graph_id')
                        result['location'] = item.get('location')
                        result['yewu'] = item.get('yewu')
                        result['hangye1'] = item.get('hangye1')
                        result['iconOssPath'] = item.get('iconOssPath')
                        result['tzdate'] = time.strftime("%Y-%m-%d", time.localtime(item.get('tzdate') / 1000))
                        result['isDeleted'] = item.get('isDeleted')
                        result['product'] = item.get('product')
                        result['money'] = item.get('money')
                        result['lunci'] = item.get('lunci')
                        result['rongzi_map'] = item.get('rongzi_map')
                        result['organization_name'] = item.get('organization_name')
                        result['personType'] = item.get('personType')
                        result['icon'] = item.get('icon')
                        result['company_name'] = item.get('company_name')
                        result['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        db.insert('t_spider_hillhousecap_tyc_investments_incident', **result)
                    if len(items)==20:
                        url_list = response.url.split('&pageNum=')
                        if len(url_list)>1:
                            pageNum = int(url_list[1])+1
                            url_findTzanli = url_list[0]+'&pageNum=%s' % pageNum
                            yield Request(url_findTzanli, callback=self.parse_findTzanli, headers=headers,meta=response.meta)
                        else:
                            url_findTzanli = response.url + '&pageNum=2'
                            yield Request(url_findTzanli, callback=self.parse_findTzanli, headers=headers,meta=response.meta)

        except Exception, e:
            print e
