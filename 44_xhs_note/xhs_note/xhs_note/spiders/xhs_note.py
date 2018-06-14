# -*- coding: utf-8 -*-
import scrapy
import json
import time
import urllib
import hashlib
import sys
from handle import get_sign,get_time
reload(sys)
sys.setdefaultencoding('utf-8')

_list_param = {
    'deviceId':'C88FC555-57E9-474A-AC18-661258D44F85',
    'lang':'zh',
    'num':'20',
    'sort':'time',
    'oid':'homefeed.skincare',
    'page':'1',
    'platform':'iOS',
    'sid':'session.1146131555707014795',
    'size':'l',
    't':'1468571134',
    'value':'simple',
}

_note_param = {
    'deviceId':'C88FC555-57E9-474A-AC18-661258D44F85',
    'lang':'zh',
    'oid':'5787a880d5945f0c7edb3313',
    'platform':'iOS',
    'sid':'session.1146131555707014795',
    'size':'l',
    't':'1468571353',
}

class ListSpider(scrapy.Spider):
    name = "xhs"
    allowed_domains = ["xiaohongshu.com"]
    def __init__(self,task_date, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.list_url = 'http://www.xiaohongshu.com/api/sns/v3/homefeed'
        self.note_url = 'http://www.xiaohongshu.com/api/sns/v2/note/{}'
        self.cate = [ 'homefeed.skincare','homefeed.fashion','homefeed.makeup','homefeed.life','homefeed.travel','homefeed.men']
        #self.cate = [ 'homefeed.skincare','homefeed.makeup' ]
        self.task_date = task_date
        self.start_urls = []
        

    def start_requests(self):
        for i in self.cate:
            tmp = dict(_list_param)
            tmp['t'] = get_time()
            tmp['oid'] = i
            tmp['sign'] = get_sign(tmp)
            url = self._get_urls_cate(tmp)
            yield scrapy.Request(url,meta={'oid':i,'page':tmp['page']},callback=self.parse)

    def parse(self, response):
        oid = response.meta['oid']
        page = response.meta['page']
        if response.body:
            content = {}
            try:
            	content = json.loads(response.body)
            except:
                tmp['t'] = get_time()
                tmp['oid'] = oid
                tmp['page'] = page
                tmp['sign'] = get_sign(tmp)
                yield scrapy.Request(self._get_urls_cate(tmp),meta={'oid':oid,'page':page},callback=self.parse,dont_filter=True)
            if 'data' in content:
                if content['data']:
                    for d in content['data']:
                        item = {}
                        item['task_date'] = self.task_date
                        item['list'] = json.dumps(d)
                        item['oid'] = oid
                        tmp_param = dict(_note_param)
                        tmp_param['t'] = get_time()
                        tmp_param['oid'] = d['id']
                        tmp_param['sign'] = get_sign(tmp_param)
                        yield scrapy.Request(self._get_urls_note(d['id'],tmp_param),meta={'item':item},callback=self.parse_note,dont_filter=True)
                    tmp = dict(_list_param)
                    page = str(int(page) + 1)
                    tmp['t'] = get_time()
                    tmp['oid'] = oid
                    tmp['page'] = page
                    tmp['sign'] = get_sign(tmp)
                    yield scrapy.Request(self._get_urls_cate(tmp),meta={'oid':oid,'page':page},callback=self.parse,dont_filter=True)
            else:
                tmp['t'] = get_time()
                tmp['oid'] = oid
                tmp['page'] = page
                tmp['sign'] = get_sign(tmp)
                yield scrapy.Request(self._get_urls_cate(tmp),meta={'oid':oid,'page':page},callback=self.parse,dont_filter=True)

    def parse_note(self, response):
        item = response.meta['item']
        content = {}
        try:
            content = json.loads(response.body)
        except:
            pass
        if 'data' in content:
            item['note'] = json.dumps(content['data'])
            body = {
                'content':item
            }
            yield body
        else:
            yield {}
        #拼接url
    def _get_urls_cate(self,tmpData):
        return self.list_url+"?"+urllib.urlencode(tmpData)

    def _get_urls_note(self,oid,tmpData):
        return self.note_url.format(oid)+"?"+urllib.urlencode(tmpData)

    
    
    
    
    
    
    
    
    
    
    