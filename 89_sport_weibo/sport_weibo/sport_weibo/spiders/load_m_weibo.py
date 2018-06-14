# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
import math
import json
import datetime
import web
import urllib
from bs4 import BeautifulSoup
from sport_weibo.items import LoadContentItem


_headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Referer": ""
}


def get_url_list():
    sql = "select name,weibo_uid from qfliu.tt_v_bang_xinglang_weibo;"
    db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')
    res = db.query(sql)
    return res

class LoadMWeiboSpider(scrapy.Spider):
    name = "load_m_weibo"
    allowed_domains = ["m.weibo.cn"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self._dt = datetime.date.today().strftime("%Y-%m-%d")

    def start_requests(self):
        for row in self.url_info:
            url = "http://m.weibo.cn/container/getIndex?containerid=230413" + row[
                "weibo_uid"] + "_-_WEIBO_SECOND_PROFILE_MORE_WEIBO"
            refer = 'http://m.weibo.cn/p/index?containerid=230413' + row[
                'weibo_uid'] + '_-_WEIBO_SECOND_PROFILE_MORE_WEIBO&title='
            tmp_headers = _headers
            tmp_headers['Referer'] = refer
            yield scrapy.FormRequest(url,
                                     headers=_headers,
                                     callback=self.parse_item,
                                     meta={'star_name': row['name'],
                                           'weibo_uid': row['weibo_uid'],
                                           'refer': refer,
                                           'url': url, 'count': '0'},
                                     dont_filter=True,
                                     )

    def check_need_retry(self, response):
        if BeautifulSoup(response.body, "lxml").find(text=re.compile(u'请输入验证码')) != None:
            return True
        try:
            json_resp = json.loads(response.body)
            if json_resp['cardlistInfo']['total'] == None:
                return True
        except:
            return True
        return False

    def parse_item(self, response):
        if not self.check_need_retry(response):
            json_resp = json.loads(response.body)
            total_number = json_resp['cardlistInfo']['total']
            if response.meta['url'].find('page') == -1:
                for page_i in range(2, int(math.ceil(total_number / 10)) + 2):
                    payload = {
                        'containerid': '230413' + response.meta['weibo_uid'] + '_-_WEIBO_SECOND_PROFILE_MORE_WEIBO',
                        'page': page_i}
                    url_new = 'http://m.weibo.cn/container/getIndex?'
                    url_new = url_new + urllib.parse.urlencode(payload)
                    data = {'url': url_new, 'count': '0',
                            'star_name': response.meta['star_name'],
                            'weibo_uid': response.meta['weibo_uid']
                            }
                    yield scrapy.FormRequest(url_new,
                                             callback=self.parse_item,
                                             meta=data,
                                             dont_filter=True,
                                             )
            json_resp = json.loads(response.body)
            for sta_list in json_resp['cards']:
                if 'mblog' in sta_list:
                    weibo_id = sta_list['mblog']['id']
                    created_at = sta_list['mblog']['created_at']
                    if created_at.find(u'分钟') > -1:
                        created_at = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    if len(created_at) < 13:
                        created_at = str(datetime.date.today().year) + '-' + created_at
                    created_at = created_at.replace(u'今天', str(datetime.date.today().month) + '-' + str(
                        datetime.date.today().day))
                    weibo_text = sta_list['mblog']['text']
                    user_id = sta_list['mblog']['user']['id']
                    followers_count = sta_list['mblog']['user']['followers_count']
                    follow_count = sta_list['mblog']['user']['follow_count']
                    statuses_count = sta_list['mblog']['user']['statuses_count']
                    urank = sta_list['mblog']['user']['urank']
                    if 'retweeted_status' in sta_list:
                        retweeted_id = sta_list['mblog']['retweeted_status']['id']
                        retweeted_text = sta_list['mblog']['retweeted_status']['text']
                    else:
                        retweeted_id = None
                        retweeted_text = None
                    reposts_count = sta_list['mblog']['reposts_count']
                    comments_count = sta_list['mblog']['comments_count']
                    attitudes_count = sta_list['mblog']['attitudes_count']
                    if response.meta['weibo_uid'] == str(user_id):
                        item=LoadContentItem()
                        item.update( {'star_name': response.meta['star_name'],
                                'weibo_id': weibo_id,
                                'created_at': created_at,
                                'weibo_text': weibo_text,
                                'followers_count': followers_count,
                                'follow_count': follow_count,
                                'statuses_count': statuses_count,
                                'urank': urank,
                                'retweeted_id': retweeted_id,
                                'retweeted_text': retweeted_text,
                                'reposts_count': reposts_count,
                                'comments_count': comments_count,
                                'attitudes_count': attitudes_count,
                                'url': response.meta['url'],
                                'getdate': self._dt, })
                        yield item

        else:
            if int(response.meta['count']) > 5:
                print("*******weibo_list-overcount:%s" % response.meta['count'])
                pass
            else:
                count = str(int(response.meta['count']) + 1)
                print("url:%s count *****:%s" % (response.meta['url'], count))
                response.meta['count'] = count
                data = response.meta
                if data.has_key('refer'):
                    tmp_headers = _headers
                    tmp_headers['Referer'] = data['refer']
                    yield scrapy.FormRequest(response.meta['url'],
                                             headers=tmp_headers,
                                             callback=self.parse_item,
                                             meta=data,
                                             dont_filter=True,
                                             )
                else:
                    yield scrapy.FormRequest(response.meta['url'],
                                             callback=self.parse_item,
                                             meta=data,
                                             dont_filter=True,
                                             )
    
    
    