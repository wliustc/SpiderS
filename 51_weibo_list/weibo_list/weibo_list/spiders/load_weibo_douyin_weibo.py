# -*- coding: utf-8 -*-
import scrapy
import math
import datetime
import json
import time
from bs4 import BeautifulSoup
import MySQLdb
import re
import traceback
#from load_content.items import LoadContentItem

class LoadWeiboDouyinWeiboSpider(scrapy.Spider):
    name = "load_weibo_douyin_weibo"
    allowed_domains = ["m.weibo.cn"]
    start_urls = ['http://m.weibo.cn/']

    def start_requests(self):
        conn = MySQLdb.connect(host='localhost',port=13306, user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur=conn.cursor()
        cur.execute('select `username`,`weibo_id` from t_spider_weibo_userid where `type`="douyin";	')
        temp=cur.fetchall()
        cur.close()
        conn.close()
        self.url_info=temp
        for row in self.url_info:
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413%s_-_WEIBO_SECOND_PROFILE_WEIBO' %row['weibo_id']
            tmp_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Host':'m.weibo.cn',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }
            yield scrapy.Request(url,
                                     headers=tmp_headers,
                                     callback=self.parse_item,
                                     meta={'star_name': row['username'],'weibo_uid':row['weibo_id'],
                                    'url':url,'count': '0','type':'微博'},
                                     dont_filter=True,
                                     )
            break

    def check_need_retry(self, response):
        if response.status==302:
            return True
        if BeautifulSoup(response.body, "lxml").find(text=re.compile(u'请输入验证码')) != None:
            return True
        try:
            json_resp = json.loads(response.body)
            if json_resp['data']['cardlistInfo']['total'] == None:
                return True
        except Exception as e:
            traceback.print_exc()
            return True
        return False

    def parse_item(self, response):
        if not self.check_need_retry(response):
            json_resp = json.loads(response.body)
            total_number = json_resp['data']['cardlistInfo']['total']
            if response.meta['url'].find('page') == -1:
                for page_i in range(2, int(math.ceil(total_number / 10)) + 2):
                    url_new = 'https://m.weibo.cn/api/container/getIndex?containerid=230413%s_-_' \
                              'WEIBO_SECOND_PROFILE_WEIBO&page=%s' \
                              %(response.meta['weibo_uid'],page_i)
                    data = {'url': url_new, 'count': '0',
                            'star_name': response.meta['star_name'],
                            'weibo_uid': response.meta['weibo_uid'],
                            'type':response.meta['type']
                            }
                    yield scrapy.FormRequest(url_new,
                                             callback=self.parse_item,
                                             meta=data,
                                             dont_filter=True,
                                             )

            for sta_list in json_resp['data']['cards']:
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
                        item = {}
                        item.update({'star_name': response.meta['star_name'],
                                     'weibo_uid': response.meta['weibo_uid'],
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
                                     'getdate': time.strftime('%Y-%m-%d', time.localtime(time.time())), 'src': '抖音|%s' %response.meta['type']})
                        yield item

