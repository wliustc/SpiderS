# -*- coding: utf-8 -*-
import scrapy
import re
import json
from gudong_spider.items import GudongSpiderItem
import datetime


headers = {'User-Agent': 'CodoonSport(7.115.1 840;Android 6.0;Letv Letv X500'}


class Gudong_Spider(scrapy.Spider):

    name = 'gudong_spider'

    def start_requests(self):
        url = 'https://race.codoon.com/share/race/home'
        page = 1
        data = {'page': str(page), 'count': '20'}
        yield scrapy.FormRequest(url, formdata=data, headers=headers, callback=self.parseGame,
                                 meta={'page': page, 'url': url}, dont_filter=True)

    def parseGame(self, response):
        content = json.loads(response.body)
        items = GudongSpiderItem()
        item_list = content['data']['race_list']
        page = response.meta['page']
        url = response.meta['url']
        if item_list:
            for item in item_list:
                items['game_name'] = item['name']
                items['game_people_num'] = item['number']
                end_time = item['end_time']
                pattern = re.compile('(\d+)')
                time_list = re.findall(pattern, end_time)
                now = datetime.datetime.now()
                delta = datetime.timedelta(days=int(time_list[0]), hours=int(time_list[1]), minutes=int(time_list[2])+1)
                game_time = now + delta
                items['game_time'] = game_time.strftime("%Y-%m-%d %H:%M")

                yield items
            page += 1
            data = {'page': str(page), 'count': '20'}
            yield scrapy.FormRequest(url, formdata=data, headers=headers, callback=self.parseGame,
                                     meta={'page': page, 'url': url}, dont_filter=True)


    
    