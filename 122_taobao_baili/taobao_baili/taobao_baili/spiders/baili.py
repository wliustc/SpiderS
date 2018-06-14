# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Selector
import web
import sys
reload(sys)
import time
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')


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
    'referer':'https://ebelle.tmall.com/category-1292664281.htm?spm=a1z10.3-b-s.w4011-14900313032.339.46f16db0Sc9FHC&search=y&scene=taobao_shop&catId=1292664281&pageNo=9&tsearch=y'
    }
class BailiSpider(scrapy.Spider):
    name = 'baili'
    allowed_domains = ['baili.org']
    # start_urls = ['https://ebelle.tmall.com/category-1292664281.htm?spm=a1z10.3-b-s.w4011-14900313032.339.46f16db0Sc9FHC&search=y&scene=taobao_shop&catId=1292664281&pageNo=9&tsearch=y#anchor']
    def __init__(self,*args,**kwargs):
        super(BailiSpider,self).__init__(*args,**kwargs)
        self.js = 'https://rate.tmall.com/list_detail_rate.htm?itemId={data_id}&spuId=868875336&sellerId=167873659&order=3&currentPage={pag}&append=0&content=1&tagId=&posi=&picture=&_ksTS=1505205914999_1308&callback=jsonp1309'
    def start_requests(self):
        sql = ''' SELECT DISTINCT dataid FROM `t_xsd_tianmao_id` where dataid=41636955268 '''
        for i in db.query(sql):
            data_id = i.get('dataid')
            url = self.js.format(data_id=data_id,pag=1)
            yield scrapy.Request(url,dont_filter=True,meta={'data_id':data_id,'url':url},headers=ua,cookies=cookies)



    def parse(self, response):
        item ={}
        data_url = response.meta.get('url')
        dataid = response.meta.get('data_id')
        html = response.body
        try:
            data = json.loads(html.decode('gbk').encode('utf8')[27:-2])
            pag = data.get('paginator').get('items')
            if int(pag) == 0:
                pass
            else:
                pag = int(pag) /20+1
                if pag >1 and pag <99:
                    for pa in range(2,int(pag)+1):
                        url = self.js.format(data_id=dataid,pag=pa)
                        yield scrapy.Request(url,meta={'data_id':dataid,'url':url},dont_filter=True,callback=self.parse_commentaries,headers=ua,cookies=cookies)
                elif pag > 99:
                    for pa in range(2,99+1):
                        url = self.js.format(data_id=dataid, pag=pa)
                        yield scrapy.Request(url,meta={'data_id':dataid,'url':url},dont_filter=True,callback=self.parse_commentaries,headers=ua,cookies=cookies)
                for i in data['rateList']:
                    rateContent = i.get('rateContent')
                    rateDate = i.get('rateDate')
                    name = i.get('displayUserNick')
                    item['commentaries'] = rateContent
                    item['score_time'] = rateDate
                    item['comments_name'] = name
                    item['code'] = dataid
                    item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                    item['url'] = response.meta.get('url')
                    yield item
        except:
            url = data_url
            yield scrapy.Request(url,meta={'data_id':dataid,'url':url},cookies=cookies,headers=ua,dont_filter=True,callback=self.parse)


    def parse_commentaries(self, response):
        item ={}
        html = response.body

        try:
            dataid = response.meta['data_id']
            data = json.loads(html.decode('gbk').encode('utf8')[27:-2])
            for i in data['rateList']:
                rateContent = i.get('rateContent')
                rateDate = i.get('rateDate')
                name = i.get('displayUserNick')
                item['commentaries'] = rateContent
                item['score_time'] = rateDate
                item['comments_name'] = name
                item['code'] = dataid
                item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
                item['url'] = response.meta.get('url')
                yield item
        except:
            dataid = response.meta.get('data_id')
            url = response.meta.get('url')
            yield scrapy.Request(url, meta={'data_id': dataid, 'url': url}, cookies=cookies, headers=ua,dont_filter=True, callback=self.parse_commentaries)

