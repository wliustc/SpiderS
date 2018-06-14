# -*- coding: utf-8 -*-
import scrapy
import web
import time
import re
import random
import urllib
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

class HuaniaoSpider(scrapy.Spider):
    name = 'huaniao_new'
    allowed_domains = ['huaniao.org']
    start_urls = ['http://huaniao.org/']
    def __init__(self,*args,**kwargs):
        super(HuaniaoSpider,self).__init__(*args,**kwargs)
        self.data_api = 'https://detail.tmall.com/item.htm?id={}'

    def start_requests(self):
        citys = ['北京', '上海', '广州', '深圳', '杭州', '海外', '江浙沪', '珠三角', '京津冀', '东三省', '港澳台', '江浙沪皖', '长沙',
                 '长春', '成都', '重庆', '大连', '东莞', '佛山', '福州', '贵阳', '合肥', '金华', '济南', '嘉兴', '昆明', '宁波',
                 '南昌', '南京', '青岛', '泉州', '沈阳', '苏州', '天津', '温州', '无锡', '武汉', '西安', '厦门', '郑州', '中山',
                 '石家庄', '哈尔滨', '安徽', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '湖北', '湖南',
                 '江苏', '江西', '吉林', '辽宁', '宁夏', '青海', '山东', '山西', '陕西', '云南', '四川', '西藏', '新疆',
                 '浙江', '澳门', '香港', '台湾', '内蒙古', '黑龙江']
        sql = '''select * from t_spider_xianhua_id  limit 3000,200 '''
        for i in db.query(sql):
            uid = i.get('uid')
            url = self.data_api.format(uid)
            yield scrapy.Request(url,dont_filter=True,meta={'uid':uid})

    def parse(self, response):
        item = {}
        try:
            html = response.body.decode('gbk')
        except:
            html = response.body
        if re.findall(u'很抱歉，您查看的宝贝不存在，可能已下架或者被转移|很抱歉，您查看的商品找不到了',html):
            pass
        else:
            uid = response.meta['uid']
            if 'detail.tmall' in response.url:
                item['uid'] = uid
                item['sag'] = '天猫'
            elif 'item.taobao' in response.url:
                item['uid'] = uid
                item['sag'] = '淘宝'
            yield item




    def parse1(self, response):
        html = response.body
        url = response.meta['url']
        page = response.meta['page']
        key = response.meta['key']
        key_word = response.meta['key_word']
        city = response.meta['city']
        try:
            if re.findall(r'所有分类',html):
                pages = re.findall('totalPage":(.*?),"currentPage"', html)[0]
                data = re.findall('allNids":(.*?),"cat"', html, re.S)
                if len(data):
                    item = {}
                    html = html[11:-2]
                    item['data'] = html
                    item['key_word'] = response.meta['key']
                    item['city'] = urllib.unquote(city)
                    item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    yield item
                    for i in range(1,int(pages)):
                        time_ = str(int(round(time.time() * 1000))) + '_' + str(random.randint(100, 1000))
                        random_ = random.randint(100, 1000)
                        page = page + 60
                        url = self.data_api.format(page=page,time=time_,random=random_,key=key,key_word=key_word,city=city)
                        yield scrapy.Request(url,meta={'url':url,'key':key,'page':page,'key_word':key_word,'city':city,'data_list':data},dont_filter=True,callback=self.page_parse)

            else:
                yield scrapy.Request(url, meta={'url':url,'key': key, 'page': page, 'key_word': key_word,'city':city}, dont_filter=True,
                                     callback=self.parse)
        except:
            yield scrapy.Request(url, meta={'url': url, 'key': key, 'page': page, 'key_word': key_word, 'city': city},
                                 dont_filter=True,
                                 callback=self.parse)
    def page_parse(self,response):
        html = response.body
        data_list = response.meta['data_list']
        url = response.meta['url']
        page = response.meta['page']
        key = response.meta['key']
        key_word = response.meta['key_word']
        city = response.meta['city']
        try:
            if re.findall(r'所有分类', html):

                data = re.findall('allNids":(.*?),"cat"', html, re.S)
                if len(data):
                    data = data[0].replace('[', '').replace(']', '').split(',')
                    if data !=data_list:
                        item = {}
                        html = html[11:-2]
                        item['data'] = html
                        item['key_word'] = response.meta['key']
                        item['city'] = urllib.unquote(city)
                        item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                        yield item
                    else:
                        print '#'*30
            else:
                yield scrapy.Request(url, meta={'url':url,'key': key, 'page': page, 'key_word': key_word,'city':city,'data_list':data_list}, dont_filter=True,
                                     callback=self.page_parse)
        except:
            yield scrapy.Request(url, meta={'url': url, 'key': key, 'page': page, 'key_word': key_word, 'city': city,'data_list':data_list},
                                 dont_filter=True,
                                 callback=self.page_parse)




    
    