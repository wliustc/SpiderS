# -*- utf-8 -*-
import scrapy
import re
from dongqiudi.items import DongqiudiItem
import json
import time

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/54.0.2840.98 Safari/537.36"}


class Dongqiudi_Spider(scrapy.Spider):
    name = 'dongqiudi_spider'
    start_urls = [
        'http://api.dongqiudi.com/leagues/groups/0',
        'http://api.dongqiudi.com/leagues/groups/26',
        'http://api.dongqiudi.com/leagues/groups/13',
        'http://api.dongqiudi.com/leagues/groups/28',
        'http://api.dongqiudi.com/leagues/groups/32',
        'http://api.dongqiudi.com/leagues/groups/6',
        'http://api.dongqiudi.com/leagues/groups/36',
        'http://api.dongqiudi.com/leagues/groups/11',
        'http://api.dongqiudi.com/leagues/groups/1',
        'http://api.dongqiudi.com/leagues/groups/3',
        'http://api.dongqiudi.com/leagues/groups/2',
        'http://api.dongqiudi.com/leagues/groups/4',
        'http://api.dongqiudi.com/leagues/groups/20',
        'http://api.dongqiudi.com/leagues/groups/10',
        'http://api.dongqiudi.com/leagues/groups/9',
        'http://api.dongqiudi.com/leagues/groups/8',
        'http://api.dongqiudi.com/leagues/groups/12',
        'http://api.dongqiudi.com/leagues/groups/18',
        'http://api.dongqiudi.com/leagues/groups/19',
        'http://api.dongqiudi.com/leagues/groups/14',
        'http://api.dongqiudi.com/leagues/groups/16',
        'http://api.dongqiudi.com/leagues/groups/0'
    ]

    def parse(self, response):
        content = json.loads(response.body)
        items = DongqiudiItem()
        items = {}
        for i in content:
            info_list = i.get('groups')
            if info_list:
                for info in info_list:
                    items['group_id'] = info['id']
                    items['group_name'] = info['title']
                    items['topic_total'] = info['topic_total']
                    items['join_user_total'] = info['join_user_total']
                    # items['group_created_date'] = info['created_at']['date']
                    items['browse_num'] = info['visits']
                    items['collect_time'] = time.strftime('%Y-%m-%d', time.localtime())

                    #print items
                    yield items

