# -*- coding: utf-8 -*-
import scrapy
import MySQLdb   
import json
import time
from weibo_shoes.items import LoadCommentItem
import datetime
import re
class CommentSpider(scrapy.Spider):
    name = "comment"
    allowed_domains = ["m.weibo.com"]
    start_urls = ['http://m.weibo.com/']
    def __init__(self, *args, **kwargs):
        self.dt = datetime.date.today().strftime("%Y-%m-%d")


    def start_requests(self):
        conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute('select `weibo_uid`,`pinpai`,`weibo_id` from `hillinsight`.`tt_spiderman_weibo_chose_pin` '
                    'where `getdate`=DATE(now()) and `src`="search";')
        temps=cur.fetchall()
        cur.close()
        conn.close()
        for tmp in temps:
            url='https://m.weibo.cn/api/comments/show?id=%s&page=1' %tmp['weibo_id']
            header={
                'Accept':'application/json, text/plain, */*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Host':'m.weibo.cn',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
            }
            yield scrapy.Request(url,headers=header,callback=self.parse_item,
                                     meta={'item':{'weibo_uid':tmp['weibo_uid'],
                                         'pinpai':tmp['pinpai'],
                                         'weibo_id':tmp['weibo_id']}},
                                     dont_filter=True)

    def parse_item(self, response):
        temp=json.loads(response.body.decode())
        if temp['msg']=='暂无数据':
            return 
        if 'total_number' not in response.meta:
            total_number=temp['data']['total_number']
        else:
            total_number=response.meta['total_number']
        if 'num_now' not in response.meta:
            num_now=0
        else:
            num_now = response.meta['num_now']
        if total_number==0:
            return

        for tmp in temp['data']['data']:
            item=LoadCommentItem()
            created_at=tmp['created_at']
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
            item['comment_id']=tmp['id']
            item['created_at'] = created_at
            item['source'] = tmp['source']
            item['comment_user_id'] = tmp['user']['id']
            item['comment_user_name'] = tmp['user']['screen_name']
            item['text'] = MySQLdb.escape_string(tmp['text'])
            item['like_counts'] = tmp['like_counts']
            item['weibo_uid']= response.meta['item']['weibo_uid']
            item['pinpai']=response.meta['item']['pinpai']
            item['weibo_id']=response.meta['item']['weibo_id']
            item['dt']=time.strftime('%Y-%m-%d',time.localtime())
            yield item
        num_now += 10
        if int(num_now)<int(total_number):
            page_num=num_now//10+1
            url='https://m.weibo.cn/api/comments/show?id=%s&page=%s' %(response.meta['item']['weibo_id'],page_num)
            header={
                'Accept':'application/json, text/plain, */*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Host':'m.weibo.cn',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
            }
            yield scrapy.Request(url,headers=header,callback=self.parse_item,
                                     meta={'item':{'weibo_uid':response.meta['item']['weibo_uid'],
                                         'pinpai':response.meta['item']['pinpai'],
                                         'weibo_id':response.meta['item']['weibo_id'],
                                        },'num_now':num_now,'total_number':total_number},
                                     dont_filter=True)

    
    
    
    
    
    
    
    