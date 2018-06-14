# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import web
import time
from jd_real_time.items import JdRealTimeFlowSource

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}


class RealTimeFlowsourceSpider(scrapy.Spider):
    name = "real_time_flowsource"
    allowed_domains = ["sz.jd.com"]
    start_urls = ['http://sz.jd.com/']

    def start_requests(self):
        self.brand_list = []
        sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
          (shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
          group by shop_name;'''
        for i in db.query(sql):
            cookies = str(i.get('cookies'))
            name = i.get('shop_name')
            cookies_tuple = name, cookies
            self.brand_list.append(cookies_tuple)
        for j, i in enumerate(self.brand_list):
            cookies = json.loads(i[1])
            shom_name = i[0]
            parameter = {'PC': 20, 'APP': 2, '微信': 3, '手Q': 4, 'M端': 1}
            for i in parameter:
                url = 'https://sz.jd.com/realTime/flowSource.ajax?indChannel={tt}'
                s = parameter.get(i)
                url = url.format(tt=s)
                yield scrapy.Request(url, headers=headers, cookies=cookies,
                                     meta={'cookiejar': j,'indChannel':i ,
                                           'Account': shom_name, 'tt': s},
                                     dont_filter=True)


    def parse(self, response):
        temp=json.loads(response.body.decode())
        datas=temp['content']['data']
        for data in datas:
            item = JdRealTimeFlowSource()
            item['source']=data[0]
            item['indChannel']=response.meta['indChannel']
            item['visit_num']=data[1]#访客数
            item['visit_rate']=data[2]#访客数占比
            item['source_id']=data[3]
            item['has_sub']=data[4]
            item['fathersourceid']=''
            item['fathersourcename'] = ''
            item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['shop_name']=response.meta['Account']
            item['date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            yield item
            if item['has_sub']==True:
                url='https://sz.jd.com/realTime/subFlowSource.ajax?indChannel=%s&' \
                    'source1Id=%s&sourceLevel=%s' %(response.meta['tt'],data[3],1)
                yield scrapy.Request(url, headers=headers,
                                     meta={'cookiejar': response.meta['cookiejar'],'indChannel':response.meta['indChannel'] ,
                                           'Account':response.meta['Account'] ,
                                            'fathersourcename':data[0],'fathersourceid':data[3],
                                           'sourceLevel':1,'tt':response.meta['tt'],
                                           'grand':{1:data[3]}},
                                     dont_filter=True,callback=self.get_subFlowSource)


    def get_subFlowSource(self,response):
        temp=json.loads(response.body.decode())
        datas=temp['content']['data']
        for data in datas:
            item = JdRealTimeFlowSource()
            item['source']=data[0]
            item['indChannel']=response.meta['indChannel']
            item['visit_num']=data[1]#访客数
            item['visit_rate']=data[2]#访客数占比
            item['source_id']=data[3]
            item['has_sub']=data[4]
            item['fathersourceid']=response.meta['fathersourceid']
            item['fathersourcename'] = response.meta['fathersourcename']
            item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['shop_name']=response.meta['Account']
            item['date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            yield item
            if item['has_sub']==True:
                sourceLevel=response.meta['sourceLevel']+1
                url='https://sz.jd.com/realTime/subFlowSource.ajax?indChannel=%s' \
                    '&sourceLevel=%s' %(response.meta['tt'],sourceLevel)
                grand=response.meta['grand']
                grand[sourceLevel]=data[3]
                link_attr=''
                for i in range(1,sourceLevel+1):
                    link_attr+='&source%sId=%s'%(i,response.meta['grand'][i])
                url+=link_attr
                yield scrapy.Request(url, headers=headers,
                                     meta={'cookiejar': response.meta['cookiejar'],'indChannel':response.meta['indChannel'] ,
                                           'Account':response.meta['Account'] ,
                                            'fathersourcename':data[0],'fathersourceid':data[3],
                                           'sourceLevel':sourceLevel,'tt':response.meta['tt'],
                                           'grand':grand},
                                     dont_filter=True,callback=self.get_subFlowSource)


    
    
    