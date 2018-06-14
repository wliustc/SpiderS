# -*- coding: utf-8 -*-
import datetime
import scrapy
import json,urllib
from scrapy import Request
import web
from qianfan.items import QianfanDetailItem
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

# 开始时间应为最新的月度
start_date = '2017/09/01'

class QfSpider(scrapy.Spider):
    name = "qf_channel_ref"
    allowed_domains = ["qianfan.analysys.cn"]
    # start_urls = ['http://qianfan.analysys.cn/']

    def start_requests(self):
        data = db.query('select distinct cateId,appId from t_spider_qianfan_yuedu;')
        for d in data:
            appid = d.get('appId')

            url = 'http://qianfan.analysys.cn/qianfan/app/appChannelRefList?appIds='+appid+'&statDate='+start_date
            print url
            yield Request(url, callback=self.parse_list, meta={'date_': start_date})
        # url = 'http://qianfan.analysys.cn/qianfan/app/appChannelRefList?appIds=3009210&statDate=2017/09/01'
        # yield Request(url,callback=self.parse_list,meta={'date_':'2017/09/01'})

    def parse_list(self,response):
        content = json.loads(response.body)
        datas = content.get('datas')
        if datas:
            echarts = datas.get('echarts')
            if echarts:
                echarts = echarts[0]
                meta = response.meta
                channelList = echarts.get('channelList')
                if channelList:
                    item = QianfanDetailItem()
                    item['content'] = content
                    item['meta'] = meta
                    yield item

                    date_ = meta['date_']
                    if date_==start_date:
                        timeRange = datas.get('timeRange')
                        for tr in timeRange:
                            date_1 = tr.get('key')
                            url = response.url
                            url = url.replace(date_,date_1)
                            meta['date_'] = date_1
                            meta['retry_times'] = 0
                            meta['url'] = url
                            yield Request(url, callback=self.parse_list, meta=meta)