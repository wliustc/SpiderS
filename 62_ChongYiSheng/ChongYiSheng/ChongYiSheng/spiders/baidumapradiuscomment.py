# -*- coding: utf-8 -*-
import datetime
import scrapy
import time
from scrapy import Request
from urlparse import urljoin
import re, json
from scrapy.selector import Selector
from ChongYiSheng.items import BaiDuMapDetailItem
from scrapy.loader.processors import MapCompose
import sys
from mysqlUtil import Mysql

reload(sys)
sys.setdefaultencoding('utf8')

ChongYiSheng_list = [
    ['47', '宠颐生沈阳爱克威分院', '6124971', '3969', '31971fe2143ce6d2583ac806'],
    ['48', '宠颐生沈阳瑞嘉分院', '23618362', '4331', 'fc244b885df5d9eb3010af51'],
    ['133', '宠颐生盘锦益友分院', '6007930', '3438','37c1f5349c2b2d80af31e5a6'],
    ['139', '宠颐生北京爱之都分院', '4663168', '2082','d52831f90c1803a72ffaa7e2'],
    ['140', '宠颐生北京爱福分院', '16092628', '1503', '53cebd509d13ab612a02e1e5'],
    ['141', '宠颐生北京爱佳分院', '1772629', '3064','37d60a4657fdce601e1d11f2'],
    ['142', '宠颐生成都宠福来分院', '43615785', '3788','f41c898455582cb2eaf8532d'],
    ['143', '萌家人成都九里堤分院', '67985395', '1863', '91c07762ffcab1e7471a32d5'],
    ['144', '萌家人成都牛市口分院', '27452514', '1875', '43dc0c1f24826608932ca3e7'],
    ['145', '萌家人成都高新一分院', '77333775', '1879','52d1b4cf3b26b2598c55ec25'],
    ['157', '宠颐生北京京冠分院', '36848655', '8582', '680fb703eb4c829c8ab988be'],
    ['158', '宠颐生北京爱之源分院', '13949683', '8597', '19778600e4f0020fd12dd626']
]

item_list = ['service_rating',
             'video_url',
             'quality_score',
             'cn_name',
             'taste_rating',
             'integral_award',
             'user_id',
             'sentiment',
             'favorNum',
             'content',
             'video_pic',
             'isAgree',
             'time_stamp',
             'effect_rating',
             'one_url_mobile',
             'overall_rating',
             'user_logo',
             'cmt_id',
             'user_url',
             'price',
             'agreeUserLogoUrl',
             'one_url',
             'nick_user_recommend',
             'date',
             'product_rating',
             'class_one',
             'src',
             'poi_id',
             'user_url_mobile',
             'comment_url_mobile',
             'pics',
             'environment_rating',
             'user_name',
             'video_time',
             'comment_url']

task_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class BaiDuMapSpider(scrapy.Spider):
    name = "baidumapradiuscomment"
    allowed_domains = ["baidu.com"]

    # start_urls = ['http://dianping.com/']

    def __init__(self, method='all',write_time='2017-03-28 18:00:00', *args, **kwargs):
        super(BaiDuMapSpider, self).__init__(*args, **kwargs)
        self.method = method
        self.write_time = write_time
        self.mysql = Mysql('10.15.1.24', 3306, 'writer', 'hh$writer', 'hillinsight', 'utf8')

    def start_requests(self):
        write_time_recent = self.mysql.getAll('select write_time from test_baidumapnear order by write_time desc limit 1;')
        if write_time_recent:
            self.write_time = write_time_recent[0]['write_time']
        print self.write_time
        informations_list = self.mysql.getAll(
            "select id,name,uid from test_baidumapnear where write_time='%s';" % self.write_time)
        for information_list in informations_list:
            # information_list = {}
            # # informations_list = ll.replace('\n', '').split(',')
            # if len(informations_list) > 4:
            #     information_list['id'] = informations_list[0]
            #     information_list['clinic_name'] = informations_list[1]
            #     information_list['dianping_id'] = informations_list[2]
            #     information_list['system_id'] = informations_list[3]
            #     information_list['uid'] = informations_list[4]
            print information_list
            yield Request(
                url='http://map.baidu.com/detail?qt=ugccmtlist&type=life&uid=%s'
                    '&from=mapiphone&pageIndex=1&pageCount=100&showPic=1&agree=1' %
                    information_list['uid'],
                callback=self.parse, meta={'information_list': information_list})

    def parse(self, response):
        information_list = response.meta['information_list']
        content = response.body
        # print content
        content_json = json.loads(content)
        print content_json
        comment = content_json.get('comment')
        if comment:
            comment_list = comment.get('comment_list')
            if comment_list:
                for comment_info in comment_list:
                    item = BaiDuMapDetailItem()
                    item['comment_avg_score'] = comment.get('comment_avg_score')
                    item['comment_num'] = comment.get('comment_num')
                    for key, value in comment_info.items():
                        if key in item_list:
                            if isinstance(value, (dict, list)):
                                value = json.dumps(value)
                            item[key] = value
                    # time.sleep(100)
                    item['write_time'] = task_time
                    item['hospital_name'] = information_list['name']
                    item['hospital_id'] = ''
                    item['hospital_system_id'] = ''
                    item['hospital_baidu_id'] = information_list['uid']
                    if str(self.method) == 'all':
                         yield Request('http://map.baidu.com/detail?qt=ninf&uid=%s&detail=life' % item['hospital_baidu_id'],
                                      callback=self.parse_score, meta={'item': item})

                        # yield item
                    else:
                        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                        comment_date = item['date']
                        comment_date = comment_date[:10]
                        if yesterday == comment_date:
                            yield Request('http://map.baidu.com/detail?qt=ninf&uid=%s&detail=life' % item['hospital_baidu_id'],
                                          callback=self.parse_score, meta={'item': item})

                            # yield item
    def parse_score(self,response):
        item = response.meta['item']
        score = re.findall('rate-num yahei">(.*?)</em>',response.body)
        if score:
            score=score[0]
            item['comment_avg_score'] = score
            yield item
        else:
            yield item
