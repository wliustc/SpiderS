# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import re
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
cookies ={
# 'WAF_SESSION_ID':'a87057c8aca77a8abada10319d4cedc4',
'UtzD_f52b_saltkey':'eOgGg8Sz',
'UtzD_f52b_lastvisit':'1516259798',
'yaozh_uidhas':'1',
'UtzD_f52b_ulastactivity':'1516014343%7C0',
'yaozh_mylogin':'1516345506',
'think_language':'zh-CN',
'PHPSESSID':'k52jpkvtuk6mtqfnfophj42qm2',
'expire':'1516442506748',
# '_ga':'GA1.2.1922947084.1516259794',
'_gid':'GA1.2.729418897.1516259806',
'yaozh_logintime':'1516356136',
'yaozh_user':'373871%09hillhouse',
'yaozh_userId':'373871',
'db_w_auth':'361484%09hillhouse',
'UtzD_f52b_lastact':'1516356137%09uc.php%09',
'UtzD_f52b_auth':'d98aPlJ7%2BlQjHBvOTsN2qaiRb63x9cHPWuYLVA9a3BNwOfJf4Djf6yNCK3hyjyt29PqnkSQaOQovPuFrOZPbpIoEM38',
'_ga':'GA1.3.1922947084.1516259794',
'Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94':'1516259794%2C1516328536%2C1516345508,1516356100',
'Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94':'1516356141',
'WAF_SESSION_ID':'483120277432773cd4a869d700e6c61e'
}
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Connection':'keep-alive',
           'Host':'db.yaozh.com',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
