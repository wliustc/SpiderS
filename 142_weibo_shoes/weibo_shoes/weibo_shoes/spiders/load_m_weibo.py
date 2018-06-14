# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
import math
import json
import time
import datetime
import urllib
from bs4 import BeautifulSoup
from weibo_shoes.items import LoadContentItem
import traceback
_headers = {
    "Host": "m.weibo.cn",
    "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
}


def get_url_list():
    res=[
        {'weibo_uid':'1648782501','name':'赵小姐失眠中','pinpai':'73 Hours'},
        {'weibo_uid':'5497155039','name':'高跟73小时73Hours','pinpai':'73 Hours'},
        {'weibo_uid': '1980434331','name':'AS官方微博','pinpai':'ACCENTO SQUISITO'},
        {'weibo_uid':'2162757372','name':'AEROSOLES','pinpai':'Aerosoles/爱柔仕'},
        {'weibo_uid': '2108812727','name':'ASH--艾熙','pinpai':'ASH'},
        {'weibo_uid': '2720021240','name':'Birkenstock中国','pinpai':'Birkenstock'},
        {'weibo_uid':'1893308930','name':'千百度官方旗舰店','pinpai':'C.BANNER/千百度'},
        {'weibo_uid': '2490567624','name':'Cat卡特官方微博','pinpai':'CAT'},
        {'weibo_uid':'1765564022','name':'CharlesKeith','pinpai':'CHARLES&KEITH'},
        {'weibo_uid': '2698482970','name':'Clarks','pinpai':'clarks'},
        {'weibo_uid':'1808540404','name':'CNE官方微博','pinpai':'CNE'},
        {'weibo_uid': '1975886475','name':'达芙妮','pinpai':'Daphne/达芙妮'},
        {'weibo_uid': '1855622015','name':'ECCO_爱步','pinpai':'Ecco/爱步'},
        {'weibo_uid': '2274543162','name':'Fed官方微博','pinpai':'fed/艾芙伊迪'},
        {'weibo_uid': '3197885312','name':'FONDBERYL菲伯丽尔','pinpai':'Fondberyl/菲伯丽尔'},
        {'weibo_uid': '1960514070','name':'哈森HARSON','pinpai':'Harson/哈森'},
        {'weibo_uid': '2280054587','name':'Innet茵奈儿官方微博','pinpai':'innet/茵奈儿'},
        {'weibo_uid': '2636824004','name':'JKJY男鞋','pinpai':'JKJY BY STELLA'},
        {'weibo_uid': '2245646292','name':'KISSCAT官方微博','pinpai':'KISS CAT/接吻猫'},
        {'weibo_uid': '3162449840','name':'kisscat接吻猫旗舰店','pinpai':'KISS CAT/接吻猫'},
        {'weibo_uid': '1996644417','name':'lesaunda莱尔斯丹天猫旗舰店','pinpai':'le saunda/莱尔斯丹'},
        {'weibo_uid': '1940627045','name':'Millies妙丽','pinpai':'Millie‘s/妙丽'},
        {'weibo_uid': '6331230447','name':'MOOFFY官微','pinpai':'MOOFFY'},
        {'weibo_uid': '1968143730','name':'NINEWEST玖熙中国','pinpai':'Nine West/玖熙'},
        {'weibo_uid': '5148488485','name':'圆漾ONDUL','pinpai':'ONDUL/圆漾'},
        {'weibo_uid': '2389536812','name':'MAISON_DE_REEFUR','pinpai':'Reef'},
        {'weibo_uid': '2176831617','name':'索菲娅女鞋','pinpai':'Safiya/索菲娅'},
        {'weibo_uid': '1938447924','name':'stellaluna女鞋','pinpai':'STELLA LUNA'},
        {'weibo_uid': '2473883720','name':'STONEFLY中国','pinpai':'STONEFLY/斯通富来'},
        {'weibo_uid': '2096588057','name':'Stuart_Weitzman','pinpai':'Stuart Weitzman'},
        {'weibo_uid': '1833037312','name':'Teenmix天美意商城','pinpai':'Teenmix/天美意'},
        {'weibo_uid': '2792667432','name':'tigrisso蹀愫','pinpai':'tigrisso'},
        {'weibo_uid': '3754151754','name':'tigrisso旗舰店','pinpai':'tigrisso'},
        {'weibo_uid': '1884228830','name':'TOP-GLORIA','pinpai':'Top Gloria'},
        {'weibo_uid': '2478152534','name':'TOPGLORIA官方微博','pinpai':'Top Gloria'},
        {'weibo_uid': '2477668744','name':'UGG官方微博','pinpai':'UGG'},
        {'weibo_uid': '5497971685','name':'VMe舞魅官方微博','pinpai':'VME/舞魅'},
        {'weibo_uid': '2044863135','name':'WHATFOR','pinpai':'WHAT FOR'},
        {'weibo_uid': '2576854334','name':'ZSAZSAZSU官方微博','pinpai':'zsazsazsu'},
        {'weibo_uid': '2004803620','name':'STACCATO_思加图','pinpai':'思加图/STACCATO'},
        {'weibo_uid': '1870080561','name':'Joy-Peace真美诗','pinpai':'真美诗/Joy-Peace'},
         ]
    return res

