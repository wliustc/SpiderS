# -*- coding: utf-8 -*-
import scrapy
import json
import time
import MySQLdb
from weixinsmall.items import WeixinsmallTakerItem
class XiangwushuoTakerSpider(scrapy.Spider):
    name = "xiangwushuo_taker"
    allowed_domains = ["39916353.share1diantong.com"]
    start_urls = ['http://39916353.share1diantong.com/']

    def start_requests(self):
        conn = MySQLdb.connect(host='10.15.1.24', user='writer',port=3306, passwd='hh$writer', db='hillinsight', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()

        cur.execute('select distinct topic_id from t_spider_xiangwushuo_list where `dt`=date(now());')
        temps=cur.fetchall()
        cur.close()
        conn.close()
        headers={
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wxa344448166586158/144/page-frame.html',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044022 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN',
            'Host': '39916353.share1diantong.com',
            'Connection': 'Keep-Alive',
        }
        for temp in temps:
            topic_id=temp['topic_id']
            user_id='8540761'
            yield scrapy.Request('https://39916353.share1diantong.com/topic/get_taker_lst',method='POST',headers=headers,
                                 body='topic_id=%s&uuid=93ee2efc2097038470af46c982303304&session_login_user_id=%s&release_version=20180223&AppID=wxa344448166586158'
                                      %(topic_id,user_id),meta={'item':{'topic_id':topic_id,'user_id':user_id}})
    def parse(self, response):
        temp=json.loads(response.body.decode())
        datas=temp['data']
        if not temp['success']:
            return
        try:
            for data in datas.keys():
                item=WeixinsmallTakerItem()
                item['topic_id']=response.meta['item']['topic_id']
                item['total'] = temp['total']
                item['user_id'] = datas[data]['user_id']
                item['userName']=datas[data]['userName']
                item['order_ctime'] = datas[data]['order_ctime']
                item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item['date']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
        except Exception as e:
            self.logger.error('%s,,,,,%s'%(response.meta['item']['topic_id'],datas))
    
    
    
    
    