# -*- coding: utf-8 -*-
import scrapy
import MySQLdb
import time
from meituan_pet_server.items import MeituanPetAppcommentItem
class MeituanAppCommentSpider(scrapy.Spider):
    name = "meituan_app_comment"
    allowed_domains = ["i.meituan.com"]
    start_urls = ['http://i.meituan.com/']
    def start_requests(self):
        url = 'https://i.meituan.com/index/changecity'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_index_url, dont_filter=True)


    def get_index_url(self, response):
        url = 'https://i.meituan.com/index/changecity'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'i.meituan.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.get_city_id, dont_filter=True)

    def get_city_id(self,response):
        conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
                            connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("SELECT `meituan_id` as `mtshop_id` FROM hillinsight.pet_tuangou_hot_shop where `meituan_id` is not NULL;")
        tmps=cur.fetchall()
        for tmp in tmps:
            base_url='https://i.meituan.com/poi/%s/feedbacks/page_%s'
            if tmp['mtshop_id']=='NULL':
                continue
            url=base_url %(tmp['mtshop_id'],1)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,dont_filter=True,meta={'item':{'shop_id':tmp['mtshop_id'],'page_name':1}})

    def parse(self, response):
        datas=response.css('.feedbackCard')
        for data in datas:
            item=MeituanPetAppcommentItem()
            item['shop_id']=response.meta['item']['shop_id']
            item['user_name']=data.css('.username::text').extract()[0]
            item['total_score']=len(data.css('.stars i.icon-star'))
            item['comment_text']=''.join(data.xpath('./div[@class="comment"]//text()').extract())
            item['comment_dt']=data.css('weak.time::text').extract()[0]
            item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['hash']=hash(data.css('.username::text').extract()[0]+data.css('weak.time::text').extract()[0]+''.join(data.xpath('./div[@class="comment"]//text()').extract()))
            yield item
        if len(datas)<15:
            pass
        else:
            base_url='https://i.meituan.com/poi/%s/feedbacks/page_%s'
            page_num=response.meta['item']['page_name']
            page_num+=1
            url = base_url % (response.meta['item']['shop_id'], page_num)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'i.meituan.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,dont_filter=True,meta={'item':{'shop_id':response.meta['item']['shop_id'],
                                                                                   'page_name':page_num}})
    
    
    
    
    
    
    
    
    
    
    
    