class LoadMWeiboSpider(scrapy.Spider):
    name = "load_m_weibo"
    allowed_domains = ["m.weibo.cn"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self.dt = datetime.date.today().strftime("%Y-%m-%d")

    def start_requests(self):
        for row in self.url_info:
            url = "https://m.weibo.cn/container/getIndex?containerid=230413" + row[
                "weibo_uid"] + "_-_WEIBO_SECOND_PROFILE_MORE_WEIBO"
            refer = 'https://m.weibo.cn/p/index?containerid=230413' + row[
                'weibo_uid'] + '_-_WEIBO_SECOND_PROFILE_MORE_WEIBO&title='
            tmp_headers = _headers
            tmp_headers['Referer'] = refer
            yield scrapy.FormRequest(url,
                                     headers=_headers,
                                     callback=self.parse_item,
                                     meta={'star_name': row['name'],
                                           'weibo_uid': row['weibo_uid'],
                                           'pinpai':row['pinpai'],
                                           'refer': refer,
                                           'url': url, 'count': '0'},
                                     dont_filter=True,
                                     )

    def check_need_retry(self, response):
        if response.status==302:
            return True
        if BeautifulSoup(response.body, "lxml").find(text=re.compile(u'请输入验证码')) != None:
            return True
        try:
            json_resp = json.loads(response.body)
            print(json_resp)
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
                    payload = {
                        'containerid': '230413' + response.meta['weibo_uid'] + '_-_WEIBO_SECOND_PROFILE_MORE_WEIBO',
                        'page': page_i}
                    url_new = 'http://m.weibo.cn/container/getIndex?'
                    url_new = url_new + urllib.urlencode(payload)
                    data = {'url': url_new, 'count': '0',
                            'star_name': response.meta['star_name'],
                            'pinpai':response.meta['pinpai'],
                            'weibo_uid': response.meta['weibo_uid']
                            }
                    yield scrapy.FormRequest(url_new,
                                             callback=self.parse_item,
                                             meta=data,
                                             dont_filter=True,
                                             )
            json_resp = json.loads(response.body)
            for sta_list in json_resp['data']['cards']:
                if 'mblog' in sta_list:
                    weibo_id = sta_list['mblog']['id']
                    created_at = sta_list['mblog']['created_at']
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
                                      'pinpai':response.meta['pinpai'],
                                      'weibo_uid':response.meta['weibo_uid'],
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
                                'getdate': self.dt,'src':'shoudong'})
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
                if 'refer' in data:
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
    
    
    
    
    
    
    
    
    
    
    
    