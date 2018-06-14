# -*- coding: utf-8 -*-
import scrapy
import re
from tmall_shop.items import TmallShopListItem
import time
headers = {
    ':authority': 'nike.tmall.com',
    'upgrade-insecure-requests': '1',
    'referer': 'https://nike.tmall.com/category.htm?pageNo=1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
cookie = {
    'cna': 'tTCaEWglogQCAd6Ab3yqeklX',
    'tk_trace': '1',
    '_tb_token_': 'eeb5abb51e6b0',
    'cookie2': '1ccd63be9facd40ecfea4e09fdd941b8',
    '_uab_collina': '151667578573912739772766',
    'cq': 'ccp%3D1',
    'uc1': 'cookie14',
    'uc3': 'nk2',
    'tracknick': '%5Cu6293%5Cu7D27%5Cu65F6%5Cu95F4%5Cu54271992',
    'lgc': '%5Cu6293%5Cu7D27%5Cu65F6%5Cu95F4%5Cu54271992',
    't': '5a33d90554f958d6150036e16c6844bd',
    'csg': 'a135a61e',
    'enc': 'kSUrSuiBbTkk0nB6%2Fwd8CbFQsu8nIDq1db076F1v3RQF2yej6BxR9Ou2e%2F1Tv2%2Bjwv091S6R%2FdTngNUqFZ%2BcVw%3D%3D',
    '_umdata': '65F7F3A2F63DF0204D4EB7FAA2B9787DAE9B9599281167EAAE0F830EE220037A9760BE682470E054CD43AD3E795C914C1FCC96CD80DB82A6DA023F4105E61376',
    'pnm_cku822': '',
    'isg': 'BAcHako0EVK6B5ZxibM3pLBUlr3bH9pdyXh-Hdn0Ixa9SCcK4dxrPkUJ7ggWoLNm'
}


class Nike_List_Spider(scrapy.Spider):

    name = 'nike_list_spider'

    def start_requests(self):
        page = 1
        url = 'https://nike.tmall.com/i/asynSearch.htm?callback=jsonp119&mid=w-14234872789-0&pageNo={}'.format(str(page))
        yield scrapy.Request(url, dont_filter=True, callback=self.list_parse, meta={'page': page}, headers=headers, cookies=cookie)

    def list_parse(self, response):
        content = response.body
        page = response.meta['page']
        # print content
        pattern = re.compile('</dd>\s{44}</dl>[\s\S]*?<dl[\s\S]*?data-id=\\\\"(\d+)\\\\">')
        id_list = re.findall(pattern, content)
        # print id_list
        if '__x5__' in content:
            url = 'https://nike.tmall.com/i/asynSearch.htm?callback=jsonp119&mid=w-14234872789-0&pageNo={}'.format(
                str(page))
            yield scrapy.Request(url, dont_filter=True, callback=self.list_parse, meta={'page': page}, headers=headers,
                                 cookies=cookie)
        else:
            if len(id_list) == 40:
                page += 1
                url = 'https://nike.tmall.com/i/asynSearch.htm?callback=jsonp119&mid=w-14234872789-0&pageNo={}'.format(
                    str(page))
                yield scrapy.Request(url, dont_filter=True, callback=self.list_parse, meta={'page': page}, headers=headers,
                                     cookies=cookie)
            for data in id_list:
                items = TmallShopListItem()
                items['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                items['nid'] = data
                items['user_id'] = '890482188'
                items['shop_name'] = 'NIKE官方旗舰店'
                yield items
