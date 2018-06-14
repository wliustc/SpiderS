# -*- coding: utf-8 -*-
import datetime
import scrapy
import json, urllib
from scrapy import Request
import web
from qianfan.items import QianfanDetailItem

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
task_date = datetime.date.today().strftime("%Y-%m-%d")

uu = 'http://qianfan.analysys.cn/qianfan/app/appIndexList?appIds=3009210&arithId=3&menuCode=2001002&categoryIds=1371278&indexType=launch_avg_day,active_avg_day,runtime_avg_day&dateType=month&startDate=2017%2F01%2F01&endDate=2017%2F10%2F26'
# 用户粘性分析（月度）（人均单日启动次数，人均单日使用时长，用户活跃度，次月留存率,人均启动次数（月度）,人均使用时长（月度））
class QfSpider(scrapy.Spider):
    name = "qf_avg_day_scale"
    allowed_domains = ["qianfan.analysys.cn"]

    # start_urls = ['http://qianfan.analysys.cn/']

    def start_requests(self):
        date_list = [('2017/01/01', '2017/12/31'), ('2016/01/01', '2016/12/31'), ('2015/01/01', '2015/12/31'),
                     ('2014/01/01', '2014/12/31')]
        data = db.query('select distinct cateId,appId from t_spider_qianfan_yuedu;')
        for d in data:
            cateid = d.get('cateId')
            appid = d.get('appId')
            for date in date_list:
                url = 'http://qianfan.analysys.cn/qianfan/app/appIndexList?' \
                      'appIds=%s&arithId=&menuCode=2001002&categoryIds=%s' \
                      '&indexType=launch_avg_day,active_avg_day,runtime_avg_day' \
                      '&dateType=month&startDate=%s&endDate=%s' % (
                          appid, cateid, date[0], date[1])
                print url
                yield Request(url, callback=self.parse, meta={'url': url, 'dt': task_date})
                    # url = 'http://qianfan.analysys.cn/qianfan/app/appIndexList?appIds=2028109&arithId=&menuCode=2001001&categoryIds=1091092&indexType=active_nums&dateType=day&startDate=2016/10/13&endDate=2017/10/12'
                    # yield Request(url, callback=self.parse, meta={'classes': ('active_nums', '活跃用户'),
                    #                                               'date_class': ('day', '日'),
                    #                                               'url': url,'dt':task_date})

    # 采集千帆app详细信息
    def parse(self, response):
        item = QianfanDetailItem()
        content = response.body

        item['content'] = content
        item['meta'] = response.meta
        yield item
