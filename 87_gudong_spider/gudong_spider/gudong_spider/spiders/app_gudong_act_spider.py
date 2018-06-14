# -*- coding: utf-8 -*-
import scrapy
import re
import json
from gudong_spider.items import GudongActSpiderItem

headers = {'User-Agent': 'CodoonSport(7.115.1 840;Android 6.0;Letv Letv X500'}


class Gudong_Act_Spider(scrapy.Spider):

    name = 'gudong_act_spider'

    def start_requests(self):
        url = 'https://www.codoon.com/activity/v1/api/event/list/init?cityCode=110000&longitude=0&latitude=0'
        yield scrapy.Request(url, headers=headers, callback=self.parseAct, dont_filter=True)

    def parseAct(self, response):
        content = json.loads(response.body)
        items = GudongActSpiderItem()
        item_list = content['data']
        for item in item_list:
            for act in item['eventLists']:
                items['act_name'] = act['title']
                items['act_heat'] = act['apply_count']
                items['act_starttime'] = act['start_time']
                items['act_endtime'] = act['end_time']

                yield items