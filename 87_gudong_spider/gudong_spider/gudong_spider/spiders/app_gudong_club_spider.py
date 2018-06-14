# -*- coding: utf-8-*-
import scrapy
import re
import json
from gudong_spider.items import GudongClubSpiderItem
import time

headers = {'User-Agent': 'CodoonSport(7.115.1 840;Android 6.0;Letv Letv X500'}


class Gudong_Club_Spider(scrapy.Spider):

    name = 'gudong_club_spider'

    def start_requests(self):
        url = 'http://club.codoon.com/get_club_industry_sort'
        yield scrapy.Request(url, headers=headers, callback=self.parseClub, dont_filter=True)

    def parseClub(self, response):
        content = json.loads(response.body)
        items = GudongClubSpiderItem()
        item_list = content['top_data_list']['club_rank']
        for item in item_list:
            items['club_name'] = item['club_name']
            items['club_rank'] = item['index']
            items['club_person_num'] = item['person_count']
            items['club_avg_steps'] = item['avg_steps']
            items['collect_time'] = time.strftime('%Y-%m-%d', time.localtime())

            yield items