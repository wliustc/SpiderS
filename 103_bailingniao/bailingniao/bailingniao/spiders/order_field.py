# coding=utf8
import sys
import scrapy
from scrapy import Request
import json
import web
from bailingniao.items import BailingniaoOrderFieldItem
reload(sys)
sys.setdefaultencoding('utf-8')
header = {
    'Tingyun-Process': 'true',
    'Content-Type': 'application/json;Charset=UTF-8',
    'Accept-Language': 'zh,zh-cn',
    'APPVersion': '2.0',
    'appChannel': 'v_1037',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Letv X500 Build/DBXCNOP5902605181S)',
    'Host': 'android.prod.quncaotech.com'
}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class BlnSpider(scrapy.Spider):
    name = "blnorderfield"
    allowed_domains = ["quncaotech.com"]

    # start_urls = ['http://quncaotech.com/']

    def start_requests(self):
        data = db.query(
            'select * from t_spider_bailingniao_field where task_time in (select max(task_time) from t_spider_bailingniao_field);')
        for d in data:
            # print type(d)
            field_id = d.get('field_id')
            category = d.get('category')
            category_list = category.split(';')
            for category in category_list:
                category_json = json.loads(category)
                category_id = category_json.get('id')
                category_name = category_json.get('name')
                # print category_id, category_name
                url = 'http://android.prod.quncaotech.com/api/place/order/placeSalePlan'
                post_body = '{"ver":"2.7.9","protocol_ver":1,"platformType":2,"placeId":' + str(field_id) + ',"categoryId":' + str(category_id) + ',"startDate":1498020080069,"endDate":1498020080069,"isAutoCompleteSalePlan":1,"isNeedUserInfo":0,"isUseFirst":1}'
                # print post_body
                yield Request(url=url, method='POST', headers=header, body=post_body, callback=self.parse,
                              meta={'category_id':category_id,'category_name':category_name})

    def parse(self, response):
        item = BailingniaoOrderFieldItem()
        item['response_content'] = response.body
        item['category_id'] = response.meta['category_id']
        item['category_name'] = response.meta['category_name']
        yield item


    