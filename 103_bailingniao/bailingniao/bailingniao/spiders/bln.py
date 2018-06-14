# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import time
# from bailingniao.items import BailingniaoItem
# start_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
start_time = dt = int(time.time())

# print start_time
header = {
    'Tingyun-Process': 'true',
    'Content-Type': 'application/json;Charset=UTF-8',
    'Accept-Language': 'zh,zh-cn',
    'APPVersion': '2.0',
    'appChannel': 'v_1037',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Letv X500 Build/DBXCNOP5902605181S)',
    'Host': 'android.prod.quncaotech.com'
}


class BlnSpider(scrapy.Spider):
    name = "bln"
    allowed_domains = ["quncaotech.com"]

    # start_urls = ['http://quncaotech.com/']

    def start_requests(self):
        url = 'http://android.prod.quncaotech.com/api/club/system/cities/list'
        post_body = '{"ver":"2.8.1","protocol_ver":1,"platformType":2,"clientType":1}'
        yield Request(url=url, method='POST', headers=header, body=post_body, callback=self.parse)

    def parse(self, response):
        response_json = json.loads(response.body)
        data = response_json.get('data')
        if data:
            category = data.get('category')
            respCityInfoList = data.get('respCityInfo')
            if respCityInfoList:
                for respCityInfo in respCityInfoList:
                    respCity = respCityInfo.get('respCity')
                    respCity = respCity.get('id')
                    for category_id in category:
                        category_name = category_id.get('name')
                        category_id = category_id.get('id')
                        url = 'http://android.prod.quncaotech.com/api/place/placeSearch'
                        post_body = '{"ver":"2.7.9","protocol_ver":1,"platformType":2,' \
                                    '"cityId":' + str(respCity) + ',"sortType":1,"categoryId":' + str(
                            category_id) + ',"pageNum":0,' \
                                           '"pageSize":1000000,"searchType":2,"lat":0,"lng":0}'

                        yield Request(url, callback=self.parse_field, method='POST', headers=header, body=post_body,
                                      meta={'category_name': category_name})

    def parse_field(self, response):
        # item = BailingniaoItem()
        # item ={}

        line_json = json.loads(response.body)

        data = line_json.get('data')
        # response_content = json.loads(response_content)
        # data = response_content.get('data')

        if data:
            items = data.get('items')
            if items:
                for item in items:
                    result = {}
                    # print item
                    category = item.get('categorys')
                    category_result = []
                    for cate in category:
                        category_result.append(json.dumps(cate))

                    result['category'] = ';'.join(category_result)
                    result['addr'] = item.get('address')
                    result['name'] = item.get('name')
                    result['lat'] = item.get('lat')
                    result['lng'] = item.get('lat')
                    result['tel'] = item.get('phone')
                    result['cityname'] = item.get('cityObj').get('name')
                    result['field_id'] = item.get('id')
                    result['task_time'] = start_time

                    yield result

    