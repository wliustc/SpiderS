# -*- coding: utf-8 -*-
import scrapy
import web
import json
import time
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class XhsCommentariesSpider(scrapy.Spider):
    name = 'xhs_commentaries'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(XhsCommentariesSpider,self).__init__(*args,**kwargs)
        self.commentaries = '''https://www.xiaohongshu.com/api/discovery/get_comment?discovery_id={}'''
    def start_requests(self):
        sql = '''select DISTINCT id from t_spider_xhs'''
        for i in db.query(sql):
            uid = i.get('id')
            url = self.commentaries.format(uid)
            yield scrapy.Request(url,meta={'uid':uid,'url':url,'t':0},dont_filter=True)

    def parse(self, response):
        uid = response.meta['uid']
        try:
            html = json.loads(response.body)
            # print html
            for i in html['comments']:
                item = {}
                item['content'] = i.get('content')
                item['content_time'] = i.get('time')
                item['nickname'] = i.get('user').get('nickname')
                item['uid'] = uid
                item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
        except:
            if response.meta.get('t') !=4:
                url = response.meta['url']
                t = response.meta['t']+1
                yield scrapy.Request(url,meta={'uid':uid,'url':url,'t':t},dont_filter=True,callback=self.parse)


    