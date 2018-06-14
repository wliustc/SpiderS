# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
import MySQLdb
import datetime
from weibo_shoes.items import LoadMSearchItem
search_list=[#'Aerosoles/爱柔仕','73 Hours','ACCENTO SQUISITO','ASH','Bevivo','Birkenstock','C.BANNER/千百度','CAT','CHARLES&KEITH','clarks','CNE',
#'Daphne/达芙妮','Ecco/爱步','fed/艾芙伊迪','Fondberyl/菲伯丽尔','Harson/哈森','innet/茵奈儿','JKJY BY STELLA','KISS CAT/接吻猫','le saunda/莱尔斯丹','Millie‘s/妙丽','MOOFFY','Nine West/玖熙','ONDUL/圆漾','Reef','Safiya/索菲娅','STELLA LUNA','STONEFLY/斯通富来',
#'Stuart Weitzman','Teenmix/天美意','tigrisso','Top Gloria','UGG','VME/舞魅','WHAT FOR','zsazsazsu','vivifleurs','S·E·N·S·E 1991','St&Sat/星期六',
#'RUBBER SOUL','Idee Europa/欧罗派	','Coup de Foudre','Dr．Martens','JIMMY BLACK','duckfeet','D：Fuse/迪芙斯','el natura lista','gingerlily',
#'IIXVIIX','Millie’s','QUEEN RABU','Rabu Rabu','ARt',
#'Blundstone'
    '思加图/STACCATO','真美诗/Joy-Peace'
]
class MSearchSpider(scrapy.Spider):
    name = "m_search"
    allowed_domains = ["m.weibo.com"]
    dt = time.strftime('%Y-%m-%d', time.localtime())

    def start_requests(self):
        url='https://passport.weibo.cn/sso/login'
        yield scrapy.FormRequest(url,
            formdata={
                'username':'504772813@qq.com',
                'password':'543324797a.5',
                'savestate':'1',
                'r':'http://m.weibo.cn/',
                'ec':'0',
                'pagerefer':'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F',
                'entry':'mweibo',
                'wentry':'',
                'loginfrom':'',
                'client_id':'',
                'code':'',
                'qq':'',
                'mainpageflag':'1',
                'hff':'',
                'hfp':'',
            },
            headers={
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                'Host':'passport.weibo.cn',
                'Origin':'https://passport.weibo.cn',
                'Pragma':'no-cache',
                'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        url = 'http://m.weibo.cn/'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'm.weibo.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://s.weibo.com/weibo/73%2520Hours&Refer=focus_lx_STopic_box',
        }
        yield scrapy.Request(url, headers=header, callback=self.start_search,
                             dont_filter=True)

    def start_search(self,response):
        for pinpai in search_list:
            for search_data in pinpai.split('/'):
                url='https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%s&luicode=10000011' \
                    '&lfid=106003type%%3D1&title=%s&containerid=100103type%%3D1%%26q%%3D%s'\
                    %(search_data,search_data,search_data)
                header = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Host': 'm.weibo.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                yield scrapy.Request(url, headers=header, callback=self.parse_item,
                                     meta={'item': {'pinpai':pinpai,'search_data':search_data}},
                                     dont_filter=True)


    def parse_item(self,response):
        temp=json.loads(response.body.decode())
        if temp['ok']==0:
            if temp['msg']=='这里还没有内容':
                return
        if 'total_number' not in response.meta:
            total_number=temp['data']['cardlistInfo']['total']
        else:
            total_number=response.meta['total_number']
        if 'num_now' not in response.meta:
            num_now=0
        else:
            num_now = response.meta['num_now']
        if total_number==0:
            return
        for tmp in temp['data']['cards']:
            if 'card_group' in tmp:
                for data in tmp['card_group']:
                    if 'mblog' not in data:
                        continue
                    item=LoadMSearchItem()
                    created_at=data['mblog']['created_at']
                    if len(created_at.split('-'))==3:
                        pass
                    elif len(created_at.split('-'))==2:
                        created_at=time.strftime('%Y', time.localtime())+'-'+created_at
                    elif re.search(u'分钟前',created_at):
                        created_at=self.dt
                    elif re.search(u'昨天',created_at):
                        created_at= (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    elif re.search(u'小时前',created_at):
                        created_at=re.sub('[^0-9]+','',created_at)
                        created_at = (datetime.date.today() - datetime.timedelta(hours=int(created_at))).strftime("%Y-%m-%d")
                    item.update({'star_name':data['mblog']['user']['screen_name'],
                                 'pinpai': response.meta['item']['pinpai'],
                                 'weibo_uid': data['mblog']['user']['id'],
                                 'weibo_id': data['mblog']['id'],
                                 'created_at': created_at ,
                                 'weibo_text': MySQLdb.escape_string(data['mblog']['text']),
                                 'followers_count': data['mblog']['user']['followers_count'],
                                 'retweeted_id': '',
                                 'retweeted_text': '',
                                 'follow_count': data['mblog']['user']['follow_count'],
                                 'statuses_count': data['mblog']['user']['statuses_count'],
                                 'urank': data['mblog']['user']['urank'],
                                 'reposts_count': data['mblog']['reposts_count'],
                                 'comments_count': data['mblog']['comments_count'],
                                 'attitudes_count': data['mblog']['attitudes_count'],
                                 'url': response.url,
                                 'getdate': self.dt,'src':'search'})
                    yield item
            else:
                pass
        num_now+=10
        print('**********************total=%s******************now=%s**************' %(total_number,num_now))
        if int(num_now)<int(total_number):
            page_num=num_now//10+1
            url = 'https://m.weibo.cn/api/container/getIndex?type=all&' \
                  'queryVal=%s&featurecode=20000320&luicode=10000011&lfid=100103type%%3D1&title=%s' \
                  '&containerid=100103type%%3D1%%26q%%3D%s&page=%s' % (response.meta['item']['search_data'],
                                                               response.meta['item']['search_data'],
                                                               response.meta['item']['search_data'],
                                                               page_num)
            header={
                'Accept':'application/json, text/plain, */*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Host':'m.weibo.cn',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
            }
            yield scrapy.Request(url,headers=header,callback=self.parse_item,
                                     meta={'item':{
                                         'pinpai':response.meta['item']['pinpai'],
                                         'search_data':response.meta['item']['search_data'],
                                        },'num_now':num_now,'total_number':total_number},
                                    dont_filter=True)


    
    
    
    
    
    
    
    