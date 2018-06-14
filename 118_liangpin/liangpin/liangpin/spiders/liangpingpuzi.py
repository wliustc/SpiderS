# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import web
import json
from liangpin.items import LiangpinItem
db_query = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db_update = web.database()

# 通过高德id获取点评商店id
class LiangpingpuziSpider(scrapy.Spider):
    name = "liangpingpuzi"
    allowed_domains = ["amap.com"]
    start_urls = ['http://amap.com/']

    def start_requests(self):
        data = db_query.query('select amap_uid from t_xsd_liangpinpuzi_amap where review_id is null')
        for d in data:
            gaode_id = d.get('amap_uid')
            url = 'http://ditu.amap.com/detail/get/detail?id=%s' % gaode_id
            yield Request(url,callback=self.parse,meta={'gaode_id':gaode_id})

    def parse(self, response):
        response_json = json.loads(response.body)
        data = response_json.get('data')
        # print data
        if data:
            print data
            hospital = data.get('hospital')
            # print hospital
            if hospital:
                item = LiangpinItem()
                item['shop_id'] = hospital.get('src_id')
                item['gaode_id'] = response.meta['gaode_id']
                yield item
            else:
                review = data.get('review')
                if review:
                    comment = review.get('comment')
                    if comment:
                        review_id = comment[0].get('review_id')
                        item = LiangpinItem()
                        item['shop_id'] = review_id
                        item['gaode_id'] = response.meta['gaode_id']
                        yield item


