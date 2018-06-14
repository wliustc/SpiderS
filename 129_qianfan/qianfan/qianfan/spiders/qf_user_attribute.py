# coding=utf8

# 用户属性（性别分布、年龄分布、消费能力分布、地域分布、品牌分布、运营商分布）
import datetime
import scrapy
import json, urllib
from scrapy import Request
import web
from qianfan.items import QianfanDetailItem

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
task_date = datetime.date.today().strftime("%Y-%m-%d")


start_date = '2017/09/01'

class QfSpider(scrapy.Spider):
    name = "qf_user_attribute"
    allowed_domains = ["qianfan.analysys.cn"]

    # start_urls = ['http://qianfan.analysys.cn/']

    def start_requests(self):

        data = db.query('select distinct appId from t_spider_qianfan_yuedu;')
        for d in data:
            appid = d.get('appId')

            url = 'http://qianfan.analysys.cn/qianfan/app/monthUserProfiles?' \
                  'appIds=%s&menuCode=2004001&parentProfileIdS=21000,11000,' \
                  '31000,41000,51000,61000,71000,81000&dateValue=%s&orderStr=profileId&orderType=asc' % (
                      appid, start_date)
            print url
            yield Request(url, callback=self.parse, meta={
                'appid': appid,
                'url': url, 'dt': task_date,'date_':start_date})

        # url = 'http://qianfan.analysys.cn/qianfan/app/monthUserProfiles?appIds=3009210&menuCode=2004001&parentProfileIdS=21000,11000,31000,41000,51000,81000&dateValue=2017/09/01&orderStr=profileId&orderType=asc'
        # yield Request(url, callback=self.parse, meta={'appid': '3009210',
        #                                               'date_': start_date,
        #                                               'url': url,'dt':task_date})

    # 采集千帆app用户属性
    def parse(self, response):

        content = response.body
        content_json = json.loads(content)
        datas = content_json.get('datas')
        if datas:
            echarts = datas.get('echarts')
            if echarts:
                next_page_sign = 0
                echarts = echarts[0]
                meta = response.meta
                for echart_key, echart_val in echarts.items():
                    if 'app' not in echart_key:
                        if echart_val:
                            next_page_sign = 1
                            item = QianfanDetailItem()


                            item['content'] = content
                            item['meta'] = meta

                            yield item
                            break

                if next_page_sign:
                    date_ = meta['date_']
                    now = datetime.datetime.strptime(date_, '%Y/%m/%d')
                    date_1 = (now.replace(day=1) - datetime.timedelta(1)).replace(day=1)
                    date_1 = date_1.strftime('%Y/%m/%d')
                    url = response.url.replace(date_, date_1)
                    print url
                    meta['date_'] = date_1
                    meta['retry_times'] = 0
                    meta['url'] = url
                    yield Request(url, callback=self.parse, meta=meta)
    