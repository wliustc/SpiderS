# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Selector
from ..items import *
import random
import web
import sys
reload(sys)
import time
import datetime
def time_s(dt):
    if dt:
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-dt)
        yes_time_nyr = yes_time.strftime('%Y-%m-%d %H:%M:%S')
        # 转换成时间数组
        timeArray = time.strptime(yes_time_nyr, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return timestamp


sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


cookies = {  'hng':'CN%7Czh-CN%7CCNY%7C156',
             'uc3':'nk2=odNmwEgvPCl3eA%3D%3D&id2=UUwY%2BY8hOjpw6g%3D%3D&vt3=F8dBzWfTEAYjnbTsJaA%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D',
             'lgc':'%5Cu9A6C%5Cu5C71tx%5Cu5C0F%5Cu5175',
             'tracknick':'%5Cu9A6C%5Cu5C71tx%5Cu5C0F%5Cu5175',
             '_uab_collina':'150518237910443769978717',
             'swfstore':'115509',
            'cookie2':'1ea7f05d6ea6d2a283aca030377dcb44',
             't':'ebf710f111c5c2c6675ec5702c4db451',
             '_tb_token_':'c9b6136789e4f',
             '_umdata':'C234BF9D3AFA6FE7E87B6114C523C90FE357CB0872A9BD520039741D37596FDA0A878194191C698CCD43AD3E795C914C8D0C8727F14F21FECCA4873D0FDC4C85',
             'cq':'ccp%3D1',
             'otherx':'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
             'isg':'AoeH6mOPkqnvcBYkYwq0jk7OFjv9mFAlHXDdUVl2JJY_yKeKYVzrvsXAHL5t',
             'cna':'UxKXEYbrhB0CAdNm1BKVQO7t',
             'pnm_cku822':''
}
ua = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.8',
    'cache-control':'max-age=0',
    }
