# -*- coding: utf-8 -*-
import scrapy
from re import sub
import time
import json
from yuedongApp.items import YuedongappGameItem

headers = {'User-Agent': 'SportsBar/3.3.8 (iPhone; iOS 10.3.1; Scale/2.00)'}


class yuedong_app_game(scrapy.Spider):
    name = 'yuedong_app_game_spider'

    def start_requests(self):
        url = 'https://api.51yund.com/challenge/get_online_group_info_client_v4'
        post_data = {
            'client_user_id': '177567644',
            'device_id': 'idfa_AAB972F2-BBA6-4CE6-96C5-F5B49F6382B0',
            'language': 'zh-Hans',
            'locale': 'CN',
            'offset': '0',
            'os': '10.3.1',
            'phone_type': 'iPhone6',
            'sign': 'gJjooA2EC5wjNwPKieLbDsbNoeI=',
            'source': 'ios',
            'timezone': '+8',
            'user_id': '177567644',
            'ver': '3.3.8',
            'xyy': 'o5qwxfsa61p4gthmbrg0',
        }

        yield scrapy.FormRequest(url, formdata=post_data, callback=self.jsonparse, dont_filter=True)

    def jsonparse(self, response):
        json_data = json.loads(response.body)
        items = YuedongappGameItem()
        print json_data
        type_list = json_data['infos']
        for typ in type_list:
            type_name = typ['title']
            game_list = typ['big_card_infos']
            if game_list:
                for game in game_list:
                    for per_game in game:
                        items['game_info'] = per_game['card_desc']
                        person_info = per_game['card_sub_desc']
                        items['person_num'] = sub('人参与', '', person_info)
                        items['begin_time'] = time.strftime('%Y-%m-%d', time.localtime(int(per_game['begin_time'])))
                        items['end_time'] = time.strftime('%Y-%m-%d', time.localtime(int(per_game['end_time'])))
                        items['game_type'] = type_name
                        items['game_id'] = per_game['group_run_id']

                        yield items