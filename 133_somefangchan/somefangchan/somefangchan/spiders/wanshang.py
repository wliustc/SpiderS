# -*- coding: utf-8 -*-
import scrapy
from somefangchan.items import Somefangchan_yingshangItem
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class WanshangSpider(scrapy.Spider):
    name = "wanshang"
    allowed_domains = ["www.vanshang.com"]
    start_urls = ['http://www.vanshang.com/']

    def start_requests(self):
        url='http://www.vanshang.com/ProjectResourceIndex.asp'
        header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Host':'www.vanshang.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        yield scrapy.Request(url,headers=header,dont_filter=True,callback=self.get_quyu_type)

    def get_quyu_type(self,response):
        quyus=response.xpath(u"//span[text()='[所在区域]']/../span")
        for quyu in quyus:
            if quyu.css('::text').extract()[0]=='[所在区域]':
                continue
            url='http://www.vanshang.com/'+quyu.css('a::attr("href")').extract()[0]
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.vanshang.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_provice_list)

    def get_provice_list(self,response):
        provices = list(map(lambda x:{'provice':x.css("span::text").extract()[0],
                                 'url':'http://www.vanshang.com/'+x.css("::attr('href')").extract()[0]},response.xpath(u"//span[contains(text(),'[省')]/../a")))
        for provice in provices:
            if provice['provice']=='不限':
                continue
            url=provice['url']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.vanshang.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_end_list,meta={'item':{'now_page':1,'end_page':0,
                                                                                                                 'provice':provice['provice']},
                                                                                                         'base_url':url})
    def get_end_list(self,response):
        end_page=response.meta['item']['end_page']
        now_page=response.meta['item']['now_page']
        if end_page == 0:
            try:
            	end_page=int(response.xpath(u"//td[contains(text(),'共有')]/text()").extract()[1].split('/')[-1].strip())
            except Exception as e:
                return
        datas=response.xpath('//table[@onmouseout]/tr[1]/td[2]')
        for data in datas:
            item=Somefangchan_yingshangItem()
            item['title']=data.xpath('./table//table[1]/tr[1]/td/a/text()').extract()[0]
            item['provice']=response.meta['item']['provice']
            url= 'http://www.vanshang.com/'+data.xpath('./table//table[1]/tr[1]/td/a/@href').extract()[0]
            item['deal_id'] = url.split('=')[-1]
            item['address'] = data.xpath('./table//table[1]/tr[2]/td/text()').extract()[0]
            try:
            	item['statics'] = data.xpath('./table//table[1]/tr[3]/td/span/text()').extract()[0].split('：')[-1]
            except Exception as e:
                item['statics'] ='未知'
            item['mianji'] = data.xpath('./table//table[1]/tr[4]/td/text()').extract()[0].split('：')[-1]
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.vanshang.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_detail,
                    meta={'item': item})
        now_page+=1
        if now_page>end_page:
            return
        else:
            url=response.meta['base_url']+'&pageid=%s'%now_page
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.vanshang.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_end_list,
                    meta={'item':{'now_page':now_page,'end_page':end_page,'provice':response.meta['item']['provice']},'base_url':response.meta['base_url']})



    def get_detail(self,response):
        item=response.meta['item']
        try:
            item['city']=response.xpath('//table[2]//table/tr/td[2]/table/tr[2]/td[2]/text()').extract()[0]
        except Exception as e:
            return
        try:
            item['city']=item['city'].split('     ')[-1]
        except Exception as e:
            pass
        item['developer']=response.xpath('//table[2]//table/tr/td[2]/table/tr[2]/td[4]/text()').extract()[0]
        item['address']=response.xpath('//table[2]//table/tr/td[2]/table/tr[3]/td[2]/text()').extract()[0]
        item['connect_name']=response.xpath('//table[2]//table/tr/td[2]/table/tr[4]/td[2]/text()').extract()[0]
        item['connect_phone'] = response.xpath('//table[2]//table/tr/td[2]/table/tr[4]/td[4]/text()').extract()[0]
        item['connect_mphone'] = response.xpath('//table[2]//table/tr/td[2]/table/tr[5]/td[2]//text()').extract()[0]
        item['connect_email']=response.xpath('//table[2]//table/tr/td[2]/table/tr[6]/td[2]//text()').extract()[0]
        item['dt']=time.strftime('%Y-%m-%d',time.localtime())
        item['platform'] = '万商会'
        item['need']= response.xpath("//table[@bgcolor='#DADADA'][2]//td[@bgcolor='#FFFFFF']//text()").extract()[0].strip()
        yield item

    
    
    
    
    
    
    
    