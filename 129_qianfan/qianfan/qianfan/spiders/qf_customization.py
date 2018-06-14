# coding=utf8

# 易观千帆定制版，按月度进行抓取

import time

import datetime
import scrapy
import json, urllib
from scrapy import Request
import web
from qianfan.items import QianfanCustomizationItem

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

# app名称，appid，app分类
app_data = [
    ['乐刻运动', '3656277', '1371278'],
    ['运动世界校园版', '3415038', '1251241'],
    ['光猪圈', '3192273', '1371278'],
    ['小熊快跑', '3108121', '3201066'],
    ['Keep', '3009210', '1371278'],
    ['FitTime-即刻运动', '2935386', '1371278'],
    ['悦动圈', '2814381', '1371278'],
    ['悦跑圈', '2693233', '1371278'],
    ['动动', '2672062', '1371278'],
    ['轻加', '2603461', '1371278'],
    ['乐动力', '2037797', '1371278'],
    ['每日瑜伽', '2031556', '1371278'],
    ['咕咚', '2031042', '1261246'],
    ['nike+runclub（Nike+ Running）', '2013511', '1371278'],
    ['niketranning（Nike+ Training Club）', '2013510', '137127'],
    ['快快减肥', '3188237', '1371278']]

#app_data = [
#	['快快减肥', '3188237', '1371278'],
#]

date_now = time.strftime('%Y/%m/01', time.localtime(time.time()))
date_now1 = datetime.datetime.strptime(date_now, '%Y/%m/%d')
date_now = (date_now1.replace(day=1) - datetime.timedelta(1)).replace(day=1)
# 上个月的日期
#date_now = date_now.strftime('%Y/%m/%d')

date_now = '2018/04/01'



class QfSpider(scrapy.Spider):
    name = "qf_customization"
    allowed_domains = ["qianfan.analysys.cn"]

    # start_urls = ['http://qianfan.analysys.cn/']

    def start_requests(self):
        for app in app_data:
            appId = app[1]
            appCate = app[2]

            # 综合数据
            synthesize_url = 'http://qianfan.analysys.cn/qianfan/app/indexBaseInfo?' \
                             'appIds=%s&categoryIds=%s&dateValue=%s' % \
                             (appId, appCate, date_now)
            yield Request(synthesize_url, callback=self.parse_synthesize)

            # 用户分布（性别分布，年龄分布，消费能力分布，地域分布，设备分布）
            user_url = 'http://qianfan.analysys.cn/qianfan/app/monthUserProfiles?' \
                       'appIds={}&dateValue={}&menuCode=2004001' \
                       '&orderStr=profileId&orderType=asc&parentProfileIdS=' \
                       '21000%2C11000%2C31000%2C41000%2C51000%2C' \
                       '81000%2C71000%2C61000'.format(appId, date_now)
            yield Request(user_url, callback=self.parse_user)

            # app渠道分布
            channel_url = 'http://qianfan.analysys.cn/qianfan/app/appChannelRefList?' \
                          'appIds=%s&menuCode=2004003&statDate=%s' % (appId, date_now)
            yield Request(channel_url, callback=self.parse_channel)

            # 分时活跃人数，分时启动次数，分时使用时长
            time_share_url = 'http://qianfan.analysys.cn/qianfan/app/' \
                             'appIntervalIndexList?appIds=%s&arithId=' \
                             '&categoryIds=%s&endDate=%s&' \
                             'indexTypes=node_runtime_time,node_launch_count,' \
                             'node_activeness_count&menuCode=2002002&' \
                             'startDate=%s' % (appId, appCate, date_now, date_now)
            yield Request(time_share_url, callback=self.parse_time_share)

    # 采集综合数据
    def parse_synthesize(self, response):
        item = QianfanCustomizationItem()
        item['content'] = response.body
        item['meta'] = response.meta
        item['category_type'] = 'synthesize'
        yield item

    # 采集用户分布（性别分布，年龄分布，消费能力分布，地域分布，设备分布）
    def parse_user(self, response):
        item = QianfanCustomizationItem()
        item['content'] = response.body
        item['meta'] = response.meta
        item['category_type'] = 'user'
        yield item

    # 采集app渠道分布
    def parse_channel(self, response):
        item = QianfanCustomizationItem()
        item['content'] = response.body
        item['meta'] = response.meta
        item['category_type'] = 'channel'
        yield item

    # 采集分时活跃人数，分时启动次数，分时使用时长
    def parse_time_share(self, response):
        item = QianfanCustomizationItem()
        item['content'] = response.body
        item['meta'] = response.meta
        item['category_type'] = 'time_share'
        yield item

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    