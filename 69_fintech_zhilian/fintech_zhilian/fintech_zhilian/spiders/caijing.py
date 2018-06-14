# -*- coding: utf-8 -*-
import scrapy
from fintech_zhilian.spiders import spider_list
from fintech_zhilian import items
import time
import re

#http://sou.zhaopin.com/jobs/companysearch.ashx?CompID=CC156038613
class CaijingSpider(scrapy.Spider):
    name = "caijing"
    allowed_domains = ["http://sou.zhaopin.com/"]

    def start_requests(self):       #生成每个公司和每个省的搜索链接
        self.provice_list=spider_list.provice_list
        self.search_word=spider_list.search_word
        self.key_word_list=spider_list.key_word_list
        request_list=[]
        for search_word in self.search_word:
            for provice_list in self.provice_list:
                request_list.append(scrapy.http.Request(
                    url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&kt=2' %(provice_list,search_word),
                    dont_filter=True,meta={'item':{'provice':provice_list,'search_word':search_word}}))
        return request_list

    def parse(self, response):  #遍历搜索结果的每一页
        provice_list=response.meta['item']['provice']
        search_word = response.meta['item']['search_word']
        search_num=int(response.css('.search_yx_tj em::text').extract()[0])
        page=(search_num + 20-1)//20
        for i in range(1,page+1):
            yield scrapy.http.Request(
                url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&kt=2&p=%s' % (provice_list, search_word,i),
                dont_filter=True,callback=self.get_list)

    def get_list(self,response):    #得到每一页的每个职位
        newlists = response.css('#newlist_list_content_table table[class=newlist]')
        for newlist in newlists:
            try:
                tr = newlist.css('tr td')[0]
                href = tr.css('div a::attr("href")').extract()[0]
                id = href.split('/')[-1].split('.')[0]
                yield scrapy.Request(href, dont_filter=True, callback=self.get_detial,
                                     meta={'item': {'href': href,
                                                    'id': id}})
            except Exception as e:
                pass

    def get_detial(self,response):  #进入职位的详情页并且获得信息
        recruit=items.ZhilianCampanyItem()

        recruit['Job_title']=response.css('.top-fixed-box .inner-left >h1')[0].css('::text').extract()[0]
        recruit['company'] = response.css('.top-fixed-box .inner-left > h2 > a')[0].css('::text').extract()[0]
        # recruit['compid'] =response.meta['item']['compid']
        recruit['payment'] = response.css('.terminalpage-left .terminal-ul li:nth-child(1) strong::text').extract()[0]
        recruit['recruiting_city'] = response.css('.terminalpage-left .terminal-ul li:nth-child(2) strong a::text').extract()[0]
        recruit['release_time'] = response.css('.terminalpage-left .terminal-ul li:nth-child(3) strong span::text').extract()[0]
        recruit['Job_describe'] = response.css('.terminalpage-left .terminal-ul li:nth-child(4) strong::text').extract()[0]
        recruit['experience'] = response.css('.terminalpage-left .terminal-ul li:nth-child(5) strong::text').extract()[0]
        recruit['learn'] = response.css('.terminalpage-left .terminal-ul li:nth-child(6) strong::text').extract()[0]
        recruit['number'] = response.css('.terminalpage-left .terminal-ul li:nth-child(7) strong::text').extract()[0]
        recruit['Job_type'] = response.css('.terminalpage-left .terminal-ul li:nth-child(8) strong a::text').extract()[0]
        recruit['source']='智联招聘'
        bewrites = response.css('.tab-cont-box .tab-inner-cont')[0].css('*')
        bewrite=''
        for temp in bewrites:
            try:
                bewrite =bewrite+temp.css('::text').extract()[0]
            except Exception as e:
                pass
        bewrite=bewrite.strip()
        recruit['Job_describe']=bewrite
        recruit['task_time']=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        keyword=''
        for temp in self.key_word_list:
            if re.findall(temp,bewrite):
                keyword+=temp+'、'
        yield recruit



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    