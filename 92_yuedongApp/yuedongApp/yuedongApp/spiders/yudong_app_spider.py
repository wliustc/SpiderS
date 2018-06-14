# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from yuedongApp.items import YuedongappItem
import traceback

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/58.0.3029.110 Safari/537.36'}


class Yuedong_App_Spider(scrapy.Spider):

    name = 'yuedong_app_spider'

    def start_requests(self):
        url = 'https://sslsharecircle.51yund.com/discover/getHotTopic'
        begin_cnt = 0
        end_cnt = 10
        for num in range(0, 3):
            post_data = {'user_id': '0', 'begin_cnt': str(begin_cnt), 'end_cnt': str(end_cnt), 'hot_type': str(num),
                         'sid': 'null'}
            yield scrapy.FormRequest(url, headers=headers, formdata=post_data, callback=self.jsonparse,
                                     meta={'begin_cnt': begin_cnt, 'end_cnt': end_cnt}, dont_filter=True)

    def jsonparse(self, response):
        try:
            json_data = json.loads(response.body)
            info_list = json_data['arrInfo']
            items = YuedongappItem()
            begin_cnt = response.meta['begin_cnt']
            end_cnt = response.meta['end_cnt']
            if info_list:
                for info in info_list:
                    items['topic_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['add_time']))
                    items['topic_content'] = info['content']
                    items['comment_num'] = info['discuss_cnt']
                    items['browse_num'] = info['read_cnt']
                    items['topic_id'] = info['topic_id']
                    items['like_num'] = info['like_cnt']
                    items['collect_time'] = time.strftime('%Y-%m-%d', time.localtime())

                    yield items
                begin_cnt += 10
                end_cnt += 10
                url = 'https://sslsharecircle.51yund.com/discover/getHotTopic'
                post_data = {'user_id': '0', 'begin_cnt': str(begin_cnt), 'end_cnt': str(end_cnt), 'hot_type': '0',
                             'sid': 'null'}
                yield scrapy.FormRequest(url, headers=headers, formdata=post_data, callback=self.jsonparse,
                                         meta={'begin_cnt': begin_cnt, 'end_cnt': end_cnt}, dont_filter=True)

        except Exception, e:
            traceback.print_exc()
