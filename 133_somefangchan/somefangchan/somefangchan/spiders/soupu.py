# -*- coding: utf-8 -*-
import scrapy
import re
import time
from somefangchan.items import Somefangchan_yingshangItem
class SoupuSpider(scrapy.Spider):
    name = "soupu"
    allowed_domains = ["www.soupu.com"]
    start_urls = ['http://www.soupu.com/']

    def start_requests(self):
        url='http://www.soupu.com/Login.aspx?ReturnUrl=http%3a%2f%2fwww.soupu.com%2fUIPro%2fBusniessProject.aspx'
        header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Host':'www.soupu.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_type)

    def get_type(self,response):
        datas=response.xpath("//input[@type='hidden']")
        item_data={}
        for temp in datas:
            item_data[temp.css('::attr("name")').extract()[0]]=temp.css('::attr("value")').extract()[0]
        item_data['btnLogin']='登　录'
        item_data['tbPassWord']='543324797'
        item_data['tbUserName'] = '18210193504'
        header={
        'Upgrade-Insecure-Requests':'1',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        }
        url='http://www.soupu.com/Login.aspx?ReturnUrl=http%3a%2f%2fwww.soupu.com%2fUIPro%2fBusniessProject.aspx'
        yield scrapy.FormRequest(url,headers=header,
                                 formdata=item_data,dont_filter=True,callback=self.get_dengluhou)

    def get_dengluhou(self,response):
        tepms=map(lambda x:{'city':x.css('::text').extract()[0],'url':'http://www.soupu.com'+x.css('::attr("href")').extract()[0]}
                  ,response.xpath("//div[contains(@class,'section')][1]//dd/a[not(@class)]"))
        tepms=list(tepms)
        for tepm in tepms:
            url=tepm['url']
            yield scrapy.Request(url,headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'www.soupu.com',
                'Referer':'http://www.soupu.com/UIPro/BusniessProject.aspx',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            },dont_filter=True,callback=self.get_city_page,meta={'item':{'city':tepm['city'],'end_page':1,'page':1},'base_url':url})

    def get_city_page(self,response):
        now_page=response.meta['item']['page']
        end_page=response.meta['item']['end_page']
        bodys=response.css('div.table_style2')
        for body in bodys:
            item=Somefangchan_yingshangItem()
            item['deal_id']=body.css('.title::attr("href")').extract()[0].split('=')[-1]
            item['provice']=response.meta['item']['city']
            item['title']=body.css('.title::text').extract()[0]
            item['distract']=body.css('tr:nth-child(2) td:nth-child(1)::text').extract()[0].split('：')[1]
            item['city']=item['distract'].split('-')[0]
            try:
            	item['city']=item['distract'].split('-')[0]
            except Exception as e:
                pass
            item['statics']=body.css('tr:nth-child(2) td:nth-child(2)::text').extract()[0].split('：')[1]
            item['need']=body.css('tr:nth-child(4) p::text').extract()[0].split('：')[1]
            url = 'http://www.soupu.com/UIPro/'+body.css('.title::attr("href")').extract()[0]
            yield scrapy.Request(url,headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'www.soupu.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            },dont_filter=True,callback=self.get_deal_detail,meta={'item':item})
        if end_page==1:
            try:
                end_page=int(re.sub('[^0-9]+','',response.xpath('//div[@id="ctl00_main_listProjcet_AspNetPager1"]/a/@title').extract()[-1]))
            except Exception as e:
                print(e)
                pass
        now_page+=1
        if now_page>end_page:
            return
        else:
            url=response.meta['base_url']+'&page=%s' %now_page
            yield scrapy.Request(url,headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'www.soupu.com',
                'Referer':'http://www.soupu.com/UIPro/BusniessProject.aspx',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            },dont_filter=True,callback=self.get_city_page,meta={'item':{'city':response.meta['item']['city'],
                                                                         'end_page':end_page,'page':now_page},'base_url':response.meta['base_url']})


    def get_deal_detail(self,response):
        item=response.meta['item']
        item['developer']=''.join(response.css('.tabpc_text dl dt p:nth-child(1)::text').extract()).split('：')[1]
        item['type']=response.css('.tabpc_text dl p:nth-child(2)::text').extract()[0].split('：')[1]
        item['mianji'] = response.css('.tabpc_text dl p:nth-child(3)::text').extract()[0].split('：')[1]
        item['address']= response.xpath('//div[@class="tabpc_text"]/p/text()').extract()[0].split('：')[1]
        url='http://www.soupu.com'+response.css('dt.c_fl a::attr("href")').extract()[0]
        yield scrapy.Request(url,headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Host':'www.soupu.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            },dont_filter=True,callback=self.get_connect,meta={'item':item})

    def get_connect(self,response):
        item=response.meta['item']
        try:
        	item['connect_name']=response.css('h2.a_ui strong::text').extract()[0]
        except Exception as e:
            pass
        try:
            item['connect_duty']=response.css('h2.a_ui span::text').extract()[0]
        except Exception as e:
            pass
        try:
            item['connect_phone']=response.css('h2.a_ui ~ ul li:nth-child(1)::text').extract()[0]
        except Exception as e:
            pass
        try:
            item['connect_mphone']=response.css('h2.a_ui ~ ul li:nth-child(2)::text').extract()[0]
        except Exception as e:
            pass
        item['platform']='搜铺'
        item['dt']=time.strftime('%Y-%m-%d',time.localtime())
        yield item
    
    
    