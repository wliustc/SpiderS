# -*- coding: utf-8 -*-
import datetime
import scrapy
import json, urllib
from scrapy import Request
import web
from qianfan.items import QianfanDetailItem

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
task_date = datetime.date.today().strftime("%Y-%m-%d")

# 人均行为分析（人均启动次数，人均使用时长）


data_class_dic = {
    'node_activeness_count': "分时活跃用户",
    'node_launch_count': "分时启动次数",
    'node_runtime_time': "分时使用时长",
    'node_activeness_averaged_count': "分时人均启动次数",
    'node_activeness_averaged_time': "分时人均使用时长",
    'node_activeness_absolute_permeability': "分时绝对渗透率",
    'node_activeness_relative_permeability': "分时相对渗透率"
}


class QfSpider(scrapy.Spider):
    name = "qf_user_time_sharing_behavior"
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
                print date
                for arith in [2,3]:
                    url = 'http://qianfan.analysys.cn/qianfan/app/appIntervalIndexList?' \
                          'appIds=%s&categoryIds=%s&arithId=%s' \
                          '&indexTypes=node_activeness_count,node_launch_count,' \
                          'node_runtime_time,node_activeness_averaged_count,' \
                          'node_activeness_averaged_time,' \
                          'node_activeness_absolute_permeability,' \
                          'node_activeness_relative_permeability&menuCode=2002002' \
                          '&dateType=&startDate=%s&endDate=%s' % (
                              appid, cateid,arith, date[0], date[1])
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
        meta = response.meta
        item['content'] = content
        item['meta'] = meta
        yield item
