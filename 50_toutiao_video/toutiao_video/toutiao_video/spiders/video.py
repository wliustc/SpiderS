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
    sql = "select star_name,star_video_link from hillinsight.toutiao_star"
    res = db.query(sql)
    return res

class VideoSpider(scrapy.Spider):
    name = "toutiao_video"
    allowed_domains = ["58.com"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self._dt = datetime.date.today().strftime("%Y-%m-%d")
    
    def start_requests(self):
        for row in self.url_info:
            url = 'http://www.toutiao.com/pgc/ma/?media_id='+row['star_video_link'].replace('http://www.toutiao.com/m','').replace('/','')+'&page_type=0&max_behot_time=0&count=10&version=2&platform=pc&as=479BB4B7254C150&cp=7E0AC8874BB0985'
            yield scrapy.FormRequest(url,
                            callback = self.parse_item,
                            meta = {'star_name':row['star_name'],
                                    'star_video_link':row['star_video_link'],
                                    'url':url, 'count':'0'},
                            dont_filter = True,
                            )

    def check_need_retry(self, response):
        if BeautifulSoup(response.body,"lxml").find(text=re.compile(u'请输入验证码')) != None:    
            return True        
        try:
            json_resp = json.loads(response.body)
            if json_resp['has_more'] == None:
                return True
        except:
            return True
        return False

    def parse_item(self, response):
        if not self.check_need_retry(response):
            json_resp = json.loads(response.body)
            has_more = json_resp['has_more']
            max_behot_time = str(json_resp['next']['max_behot_time'])
            if has_more == 1:
                url_new = 'http://www.toutiao.com/pgc/ma/?media_id='+response.meta['star_video_link'].replace('http://www.toutiao.com/m','').replace('/','')+'&page_type=0&max_behot_time='+max_behot_time+'&count=10&version=2&platform=pc&as=479BB4B7254C150&cp=7E0AC8874BB0985'
                data = {'url': url_new, 'count':'0',
                        'star_name': response.meta['star_name'],
                        'star_video_link': response.meta['star_video_link']
                        }
                yield scrapy.FormRequest(url_new,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )
            for data_list in json_resp['data']:
                video_title = data_list['title']
                video_played = data_list['play_effective_count']
                video_id = data_list['source_url'].replace('http://www.toutiao.com/item/','').replace('/','')
                if video_played.find('万')>-1:
                    video_played = float(video_played.replace('万',''))*10000               
                video_created = data_list['datetime']
                video_comments = data_list['comments_count']
                video_readed = data_list['go_detail_count'].replace(',','')
                if video_readed.find('万')>-1:
                    video_readed = float(video_readed.replace('万',''))*10000
                video_url = data_list['source_url'] 
                item = {'star_name': response.meta['star_name'],
                        'video_title': video_title,
                        'video_id': video_id,
                        'video_played': video_played,
                        'video_readed': video_readed,
                        'video_created': video_created,
                        'video_comments': video_comments,
                        'video_url': video_url,
                        'getdate': self._dt}
                yield item

        else:
            if int(response.meta['count']) > 10:
                print "*******toutiao-videoovercount:%s"%response.meta['count']
                pass
            else:
                count = str(int(response.meta['count']) + 1)
                print "url:%s count *****:%s"%(response.meta['url'], count)
                response.meta['count'] = count
                data = response.meta
                yield scrapy.FormRequest(response.meta['url'],
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )
    
    
    
    
    