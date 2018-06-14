# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pyhs2
from xiaohongshu.items import XhsFansItem


class Xhs_Fans_Spider(scrapy.Spider):

    name = 'xhs_fans_spider'
    #custom_settings = {
     #   'DOWNLOADER_MIDDLEWARES': {'xiaohongshu.middlewares_mine.ProxyMiddleware': 110}
    #}

    def start_requests(self):
        with pyhs2.connect(host='10.15.1.16', port=10000, authMechanism="PLAIN", user='zyliu', password='zyliu',
                           database='ods') as conn:
            with conn.cursor() as cur:
                sql = "select task_date from ods.xhs_all_note where list not LIKE concat('%','穿搭','%') and list not LIKE concat('%','包','%') and oid not in ('homefeed.cosmetics_v2', 'homefeed.fashion_v2') group by task_date limit 85000"
                cur.execute(sql)
                for info in cur.fetch():
                    user_id = info[0]
                    url = 'http://www.xiaohongshu.com/user/profile/{}'.format(user_id)
                    yield scrapy.Request(url, callback=self.parse_detail, meta={'user_id': user_id})
                # for word in ['穿搭', '包']:
                #     sql = "select task_date from ods.xhs_all_note where list LIKE concat('%','{}','%') group by task_date".format(word)
                #     cur.execute(sql)
                #     for info in cur.fetch():
                #         user_id = info[0]
                #         url = 'http://www.xiaohongshu.com/user/profile/{}'.format(user_id)
                #         yield scrapy.Request(url, callback=self.parse_detail, meta={'user_id': user_id, 'cate': word})
                # for cate in ['homefeed.fashion_v2', 'homefeed.makeup']:
                #     sql = "select task_date from ods.xhs_all_note where oid='{}' group by task_date".format(cate)
                #     cur.execute(sql)
                #     for info in cur.fetch():
                #         user_id = info[0]
                #         url = 'http://www.xiaohongshu.com/user/profile/{}'.format(user_id)
                #         yield scrapy.Request(url, callback=self.parse_detail, meta={'user_id': user_id, 'cate': cate})
        # url = 'http://www.xiaohongshu.com/user/profile/5a6ca8554eacab4b4e7834b7'
        # user_id = ''
        # cate = ''
        # yield scrapy.Request(url, callback=self.parse_detail, meta={'user_id': user_id, 'cate': cate})

    def parse_detail(self, response):
        content = response.body
        items = XhsFansItem()
        user_id = response.meta['user_id']
        # cate = response.meta['cate']
        pattern1 = re.search('class="fans".*?>(.*?)<', content)
        fans_num = pattern1.group(1)
        if '万' in fans_num:
            fans_num = re.sub('万', '', fans_num)
            fans_num = int(float(fans_num) * 10000)
        pattern2 = re.search('class="collect".*?>(.*?)<', content)
        collect = pattern2.group(1)
        if '万' in collect:
            collect = re.sub('万', '', collect)
            collect = int(float(collect) * 10000)
        pattern3 = re.search('class="name-detail".*?>(.*?)<', content)
        name = pattern3.group(1)
        pattern4 = re.search('笔记<span data.*?</i>(.*?)<', content)
        note_num = pattern4.group(1)
        pattern5 = re.search('class="brief".*?>(.*?)<', content)
        brief = ''
        if pattern5:
            brief = pattern5.group(1)
        items['user_id'] = user_id
        items['fans_num'] = fans_num
        items['collect'] = collect
        items['name'] = name
        items['note_num'] = note_num
        items['brief'] = brief

        yield items
    
    
    
    
    
    