# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from yuedongApp.items import YuedongappCityActItem
import web

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/58.0.3029.110 Safari/537.36'}
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class Yuedong_App_Cityact(scrapy.Spider):
    name = 'yuedong_app_cityact'

    def start_requests(self):
        data = db.query("select city_name, province_name from t_spider_App_yuedong_city")
        begin_cnt = 0
        end_cnt = 10
        url = 'https://circle.51yund.com/cityactivity/getActivityList'
        for item in data:
            post_data = {
                'user_id': '187586992',
                'oper_type': 'hot',
                'begin_cnt': str(begin_cnt),
                'end_cnt': str(end_cnt),
                'oper_city': item.city_name,
                'oper_fee': '',
                'sid': ''
            }
            yield scrapy.FormRequest(url, formdata=post_data, headers=headers, callback=self.jsonparse,
                                     dont_filter=True,
                                     meta={'begin_cnt': begin_cnt, 'end_cnt': end_cnt, 'province_name':
                                         item.province_name,
                                           'city_name': item.city_name, 'url': url})

    def jsonparse(self, response):
        content = json.loads(response.body)
        print content
        begin_cnt = response.meta['begin_cnt']
        end_cnt = response.meta['end_cnt']
        province_name = response.meta['province_name']
        city_name = response.meta['city_name']
        url = response.meta['url']
        act_list = content['arrInfo']
        if act_list:
            for act in act_list:
                items = YuedongappCityActItem()
                items['act_id'] = act['activity_id']
                items['act_name'] = act['title']
                items['address'] = act['address']
                items['begin_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(act['begin_time'])))
                items['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(act['end_time'])))
                items['province_name'] = province_name
                items['city_name'] = city_name

                yield items
            begin_cnt += 10
            end_cnt += 10
            post_data = {
                'user_id': '187586992',
                'oper_type': 'hot',
                'begin_cnt': str(begin_cnt),
                'end_cnt': str(end_cnt),
                'oper_city': city_name,
                'oper_fee': '',
                'sid': ''
            }
            yield scrapy.FormRequest(url, formdata=post_data, headers=headers, callback=self.jsonparse, dont_filter=True,
                                     meta={'begin_cnt': begin_cnt, 'end_cnt': end_cnt, 'province_name':
                                         province_name, 'city_name': city_name, 'url': url})
