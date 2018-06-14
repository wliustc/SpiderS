# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
from weather.items import Weatherhttp3Item
import time
import datetime
from scrapy import log
class TutiempoSpider(scrapy.Spider):
    name = "tutiempo"
    allowed_domains = ["en.tutiempo.net"]
    start_urls = ['http://en.tutiempo.net/']

    def start_requests(self):
        data=[('北京','BEIJING'),('上海','SHANGHAI')]
        data=pd.DataFrame(data,columns=['城市','城市英文名称'])
        data = data.dropna()
        datas = list(zip(data['城市'].tolist(), data['城市英文名称'].tolist()))
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'en.tutiempo.net',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        url='https://en.tutiempo.net/climate/china.html'
        yield scrapy.Request(url,dont_filter=True,callback=self.get_city_list,
                             headers=header,meta={'item':{'databiaozhun':datas},'page':1})
    def get_city_list(self,response):
        page=response.meta['page']
        if page==1:
            end_page=int(response.xpath('//li[@class="siguiente"]/a[text()="Last"]/@href').extract()[0].split('/')[-2])
            city_data=pd.DataFrame(columns=['city','url','city_name'])
        else:
            end_page=response.meta['item']['end_page']
            city_data = response.meta['item']['data']
        city_data=city_data.append(self.get_city_list_content(response))
        if page>=end_page:
            databiaozhun=response.meta['item']['databiaozhun']
            city_data['city']=city_data['city'].map(lambda x:x.lower())
            city_data=city_data.reset_index()
            for temp in databiaozhun:
                city_data['city_name'].loc[city_data[city_data['city']==temp[1].lower()].index]=temp[0]
            city_data.dropna(inplace=True)
            for index, temp in city_data.iterrows():
                url=temp['url']
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Host': 'en.tutiempo.net',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                }
                yield scrapy.Request(url, dont_filter=True, callback=self.get_city_date_list,
                                     headers=header, meta={'item': {'city_name':temp['city_name'],'city':temp['city']}})
            return
        page += 1
        url = 'https://en.tutiempo.net/climate/china/%s/' % page
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'en.tutiempo.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        yield scrapy.Request(url, dont_filter=True, callback=self.get_city_list,
                             headers=header, meta={'item': {'databiaozhun':response.meta['item']['databiaozhun'],'data': city_data,'end_page':end_page}, 'page': page})

    def get_city_list_content(self,response):
        datas=response.css('div.mlistados ul li a')
        datas=list(map(lambda x:{'city':x.css("::text").extract()[0].strip(),'url':'https://en.tutiempo.net'+x.css("::attr('href')").extract()[0]},datas))
        datas=pd.DataFrame(datas)
        return datas

    def get_city_date_list(self,response):
        city_latitude=response.xpath('//p[@class="mt5"]/b[1]/text()').extract()[0]
        city_longitude = response.xpath('//p[@class="mt5"]/b[2]/text()').extract()[0]
        if response.css('.mlistados a::attr("href")'):
            year_url_list=list(map(lambda x:{'year':re.sub('[^0-9]+','',x.css('::text').extract()[0]),
                                        'url':'https://en.tutiempo.net'+x.css("::attr('href')")},
                                response.css('.mlistados a')))
        elif response.css('.minoverflow a'):
            year_url_list=list(map(lambda x:{'year':re.sub('[^0-9]+','',x.css('strong::text').extract()[0]),
                                        'url':'https://en.tutiempo.net'+x.css("::attr('href')").extract()[0]},
                                response.css('.minoverflow a')))
        else:
            log.msg('CANNOT FIND TEMP URL=%s' % response.url, level=log.ERROR)
        for year in year_url_list:
            data = response.meta['item'].copy()
            data['city_latitude']=city_latitude
            data['city_longitude']=city_longitude
            data['year'] = year['year']
            if not data['year'] in ['2010','2011','2012','2013','2014','2015','2016','2017']:
                continue
            url = year['url']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'en.tutiempo.net',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_city_month_list,meta={'item':data})

    def get_city_month_list(self,response):

        temps=map(lambda x:{'month':x.css('::text').extract()[0],
                            'url':'https://en.tutiempo.net'+x.css('::attr("href")').extract()[0]},response.css('.mlistados a'))
        for temp in temps:
            data=response.meta['item'].copy()
            data['month']=temp['month']
            url=temp['url']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'en.tutiempo.net',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_city_item,meta={'item':data})

    def get_city_item(self,response):
        trs=response.css('.mt5.minoverflow tr')
        for i,tr in enumerate(trs):
            if i==0:
                continue
            try:
                day=int(tr.xpath('./td[1]/strong/text()').extract()[0])
            except Exception as e:
                continue
            item=Weatherhttp3Item()
            if response.meta['item']['city']=='yichun':
                if response.meta['item']['city_latitude']=='27.9' and response.meta['item']['city_longitude']=='114.38':
                    response.meta['item']['city_name']='宜春'
                else:
                    response.meta['item']['city_name'] = '伊春'
            item['city'] = response.meta['item']['city']
            item['city_name']=response.meta['item']['city_name']
            item['city_latitude'] = response.meta['item']['city_latitude']
            item['city_longitude'] = response.meta['item']['city_longitude']
            date=response.meta['item']['year']+'-'+response.meta['item']['month']+'-'+str(day)
            item['date']=datetime.datetime.strptime(date,"%Y-%B-%d").strftime('%Y-%m-%d')
            item['T']=tr.xpath('./td[2]/text()').extract()[0].strip()   #平均温度
            item['Tmax']=tr.xpath('./td[3]/text()').extract()[0].strip()  #最高温度
            item['Tmin']=tr.xpath('./td[4]/text()').extract()[0].strip() #最低温度
            item['PP']=tr.xpath('./td[7]/text()').extract()[0].strip()#降雨量
            item['dt']=time.strftime('%Y-%m-%d',time.localtime())
            yield item

    
    
    