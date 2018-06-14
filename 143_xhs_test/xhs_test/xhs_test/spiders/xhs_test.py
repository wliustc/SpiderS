# -*- coding: utf-8 -*-
import scrapy
import json
import re
import urllib
import time
import hashlib

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.xiaohongshu.com',
'Referer':'http://www.xiaohongshu.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
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


def get_sign(params_dict):
    keys = params_dict.keys()
    keys.sort()
    mess = ''
    for k in keys:
        mess += k+'='+params_dict[k]
    mess = urllib.quote_plus(mess)

    a = bytearray(mess, encoding='utf-8')
    b = bytearray(params_dict['deviceId'], encoding='utf-8')
    c = ''
    j = 0
    for byt in a:
        c += str(byt^b[j])
        j = (j+1)%len(b)
    return hashlib.md5((hashlib.md5(c).hexdigest() + params_dict['deviceId'])).hexdigest()

class XhsTestSpider(scrapy.Spider):
    name = 'xhs_test'
    allowed_domains = ['xhs.org']
    start_urls = ['http://xhs.org/']
    def __init__(self,*args,**kwargs):
        super(XhsTestSpider,self).__init__(*args,**kwargs)
        self.comment = '''https://www.xiaohongshu.com/api/discovery/get_comment?discovery_id={id}'''
        self.keyword = '''http://www.xiaohongshu.com/web_api/sns/v2/search/note?keyword={keyword}&page={page}'''
        self.home = '''http://www.xiaohongshu.com/api/sns/v2/note/{}'''
    def start_requests(self):
        # id_lsit = '5a3275ea4b88450f7b9752ad'
        # url = self.home.format(id_lsit)
        # yield scrapy.Request(url,dont_filter=True,callback=self.homes)
        keyword = ['奈绮儿Naiyee','玛速MASOOMAKE','TB拓贝','OZWEAR UGG','KEDDO','小CK','PAZZION','OZLANA UGG','Marie Claire','Maud Frizon','Charles&Keith','Belle百丽', 'TATA他她', 'Staccato思加图','烫 鞋','st&sat星期六','lesaunda莱尔斯丹','KISSKAT接吻猫','BASTO百思图','Harson哈森','73小时73hours',
        '千百度C.BANNER', 'STELLALUNA','Joy&peace真美诗','FED','D:fuse迪芙斯','玖熙NineWest']
        for i in keyword:
            s = urllib.quote(i)
            url = self.keyword.format(keyword=s,page=1)
            yield scrapy.Request(url,meta={'url':url,'keyword':i})
    def parse(self, response):
        html = json.loads(response.body)
        if len(html['data']):
            keyword = response.meta['keyword']
            for i in html['data']:
                item ={}
                id_ = i.get('id')
                title = i.get('title')
                nickname = i.get('user').get('nickname')
                likes = i.get('likes')
                item['id'] = id_
                item['title'] = title
                item['nickname'] = nickname
                item['keyword'] = keyword
                item['likes'] = likes
                if u'鞋' in title:
                    item['marking'] =1
                elif u'靴' in title:
                    item['marking'] = 1
                else:
                    item['marking'] =0
                url = self.home.format(item['id'])
                tmp = dict(_note_param)
                tmp['t'] = str(int(time.time()))
                tmp['oid'] = item['id']
                tmp['sign'] = get_sign(tmp)
                yield scrapy.Request(self._get_urls_note(item['id'],tmp),headers=headers,meta={'item':item,'url':url},callback=self.homes,dont_filter=True)
            url = response.meta['url'].split('page=')
            page = int(url[1])+1
            urls = url[0]+'page='+ str(page)
            yield scrapy.Request(urls,meta={'url':urls,'keyword':keyword},dont_filter=True,callback=self.parse)
    def homes(self,response):
        item = response.meta['item']
        html = json.loads(response.body)
        comments = html.get('data').get('comments')
        fav_count = html.get('data').get('fav_count')
        posted_time = html.get('data').get('time')
        item['posted_time'] = posted_time
        item['commentaries'] = comments
        item['collect'] = fav_count
        item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        yield item
    def _get_urls_note(self,oid,tmpData):
        return self.home.format(oid)+"?"+urllib.urlencode(tmpData)

