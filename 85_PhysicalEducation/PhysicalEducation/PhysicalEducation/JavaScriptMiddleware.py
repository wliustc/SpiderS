# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import requests
from scrapy.downloadermiddlewares.stats import DownloaderStats
from selenium.webdriver import DesiredCapabilities
#
# global driver
# driver = webdriver.PhantomJS()  # 指定使用的浏览器，写在此处而不写在类中，是为了不每次调用都生成一个信息独享，减少内存使用
# print"PhantomJS is starting..."


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        # global driver
        # driver = webdriver.Firefox()
        meta = request._meta
        package = meta['package']
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0")
        dcap["phantomjs.page.settings.Host"] = ("android.kuchuan.com")
        dcap["phantomjs.page.settings.Referer"] = (
            "http://android.kuchuan.com/page/detail/download?package=%s&infomarketid=1&site=0" % package)

        driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                     service_args=['--load-images=no', '--disk-cache=yes', '--ignore-ssl-errors=true'])
        url = request.url;
        # driver.get(url)
        # time.sleep(1)
        driver.get('http://android.kuchuan.com/page/detail/download?package=%s&infomarketid=1&site=0#!/day/%s' % (package, package))
        # js = "var q=document.documentElement.scrollTop=10000"
        driver.get(url)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        # body = driver.page_source
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
        # headers = {'User-Agent': user_agent}
        # r = requests.post(url, headers=headers)
        body = driver.page_source
        # driver.close()
        # print("访问" + request.url)
        return HtmlResponse(url, encoding='utf-8', status=200, body=body)
        # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
