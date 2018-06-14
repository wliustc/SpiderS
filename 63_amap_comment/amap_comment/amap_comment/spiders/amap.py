# -*- coding: utf-8 -*-
import scrapy
from amap_comment.items import MapGapdeItem
import time
import sys
import json
import web
reload(sys)
sys.setdefaultencoding('utf-8')

class AmapSpider(scrapy.Spider):
    name = "amap"
    allowed_domains = ["http://ditu.amap.com"]
    DIANPU_FORMAT='http://ditu.amap.com/detail/%s'

    def start_requests(self):
	db = web.database(dbn='mysql',db='pet_cloud',user='work',pw='phkAmwrF',port=3306,host='10.15.1.14')
	#brand = '宠颐生'.encode('utf-8')
      #  sql='''select gaodemap_id from `pet_cloud`.`hospital_base_information` where brand='%s';''' % brand
        sql='''select gaodemap_id from `pet_cloud`.`hospital_base_information`;''' 
	temps = db.query(sql)
	temps = list(temps)
        for temp in temps:
            print temp
            url= self.DIANPU_FORMAT % temp['gaodemap_id']
            yield scrapy.Request(url,meta={'item':{'uid':temp['gaodemap_id']}})


    def parse(self, response):
        item=MapGapdeItem()
        uid=response.meta['item']['uid']
        try:
            comment_score= response.css('.score::text').extract()[0]
        except Exception as e:
            comment_score=''
        item['uid']=uid
        item['comment_id']=''
        item['user_id']=''
        item['comment_score']=''
        item['comment_text']=''
        item['comment_dt']=''
        item['write_time']=''
        item['comments_avg']=comment_score
        item['pt_jobid']=''
        item['insert_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        yield item
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    