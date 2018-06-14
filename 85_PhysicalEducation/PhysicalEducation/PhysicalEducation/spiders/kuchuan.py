# -*- coding: utf-8 -*-
import re

import scrapy
import json
import re
import time
from scrapy import Request
from PhysicalEducation.items import KuChuanItem
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

app_package = {
    '腾讯体育': 'com.tencent.qqsports',
    '聚力体育': 'com.pplive.androidphone.sport',
    '懂球帝': 'com.dongqiudi.news',
    '虎扑体育': 'com.hupu.games',
    'Keep': 'com.gotokeep.keep',
    '悦动圈': 'com.yuedong.sport',
    '咕咚': 'com.codoon.gps',
    '乐动力': 'cn.ledongli.ldl',
    '悦跑圈': 'co.runner.app',
    '咪咕善跑': 'com.imohoo.shanpao',
    '黑鸟单车': 'com.bamboo.ibike'
}

header = {
    'Host': 'android.kuchuan.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


class KuchuanSpider(scrapy.Spider):
    name = "kuchuan"
    allowed_domains = ["kuchuan.com"]
    start_urls = ['http://kuchuan.com/']

    def start_requests(self):
        for key, val in app_package.items():
            # item = KuChuanItem()
            url = "http://android.kuchuan.com/histortydailydownload?packagename" \
                  "=%s&start_date=&end_date=&longType=365-d&date=%s" % (val, (str(time.time()) + '0').replace('.', ''))
            # yield Request(url,self.parse,meta={'app_name':key},headers=header)
            # dcap = dict(DesiredCapabilities.PHANTOMJS)
            # dcap["phantomjs.page.settings.userAgent"] = (
            #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
            # dcap["phantomjs.page.settings.Host"] = ("android.kuchuan.com")
            # dcap["phantomjs.page.settings.Referer"] = (
            #     "http://android.kuchuan.com/page/detail/download?package=%s&infomarketid=1&site=0" % val)
            # driver = webdriver.PhantomJS(desired_capabilities=dcap,
            #                              service_args=['--load-images=no', '--disk-cache=yes',
            #                                            '--ignore-ssl-errors=true'])
            # # driver = webdriver.PhantomJS()
            # driver.get(
            #     'http://android.kuchuan.com/page/detail/download?package=%s&infomarketid=1&site=0#!/day/%s' % (
            #     val, val))
            # time.sleep(1)
            # driver.get(
            #     "http://android.kuchuan.com/histortydailydownload?packagename="
            #     "%s&start_date=&end_date=&longType=365-d&date=%s" % (
            #     val, (str(time.time()) + '0').replace('.', '')))
            # data = driver.page_source
            # driver.close()
            # # driver.quit()
            # print key,data
            # item['response_content'] = data
            #
            # time.sleep(3)
            yield Request(url, callback=self.parse, meta={'app_name': key, 'package': val},dont_filter=True)
            time.sleep(10)

    def parse(self, response):
        # content_json = json.loads(response.body)
        # data = content_json.get('data')
        # if data:
        #     total = 0
        #     for d, num in data.items():
        #         total = total + int(num)
        #         print total
        status = ''.join(re.findall('"status":(.*?),',response.body))
        if int(status)==300:
            yield Request(response.url, callback=self.parse, meta=response.meta,dont_filter=True)
        else:
            item = KuChuanItem()
            item['response_content'] = response.body
            yield item


    