class YaozhiSpider(scrapy.Spider):
    name = 'YaoZhi'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(YaozhiSpider,self).__init__(*args,**kwargs)
        self.url = 'https://db.yaozh.com/hmap?grade=%E4%B8%89%E7%BA%A7%E7%94%B2%E7%AD%89&pageSize=30&province=%E5%8C%97%E4%BA%AC%E5%B8%82&type=%E7%BB%BC%E5%90%88%E5%8C%BB%E9%99%A2&p=1'
        self.city_url = '''https://db.yaozh.com/hmap?grade={level}&pageSize=30&province={province}&type={type_}&p={page}'''
    def start_requests(self):
        url = self.url
        # url = 'https://db.yaozh.com/hmap/39762.html'
        yield scrapy.Request(url,cookies=cookies,headers=headers,dont_filter=True,meta={'url':url})
        # yield scrapy.Request(url,cookies=cookies,headers=headers,dont_filter=True,callback=self.parse_home,meta={'province':'aa','level':'dd','type_':'sss','url':url})
        # yield scrapy.Request(url,cookies=cookies,headers=headers,dont_filter=True,callback=self.parse_)

    def parse(self, response):
        html = response.body
        level_list = ['三级甲等','三级乙等','三级未定','二级甲等','二级乙等','二级未定','一级甲等','一级乙等','一级未定']
        type_list = [ u'\u7efc\u5408\u533b\u9662', u'\u4e2d\u533b\u533b\u9662', u'\u4e2d\u897f\u533b\u7ed3\u5408\u533b\u9662', u'\u4e13\u79d1\u533b\u9662', u'\u6c11\u65cf\u533b\u9662', u'\u5987\u5e7c\u4fdd\u5065\u9662', u'\u4e13\u79d1\u75be\u75c5\u9632\u6cbb\u9662\uff08\u6240\u3001\u7ad9\uff09', u'\u62a4\u7406\u9662', u'\u7597\u517b\u9662', u'\u793e\u533a\u536b\u751f\u670d\u52a1\u4e2d\u5fc3', u'\u4e61\u9547\u536b\u751f\u9662', u'\u75be\u75c5\u9884\u9632\u63a7\u5236\u4e2d\u5fc3', u'\u8ba1\u5212\u751f\u80b2\u670d\u52a1\u4e2d\u5fc3', u'\u95e8\u8bca\u90e8', u'\u8bca\u6240']
        province_list = [ u'\u5317\u4eac\u5e02',u'\u5929\u6d25\u5e02', u'\u6cb3\u5317\u7701', u'\u5c71\u897f\u7701', u'\u5185\u8499\u53e4', u'\u8fbd\u5b81\u7701', u'\u5409\u6797\u7701', u'\u9ed1\u9f99\u6c5f\u7701', u'\u4e0a\u6d77\u5e02', u'\u6c5f\u82cf\u7701', u'\u6d59\u6c5f\u7701', u'\u5b89\u5fbd\u7701', u'\u798f\u5efa\u7701', u'\u6c5f\u897f\u7701', u'\u5c71\u4e1c\u7701', u'\u6cb3\u5357\u7701', u'\u6e56\u5317\u7701', u'\u6e56\u5357\u7701', u'\u5e7f\u4e1c\u7701', u'\u5e7f\u897f', u'\u6d77\u5357\u7701', u'\u91cd\u5e86\u5e02', u'\u56db\u5ddd\u7701', u'\u8d35\u5dde\u7701', u'\u4e91\u5357\u7701', u'\u897f\u85cf', u'\u9655\u897f\u7701', u'\u7518\u8083\u7701', u'\u9752\u6d77\u7701', u'\u5b81\u590f', u'\u65b0\u7586']

        # type_list = []
        # province_list = []
        # type_S = ''.join(re.findall('data-names="type" data-list=\'(.*?)\' data-src=""',html,re.S)).replace('[','').replace(']','')
        if len(level_list):#type_S
        #     for i in ''.join(re.findall('data-names="type" data-list=\'(.*?)\' data-src=""',html,re.S)).replace('[','').replace(']','').split(r',{'):
        #         if i[0]!='{':
        #             i = '{'+i
        #         h = json.loads(i)
        #         type_list.append(h.get('name'))
        #     for _ in ''.join(re.findall('data-names="province" data-list=\'(.*?)\' data-src=""',html,re.S)).replace('[','').replace(']','').split(r',{'):
        #         if _[0]!='{':
        #             _ = '{'+_
        #         hh = json.loads(_)
        #         province_list.append(hh.get('name'))
        #     print type_list,province_list
            for level in level_list:
                for type_ in type_list:#[1:2]
                    for province in province_list:#[1:2]
                        url = self.city_url.format(level=level,province=province,type_=type_,page=1)
                        yield scrapy.Request(url,meta={'province':province,'level':level,'type_':type_,'url':url},cookies=cookies,headers=headers,dont_filter=True,callback=self.parse_home)
        else:
            url = response.meta['url']
            yield scrapy.Request(url, cookies=cookies, headers=headers, dont_filter=True, meta={'url': url},callback=self.parse)
    def parse_home(self,response):
        html = response.body
        province = response.meta['province']
        level = response.meta['level']
        type_ = response.meta['type_']
        list_url = response.meta['url']
        len_list = []

        for x in re.findall('<th><a class="cl-blue" href="(.*?)" target',html,re.S):
            item ={}
            url = 'https://db.yaozh.com'+''.join(x)
            len_list.append(url)
            item['url'] = url
            item['province'] = province
            item['level'] = level
            item['type_'] = type_
            item['page_url'] = list_url
            yield item

        page = ''.join(re.findall('data-total="(.*?)" data-size', html, re.S))
        if len(page):
            page,remainder = divmod(int(page),30)
            page = int(page)
            if remainder != 0:
                page +=1
            for pag in range(2,page+1):
                url_split = list_url.split('&p=')
                url = url_split[0] + '&p=' + str(pag)
                yield scrapy.Request(url,callback=self.parse_homes,dont_filter=True,meta={'url':url,'province':province,'level':level,'type_':type_},cookies=cookies,headers=headers)

    def parse_homes(self,response):
        html = response.body
        province = response.meta['province']
        level = response.meta['level']
        type_ = response.meta['type_']
        list_url = response.meta['url']
        for x in re.findall('<th><a class="cl-blue" href="(.*?)" target',html,re.S):
            item ={}
            url = 'https://db.yaozh.com'+''.join(x)
            item['url'] = url
            item['province'] = province
            item['level'] = level
            item['type_'] = type_
            item['page_url'] = list_url
            yield item










