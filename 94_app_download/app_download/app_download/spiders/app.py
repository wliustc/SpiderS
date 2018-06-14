# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import time
import re
start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
class AppSpider(scrapy.Spider):
    name = "app"
    allowed_domains = ["app.org"]
    # start_urls = ['http://www.wandoujia.com/apps/com.hupu.games ']
    def __init__(self,*args,**kwargs):
        super(AppSpider,self).__init__(*args,**kwargs)
        self.wandoujia_url = 'http://www.wandoujia.com/apps/{}'
        self.baidu_url = 'http://shouji.baidu.com/{}'
        self.huawei_url = 'http://app.hicloud.com/app/{}'
        self.oppo_url = 'http://store.oppomobile.com/product/{}'
        self.zhushou_url = 'http://zhushou.360.cn/detail/index/soft_id/{}'
        self.lenovo_url = 'http://www.lenovomm.com/app/{}'
        self.start_urls = []
    def start_requests(self):
        id_list = {u'豌豆荚':['com.gotokeep.keep','com.codoon.gps','com.hupu.games','com.tencent.qqsports','com.dongqiudi.news','com.yuedong.sport','com.imohoo.shanpao','com.bamboo.ibike','com.lflgvncbamboo.ibike','com.pplive.androidphone.sport','cn.ledongli.ldl'],
                   u'百度':['software/11557969.html','software/11558000.html','software/11461916.html','software/7102957.html','software/11512484.html','software/11421290.html','software/11511659.html','software/11529666.html','game/11477952.html','software/11531895.html','software/11457106.html','software/11423259.html'],
                   u'华为':['C134730','C10274914','C121952','C10325475','C10114803','C10144837','C10341299','C10088723','C10039377','C10096710','C10115026'],
                   'oppo':['0011/008/812_1.html?from=1152_1','0011/008/849_1.html?from=1152_1','0010/988/469_1.html?from=1152_1','0010/999/410_1.html?from=1152_1','0010/999/086_1.html?from=1152_1','0011/007/701_1.html?from=1152_1','0011/002/736_1.html?from=1152_1','0010/992/557_1.html?from=1152_1','0011/004/347_1.html?from=1152_1','0011/003/624_1.html?from=1152_1','0010/980/065_1.html?from=1152_1'],
                   u'360手机助手':['42908','2933398','189166','703380','1165595','1726950','3086240','820585','470402','366996','914330'],
                   u'乐商店':['21273339.html','21273168.html','21244677.html','21252417.html','21262859.html','21262580.html','21266714.html','21255391.html','21255092.html','21245607.html','21263071.html']}
        # id_list = {u'360手机助手':['189166']}
        for uid in id_list:
            if uid == u'豌豆荚':
                source = id_list.get(uid)
                for i in source:
                    url = self.wandoujia_url.format(i)
                    yield scrapy.Request(url,dont_filter=True,meta={'url':i,'uid':uid})
            elif uid == u'百度':
                source = id_list.get(uid)
                for i in source:
                    url = self.baidu_url.format(i)
                    yield  scrapy.Request(url,dont_filter=True,meta={'url':i,'uid':uid},callback=self.parse1)
            elif uid == u'华为':
                source = id_list.get(uid)
                for i in source:
                    url = self.huawei_url.format(i)
                    yield scrapy.Request(url, dont_filter=True, meta={'url': i, 'uid': uid}, callback=self.parse2)
            elif uid == 'oppo':
                source = id_list.get(uid)
                for i in source:
                    url = self.oppo_url.format(i)
                    yield scrapy.Request(url, dont_filter=True, meta={'url': i, 'uid': uid}, callback=self.parse3)
            elif uid == u'360手机助手':
                source = id_list.get(uid)
                for i in source:
                    url = self.zhushou_url.format(i)
                    yield scrapy.Request(url, dont_filter=True, meta={'url': i, 'uid': uid}, callback=self.parse4)
            elif uid == u'乐商店':
                source = id_list.get(uid)
                for i in source:
                    url = self.lenovo_url.format(i)
                    yield scrapy.Request(url, dont_filter=True, meta={'url': i, 'uid': uid}, callback=self.parse5)
    def parse(self, response):
        html = response.body
        item ={}
        app_name = Selector(text=html).xpath('//*[@class="app-name"]/span/text()').extract()
        download = Selector(text=html).xpath('//div[@class="num-list"]/span[1]/i/text()').extract()
        item['app_name'] = app_name[0]
        item['download'] = download[0]
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item
    def parse1(self, response):
        item = {}
        html = response.body
        app_name = Selector(text=html).xpath('//*[@class="app-name"]/span/text()').extract()
        download = Selector(text=html).xpath('//*[@class="detail"]/span[@class="download-num"]/text()').extract()
        if len(download[0]) !=0:
            download = download[0].split(':')[1]
        else:download=''
        item['app_name'] = app_name[0]
        item['download'] = download
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item

    def parse2(self, response):
        item = {}
        html = response.body
        app_name = Selector(text=html).xpath('//*[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract()
        download = Selector(text=html).xpath('//*[@class="app-info-ul nofloat"]/li/p/span[@class="grey sub"]/text()').extract()
        if len(download) !=0:
            download = re.findall('\d+',download[0])
        else:download=''
        item['app_name'] = app_name[0]
        item['download'] = download[0]
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item

    def parse3(self,response):
        item ={}
        html = response.body
        app_name = Selector(text=html).xpath('//*[@class="soft_info_middle"]/h3/text()').extract()
        download = Selector(text=html).xpath('//*[@class="soft_info_nums"]/text()').extract()
        download = ''.join(download).replace('\n','').replace(' ','')
        download = re.findall(u'\d+万|\d+',download)[0]
        item['app_name'] = app_name[0]
        item['download'] = download
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item

    def parse4(self,response):
        item ={}
        html = response.body
        app_name = ''.join(Selector(text=html).xpath('//*[@id="app-name"]/span/text()').extract())
        download = Selector(text=html).xpath('//*[@class="pf"]/span[@class="s-3"]/text()').extract()
        if len(download) != 0:
            download = re.findall(u'\d+万|\d+',download[0])[0]
        else:
            download = ''
        item['app_name'] = app_name
        item['download'] = download
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item


    def parse5(self, response):
        item ={}
        html = response.body
        app_name = ''.join(Selector(text=html).xpath('//*[@class="f18 fl"]/text()').extract())
        download = ''.join(Selector(text=html).xpath('//*[@class="f12 detailDownNum cb clearfix"]/span[@class="fgrey5"]/text()').extract())
        if len(download) != 0:
            download = re.findall(u'\d+万|\d+',download)[0]
        else:
            download = ''
        item['app_name'] = app_name
        item['download'] = download
        item['source'] = response.meta['uid']
        item['time'] = start_time
        yield item

    
    