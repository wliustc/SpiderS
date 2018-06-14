# -*- coding: utf-8 -*-
import scrapy
import json
import time
import urllib
import hashlib
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def get_sign(params_dict):
    keys = params_dict.keys()
    keys.sort()
    mess = ''
    for k in keys:
        mess += k + '=' + params_dict[k]
    mess = urllib.quote_plus(mess)

    a = bytearray(mess, encoding='utf-8')
    b = bytearray(params_dict['deviceId'], encoding='utf-8')
    c = ''
    j = 0
    for byt in a:
        c += str(byt ^ b[j])
        j = (j + 1) % len(b)
    return hashlib.md5((hashlib.md5(c).hexdigest() + params_dict['deviceId'])).hexdigest()


def get_time():
    return str(time.time())[:10]
_list_param = {
    'deviceId': 'C88FC555-57E9-474A-AC18-661258D44F85',
    'lang': 'zh',
    'num': '20',
    'sort': 'time',
    'oid': 'homefeed.skincare',
    'page': '1',
    'platform': 'iOS',
    'sid': 'session.1146131555707014795',
    'size': 'l',
    't': '1468571134',
    'value': 'simple',
}

_note_param = {
    'deviceId': 'C88FC555-57E9-474A-AC18-661258D44F85',
    'lang': 'zh',
    'oid': '5304e51ab4c4d63d59a30bac',
    'platform': 'iOS',
    'sid': 'session.1146131555707014795',
    'size': 'l',
    't': '1468571353',
}
# _note_param['t'] = get_time()
# _note_param['sign'] = get_sign(_note_param)
# url = 'http://www.xiaohongshu.com/api/sns/v2/note/{}'.format('5304e51ab4c4d63d59a30bac')+'?'+ urllib.urlencode(_note_param)
# print url


class ListSpider(scrapy.Spider):
    name = "xhs_note_spider"
    allowed_domains = ["xiaohongshu.com"]

    def __init__(self, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.list_url = 'http://www.xiaohongshu.com/api/sns/v3/homefeed'
        self.note_url = 'http://www.xiaohongshu.com/api/sns/v2/note/{}'
        self.cate = ['homefeed.skincare_v2', 'homefeed.fashion_v2', 'homefeed.makeup', 'homefeed.life', 'homefeed.travel_v2',
                     'homefeed.men', 'homefeed.video', 'homefeed.cosmetics_v2', 'homefeed.celebrities_v2',
                     'homefeed.fitness_v2', 'homefeed.home_v2', 'homefeed.maternity_v2', 'homefeed.digital_v2',
                     'homefeed.mens_fashion_v2', 'homefeed.music_v2']
        # self.cate = [ 'homefeed.skincare','homefeed.makeup' ]
        # self.task_date = task_date
        self.start_urls = []

    def start_requests(self):
        for i in self.cate:
            tmp = dict(_list_param)
            tmp['t'] = get_time()
            tmp['oid'] = i
            tmp['sign'] = get_sign(tmp)
            url = self._get_urls_cate(tmp)
            yield scrapy.Request(url, meta={'oid': i, 'page': tmp['page']}, callback=self.parse)

    def parse(self, response):
        oid = response.meta['oid']
        page = response.meta['page']
        if response.body:
            content = {}
            try:
                content = json.loads(response.body)
            except:
                tmp = dict(_list_param)
                tmp['t'] = get_time()
                tmp['oid'] = oid
                tmp['page'] = page
                tmp['sign'] = get_sign(tmp)
                yield scrapy.Request(self._get_urls_cate(tmp), meta={'oid': oid, 'page': page}, callback=self.parse,
                                     dont_filter=True)
            if 'data' in content:
                if content['data']:
                    for d in content['data']:
                        item = {}
                        item['task_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                        item['list'] = json.dumps(d)
                        item['oid'] = oid
                        tmp_param = dict(_note_param)
                        tmp_param['t'] = get_time()
                        tmp_param['oid'] = d['id']
                        tmp_param['sign'] = get_sign(tmp_param)
                        yield scrapy.Request(self._get_urls_note(d['id'], tmp_param), meta={'item': item},
                                             callback=self.parse_note, dont_filter=True)
                    tmp = dict(_list_param)
                    page = str(int(page) + 1)
                    tmp['t'] = get_time()
                    tmp['oid'] = oid
                    tmp['page'] = page
                    tmp['sign'] = get_sign(tmp)
                    yield scrapy.Request(self._get_urls_cate(tmp), meta={'oid': oid, 'page': page}, callback=self.parse,
                                         dont_filter=True)
            else:
                tmp = dict(_list_param)
                tmp['t'] = get_time()
                tmp['oid'] = oid
                tmp['page'] = page
                tmp['sign'] = get_sign(tmp)
                yield scrapy.Request(self._get_urls_cate(tmp), meta={'oid': oid, 'page': page}, callback=self.parse,
                                     dont_filter=True)

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
                'content': item
            }
            yield body
            # raw_input("enter")
        else:
            yield {}
            # 拼接url

    def _get_urls_cate(self, tmpData):
        return self.list_url + "?" + urllib.urlencode(tmpData)

    def _get_urls_note(self, oid, tmpData):
        return self.note_url.format(oid) + "?" + urllib.urlencode(tmpData)