class BailiSpider(scrapy.Spider):
    name = 'taobao_id'
    allowed_domains = ['baili.org']
    def __init__(self,dt=7,*args,**kwargs):
        super(BailiSpider,self).__init__(*args,**kwargs)
        self.dt =dt
        self.js = 'https://rate.tmall.com/list_detail_rate.htm?itemId={data_id}&spuId=868875336&sellerId=167873659&order=1&append=0&content=1&tagId=&posi=&picture=&_ksTS={time_s}&callback=jsonp{s}&currentPage={pag}'
    def start_requests(self):
        sql = ''' SELECT DISTINCT dataid FROM `t_xsd_tianmao_id_picture` '''
        for i in db.query(sql):
            data_id = i.get('dataid')
            sj = str(random.randint(100, 1999))
            task_time = str(int(time.time() * 1000)) + '_' + sj
            s = str(random.randint(100, 999))
            url = self.js.format(data_id=data_id,pag=1,time_s=task_time,s=s)
            if self.dt == 7:
                yield scrapy.Request(url,dont_filter=True,meta={'count1':1,'pass':0,'data_id':data_id,'url':url},headers=ua,cookies=cookies)
            elif self.dt == '0':
                yield scrapy.Request(url,dont_filter=True,meta={'count1':1,'pass':0,'data_id':data_id,'url':url},headers=ua,cookies=cookies,callback=self.parse_all)



    def parse(self, response):
        if 'checklogin' is response.url:
            url = response.meta.get('url')
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse)

        item = TaobaoBaidliItem()
        data_url = response.meta.get('url')
        dataid = response.meta.get('data_id')
        html = response.body
        if response.meta.get('count') != response.meta.get('count1'):
            try:
                data = json.loads(html.decode('gbk').encode('utf8')[12:-1])
                if int(data.get('rateDetail').get('paginator').get('lastPage')) >=1:
                    pag = int(data.get('rateDetail').get('paginator').get('lastPage'))+1
                    ScoreTime = data.get('rateDetail').get('rateList')[0].get('rateDate')
                    ScoreTime = time.mktime(time.strptime(ScoreTime, "%Y-%m-%d %H:%M:%S"))
                    if int(ScoreTime) > int(time_s(self.dt)):
                        for i in data.get('rateDetail').get('rateList'):

                            rateContent = i.get('rateContent')
                            rateDate = i.get('rateDate')
                            ScoreTime = time.mktime(time.strptime(rateDate, "%Y-%m-%d %H:%M:%S"))
                            if int(ScoreTime) > int(time_s(self.dt)):
                                name = i.get('displayUserNick')
                                item['commentaries'] = rateContent
                                item['score_time'] = rateDate
                                item['comments_name'] = name
                                item['code'] = dataid
                                item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                                # item['url'] = response.meta.get('url')
                                rateDate = rateDate.split(' ')[0].split('-')
                                rate = datetime.date(int(rateDate[0]), int(rateDate[1]), int(rateDate[2])).isocalendar()
                                item['years'] = rate[0]
                                item['months'] = rateDate[1]
                                item['weeks'] = rate[1]
                                yield item
                        pag1 = data_url.split('currentPage=')
                        url = pag1[0]+'currentPage='+str(int(pag1[1])+1)
                        response.meta['count'] = pag
                        response.meta['count1'] = response.meta.get('count1') + 1
                        response.meta['data_id'] = dataid
                        response.meta['url'] = url
                        yield scrapy.Request(url,meta=response.meta,callback=self.parse,dont_filter=True)
            except Exception as e:
                if response.meta.get('pass') == 10:
                    pass
                else:
                    response.meta['pass'] = int(response.meta.get('pass')) + 1
                    url = data_url
                    yield scrapy.Request(url,meta=response.meta,cookies=cookies,headers=ua,dont_filter=True,callback=self.parse)




    def parse_all(self, response):
        if 'checklogin' is response.url:
            url = response.meta.get('url')
            yield scrapy.Request(url,meta=response.meta,dont_filter=True,callback=self.parse_all)
        item = TaobaoBaidliItem()
        data_url = response.meta.get('url')
        dataid = response.meta.get('data_id')
        html = response.body
        if response.meta.get('count') != response.meta.get('count1'):
            try:
                data = json.loads(html.decode('gbk').encode('utf8')[12:-1])
                pag = int(data.get('rateDetail').get('paginator').get('lastPage')) + 1
                if int(data.get('rateDetail').get('paginator').get('lastPage')) >=1:

                    for i in data.get('rateDetail').get('rateList'):
                        rateContent = i.get('rateContent')
                        rateDate = i.get('rateDate')
                        name = i.get('displayUserNick')
                        item['commentaries'] = rateContent
                        item['score_time'] = rateDate
                        item['comments_name'] = name
                        item['code'] = dataid
                        item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                        rateDate = rateDate.split(' ')[0].split('-')
                        rate = datetime.date(int(rateDate[0]), int(rateDate[1]), int(rateDate[2])).isocalendar()
                        item['years'] = rate[0]
                        item['months'] = rateDate[1]
                        item['weeks'] = rate[1]
                        # item['url'] = response.meta.get('url')
                        yield item
                pag1 = data_url.split('currentPage=')
                url = pag1[0]+'currentPage='+str(int(pag1[1])+1)
                response.meta['count'] = pag
                response.meta['count1'] = response.meta.get('count1')+1
                response.meta['data_id'] = dataid
                response.meta['url'] = url

                yield scrapy.Request(url,meta=response.meta,callback=self.parse_all,dont_filter=True)
            except Exception as e:
                if response.meta.get('pass') == 10:
                    pass
                else:
                    response.meta['pass']=int(response.meta.get('pass'))+1
                    url = data_url
                    yield scrapy.Request(url,meta=response.meta,cookies=cookies,headers=ua,dont_filter=True,callback=self.parse_all)
    
    
    