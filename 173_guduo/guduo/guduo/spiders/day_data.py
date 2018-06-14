# -*- coding: utf-8 -*-
import scrapy
import random
import json
import time
import sys
import re
from guduo.items import GuduoItem

reload(sys)
import datetime

sys.setdefaultencoding('utf-8')
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'User-Agent,Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'User-Agent,Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent,Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
]
dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))


class DayDataSpider(scrapy.Spider):
    name = 'day_data'
    handle_httpstatus_list = [502]

    # allowed_domains = ['http://data.guduomedia.com/']
    # start_urls = ['http://http://data.guduomedia.com//']
    def start_requests(self):
        # http://data.guduomedia.com/show/datalist?category=DRAMA&date=2018-04-14&t=1526289356173
        category_list = ['DRAMA', 'VARIETY', 'NETWORK_DRAMA', 'NETWORK_VARIETY', 'TV_DRAMA', 'TV_VARIETY']
        # category_list = ['DRAMA']
        for i in category_list:
            # start_time = '2016-09-01'
            # end_time = self.getYesterday()
            # num, start_time = self.time_zhaunhuan(start_time, end_time)
            # for x in xrange(0, num+1):
            # time = start_time + datetime.timedelta(days=x)
            # time = str(time)
            # activity_time = re.search(r'\d+-\d+-\d+', time)
            # if activity_time:
            # activity_time = activity_time.group()
            url = 'http://data.guduomedia.com/show/datalist?category=' + i + '&date=' + self.getYesterday()
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            yield scrapy.Request(url, headers=headers,
                                 meta={'category': i, 'datetimes': self.getYesterday(), 'url': url}, dont_filter=True)


    def parse(self, response):
        meta = response.meta
        html = response.body
        json_obj = json.loads(html)
        data = json_obj.get('data')
        if data:
            dayBillboardList = data.get('dayBillboardList')
            if dayBillboardList:
                for i in dayBillboardList:
                    item = GuduoItem()
                    item['url'] = meta.get('url')
                    item['category'] = meta.get('category')
                    item['datetimes'] = meta.get('datetimes')
                    item['platformImgUrl'] = i.get('platformImgUrl')
                    item['today_play_count'] = i.get('today_play_count')
                    item['incType'] = i.get('incType')
                    item['directors'] = i.get('directors')
                    item['douban_score'] = i.get('douban_score')
                    item['episode'] = i.get('episode')
                    item['coverImgUrl'] = i.get('coverImgUrl')
                    item['duration'] = i.get('duration')
                    item['actors'] = i.get('actors')
                    item['showId'] = i.get('showId')
                    item['total_comment_count'] = i.get('total_comment_count')
                    item['market_share_ratio'] = i.get('market_share_ratio')
                    item['nowEpisode'] = i.get('nowEpisode')
                    item['release_date'] = i.get('release_date')
                    item['baidu_exponent'] = i.get('baidu_exponent')
                    item['dianshi_names'] = i.get('name')
                    item['increaseCount'] = i.get('increaseCount')
                    item['days'] = i.get('days')
                    item['platformName'] = i.get('platformName')
                    item['rise'] = i.get('rise')
                    item['ordinal'] = i.get('ordinal')
                    item['riseAbs'] = i.get('riseAbs')
                    item['dt'] = dt
                    yield item


    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")


    def time_zhaunhuan(self, start_time, end_time):
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        delta = end - start
        return delta.days, start




