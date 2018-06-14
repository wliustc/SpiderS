# -*- coding: utf-8 -*-
import scrapy
import time
import re
from it_juzi.items import TiJuzi_newsfull
class ItjuziNewsSpider(scrapy.Spider):
    name = "itjuzi_news"
    allowed_domains = ["www.itjuzi.com/dailynews"]
    start_urls = ['http://www.itjuzi.com/dailynews/']

    def start_requests(self):
        yield scrapy.Request('https://www.itjuzi.com/user/login?redirect=index.php',headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Host':'www.itjuzi.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        },dont_filter=True,callback=self.request_login)

    def request_login(self,response):
        url='https://www.itjuzi.com/user/login?redirect=&flag=&radar_coupon='
        yield scrapy.FormRequest(url,headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.itjuzi.com',
            'Origin':'https://www.itjuzi.com',
            'Referer':'https://www.itjuzi.com/user/login',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        },formdata={
            'identity':'18210193504',
            'password':'543324797a.5',
            'remember':'1',
            'submit':'',
            'page':'',
            'url':'',
        },dont_filter=True,callback=self.denglu)

    def denglu(self,response):
        token_str=response.headers['Set-Cookie'].decode().split(';')[0]
        yield scrapy.Request('https://www.itjuzi.com/dailynews',headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.itjuzi.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        },dont_filter=True,callback=self.user_info,meta={'item':{'token_str':token_str}})

    def user_info(self,response):
        tiaoshu=response.css('.list-main-index span::text').extract()[0]
        tiaoshu=int(re.sub('[^0-9]+','',tiaoshu))
        page_num=tiaoshu//10+1+bool(tiaoshu%10)
        for i in range(1,page_num):
            url='https://www.itjuzi.com/dailynews?page=%s' %i
            header={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Host':'www.itjuzi.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_company_list)

    def get_company_list(self,response):
        temps=response.css('.incinfo.leri.long')
        for temp in temps:
            url=temp.css('.long.title.mart5 a::attr("href")').extract()[0]
            news_id=url.split('/')[-1]
            title = temp.css('.long.title.mart5 a::text').extract()[0]
            tag = '|'.join(temp.css('.scopes.c-gray-aset a b::text').extract())
            new_date=temp.css('.newsdate.c-gray span::text').extract()[0]
            source = temp.css('.newsdate.c-gray span::text').extract()[1]
            header={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'www.itjuzi.com',
                'If-Modified-Since':'Wed, 25 Oct 2017 02:32:08 GMT',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_news_page,
                                 meta={'item':{'news_id':news_id,'title':title,'tag':tag,
                                               'new_date':new_date,'source':source,
                                               }})


    def get_news_page(self,response):
        item=TiJuzi_newsfull()
        url=response.css('.subnav-news.flr a::attr("href")').extract()[0]
        item['news_id'] = response.meta['item']['news_id']
        item['title'] = response.meta['item']['title']
        item['tag']=response.meta['item']['tag']
        item['new_date'] = response.meta['item']['new_date']
        item['source'] = response.meta['item']['source']
        item['url']=url
        header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host':url.split('/')[2],
            'If-Modified-Since': 'Wed, 25 Oct 2017 02:32:08 GMT',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',

        }
        yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_item,
                             meta={'item': item}
                             )

    def get_item(self, response):
        item=response.meta['item']
        item['context']=response.body.decode(response.encoding)
        item['dt']=time.strftime('%Y-%m-%d',time.localtime())
        yield item
    
    