# -*- coding: utf-8 -*-
import scrapy
import web
import json
import time
from jd_real_time.items import JdRealTimeTopItem

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}

class RealTimeTopSpider(scrapy.Spider):
    name = "real_time_top"
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

        for i in self.brand_list:
            cookies = json.loads(i[1])
            shop_name = i[0]
            dt=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            After_sale_url='https://sz.jd.com/realTime/getRealTopList.ajax?categoryType=0&channel=99&second=999999&third=999999'
            yield scrapy.Request(After_sale_url, headers=headers, cookies=cookies,
                                 meta={'Account': shop_name}, dont_filter=True)

    def parse(self, response):
        data=json.loads(response.body.decode())
        date=data['content']['topList']['updateTime']
        data=data['content']['topList']['data']
        items={}
        spus=[]
        temp=''
        x=0
        for i,tmp in enumerate(data):
            item = JdRealTimeTopItem()
            item['shop_name']=response.meta['Account']
            item['date']=date
            item['title']=tmp[0]
            item['xiadan_jine']=tmp[1]
            item['xiadan_danliang'] = tmp[2]
            item['xiandan_kehu'] = tmp[3]
            item['pv'] = tmp[4]
            item['uv']=tmp[5]
            item['change'] = tmp[6]
            item['spuid'] = str(tmp[7])
            item['top']=i+1
            item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # print(item)
            items[item['spuid']]=item
            temp+=item['spuid']+','
            if not (i+1)%10:
                temp=[temp[0:-1]]
                spus.append(temp)
                temp=''
        for tmp in spus:
            url='https://sz.jd.com/realTime/getImageUrlBySpuIds.ajax?spuIds='+''.join(tmp)
            yield scrapy.Request(url, headers=headers,callback=self.get_image,
                                 meta={'Account': response.meta['Account'],'item':items}, dont_filter=True)
            # break

    def get_image(self, response):
        temps=json.loads(response.body.decode())
        data=temps['content']['data']
        items=response.meta['item']
        for tmp in data:
            spuId=str(tmp['spuId'])
            item=items[spuId]
            imgSrc=tmp['imgSrc'].strip('/')
            item['imgurl']=imgSrc
            yield item

        # 'https://sz.jd.com/realTime/getImageUrlBySpuIds.ajax?spuIds=' \
        # '10258525985,10258526410,10258527558,10258528022,10258531787,10258534352,10258535141,10258535891,10258537000,10258537880'


    
    