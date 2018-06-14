# -*- coding: utf-8 -*-
import re
import time
import scrapy
import json
from scrapy import Request

# from PhysicalEducation.items import AiRuiItem

timeId = [54, 51]
# 艾瑞对应时间

ar_category = {'0': '月度独立设备数', '-2': '日均独立设备数', '-1': '月度总有效时长'}
def timeIds():
    stop_time = time.strftime('%m', time.localtime(time.time()))
    n_time = time.strftime('%Y', time.localtime(time.time()))
    # stop_time =3

    stop_time = int(stop_time)
    if stop_time <= 1:
        ar = 59
        return str(ar)
    else:
        ad = stop_time - 1
        ar = 59 + ad
        return str(ar)
print timeIds()

print timeIds()
class AiRuiSpider(scrapy.Spider):
    name = "airui"
    allowed_domains = ["iresearch.com.cn"]
    start_urls = ['http://index.iresearch.com.cn/app/GetDataList/?classId=93&'
                  'classLevel=2&timeId=36&orderBy=0&pageSize=undefined&pageIndex=1']

    def start_requests(self):
        for i in ['0', '-1', '-2']:
            url = 'http://index.iresearch.com.cn/app/GetDataList/?classId=93&' \
                  'classLevel=2&timeId=%s&orderBy=%s&pageSize=undefined&pageIndex=1' % (timeIds(),i)
            yield Request(url, callback=self.parse, meta={'no_data': 0, 'category_child': '体育资讯'},
                          dont_filter=True)
            url = 'http://index.iresearch.com.cn/app/GetDataList/?classId=28&' \
                  'classLevel=2&timeId=%s&orderBy=%s&pageSize=undefined&pageIndex=1' % (timeIds(),i)
            yield Request(url, callback=self.parse, meta={'no_data': 0, 'category_child': '健身运动'},
                          dont_filter=True)

    def parse(self, response):

        # item
        json_content = json.loads(response.body)
        # print json_content
        List = json_content.get('List')
        if List:
            response_content = json.loads(response.body)
            for i in response_content.get('List'):
                item = i
                item['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                category = ''.join(re.findall('orderBy=(.*?)&', response.url))
                print category
                print '--------------------------'
                item['category'] = ar_category[category]
                # item['url'] = response.url
                item['category_child'] = response.meta['category_child']
                print item['category_child']
                print '--------------------------'
                yield item
            if len(List) == 20:
                url = response.url
                pageIndex_list = str(url).split('&pageIndex=')
                if pageIndex_list:
                    pageIndex = pageIndex_list[1]
                    pageIndex = int(pageIndex) + 1
                    url = pageIndex_list[0] + '&pageIndex=%s' % pageIndex
                    meta = response.meta
                    meta['no_data'] = 0
                    yield Request(url, callback=self.parse, meta=meta, dont_filter=True)

        else:
            no_data = response.meta['no_data']
            if no_data < 3:
                no_data = int(no_data) + 1
                meta = response.meta
                meta['no_data'] = no_data
                yield Request(response.url, callback=self.parse, meta=meta, dont_filter=True)




    
    