# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector
import re
import web
import json
import datetime
import time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding( "utf-8" )
db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')

def get_url_list():
    sql = "select star_name,star_id from hillinsight.toutiao_star"
    print sql
    res = db.query(sql)
    return res

class MemonetSpider(scrapy.Spider):
    name = "toutiao_memonet"
    allowed_domains = ["baidu.com"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self._dt = datetime.date.today().strftime("%Y-%m-%d")
    
    def start_requests(self):
        for row in self.url_info:
            url = 'http://isub.snssdk.com/dongtai/list/v8/?version_code=5.8.3&app_name=news_article&vid=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&device_id=33596351322&channel=App%20Store&resolution=750*1334&aid=13&ab_version=86574,83096,77079,79286,87750,87331,88106,87982,88398,88303,88700,87881,82679,88185,88695,87355,87835,88283,87505,88302,88444,87827,88322,87502,87988&ab_feature=z1&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&live_sdk_version=1.3.0&idfv=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=6084034225&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=06066E4A-F204-4037-B473-FF6DD068F35F&count=20&min_cursor=0&screen_width=750&source=6&user_id='+row['star_id']
            yield scrapy.FormRequest(url,
                            callback = self.parse_item,
                            meta = {'star_name':row['star_name'], 'star_id':row['star_id'],
                                    'url':url, 'count':'0'},
                            dont_filter = True,
                            )

    def parse_followers_item(self,  response):
        try:
            json_follow = json.loads(response.body)
            followers = json_follow['data']['followers_count']
        except:
            followers = 0
        item = response.meta['item']
        item['followers'] = followers
        yield item

    def check_need_retry(self, response):
        if BeautifulSoup(response.body,"lxml").find(text=re.compile(u'请输入验证码')) != None:    
            return True
        if response.body.find(':') == -1:
            return True
        try:
            json_resp = json.loads(response.body)
        except:
            return True
        return False

    def parse_item(self, response):
        if not self.check_need_retry(response):
            json_resp = json.loads(response.body)
            has_more = json_resp['data']['has_more']
            max_cursor = json_resp['data']['max_cursor']
            if has_more == True:
                url_new = 'http://isub.snssdk.com/dongtai/list/v8/?version_code=5.8.3&app_name=news_article&vid=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&device_id=33596351322&channel=App%20Store&resolution=750*1334&aid=13&ab_version=86574,83096,77079,79286,87750,87331,88106,87982,88398,88303,88700,87881,82679,88185,88695,87355,87835,88283,87505,88302,88444,87827,88322,87502,87988&ab_feature=z1&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&live_sdk_version=1.3.0&idfv=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=6084034225&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=06066E4A-F204-4037-B473-FF6DD068F35F&count=20&max_cursor='+str(max_cursor)+'&screen_width=750&source=6&user_id='+response.meta['star_id']
                response.meta['count'] = '0'
                data = response.meta
                yield scrapy.FormRequest(url_new,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )

            followers = 0
            if not json_resp['data']['data']:
                item = {'star_name': response.meta['star_name'],
                        'followers': followers,
                        'create_time':'',
                        'content':'',
                        'memo_id':'',
                        'comment_count':'',
                        'digg_count':'', 
                        'item_type':'',
                        'getdate': self._dt,}
                follow_url = 'http://isub.snssdk.com/2/user/profile/v2/?version_code=5.8.3&app_name=news_article&vid=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&device_id=33596351322&channel=App%20Store&resolution=750*1334&aid=13&ab_version=86574,83096,77079,79286,87750,87331,88106,87982,88398,88303,88700,87881,82679,88185,88695,87355,87835,88283,87505,88302,88444,87827,88322,87502,87988&ab_feature=z1&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&live_sdk_version=1.3.0&idfv=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=6084034225&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=06066E4A-F204-4037-B473-FF6DD068F35F&aid=13&app_name=news_article&device_id=33596351322&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&user_id='+response.meta['star_id']
                data = {'item':item}
                yield scrapy.FormRequest(follow_url,
                            callback = self.parse_followers_item,
                            meta = data,
                            dont_filter = True,
                            )
            else:
                for item_list in json_resp['data']['data']:
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item_list['create_time']))
                    item = {'star_name': response.meta['star_name'],
                            'followers': followers,
                            'create_time': create_time,
                            'content': item_list['content'],
                            'memo_id': item_list['id'],
                            'comment_count': item_list['comment_count'],
                            'digg_count': item_list['digg_count'],
                            'item_type': item_list['item_type'],
                            'getdate': self._dt,}
                    follow_url = 'http://isub.snssdk.com/2/user/profile/v2/?version_code=5.8.3&app_name=news_article&vid=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&device_id=33596351322&channel=App%20Store&resolution=750*1334&aid=13&ab_version=86574,83096,77079,79286,87750,87331,88106,87982,88398,88303,88700,87881,82679,88185,88695,87355,87835,88283,87505,88302,88444,87827,88322,87502,87988&ab_feature=z1&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&live_sdk_version=1.3.0&idfv=C353EC66-C05A-44DA-B6C7-29C6EE134B7D&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=6084034225&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=06066E4A-F204-4037-B473-FF6DD068F35F&aid=13&app_name=news_article&device_id=33596351322&openudid=18b4c8fc33523b8f8572693f6e2896708f8f4339&user_id='+response.meta['star_id']
                    data = {'item':item}
                    yield scrapy.FormRequest(follow_url,
                            callback = self.parse_followers_item,
                            meta = data,
                            dont_filter = True,
                            )
        else:
            if int(response.meta['count']) > 3:
                print "*******toutiao-momentovercount:%s"%response.meta['count']
                pass
            else:
                count = str(int(response.meta['count']) + 1)
                print "toutiao_mement retry count *****:%s"%(response.meta['url'], count)
                response.meta['count'] = count
                data = response.meta
                yield scrapy.FormRequest(response.meta['url'],
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )