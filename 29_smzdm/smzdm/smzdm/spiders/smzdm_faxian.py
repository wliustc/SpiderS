# -*- coding: utf-8 -*-
import scrapy
import re
import json

from smzdm.items import *

_mapping = {
        'offset' : re.compile(r'[&?]offset=(\d+)'),
        'article_id' : re.compile(r'article_id=(\d+)'),
        'limit' : re.compile(r'limit=(\d+)')
        }

def get_regex_group1(key,_str, default=None):

    p = _mapping[key]
    m = p.search(_str)
    if m:
        return m.group(1)
    return default


def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj


def load_json(response, logger):
    json_obj = json.loads(response.body)
    if not json_obj:
        logger.warning('Not a proper response for "{}":\n{}'.format(response.url, response.body))
        return None

    if json_obj['error_msg'] not in ("", "data"):
        logger.warning('No data for "{}":\n{}'.format(response.url, response.body))
        return None

    return json_obj


list_url_template = 'http://api.smzdm.com/v1/faxian/articles?imgmode=0&limit={}&offset={}'
page_limit = 50
item_url_template = 'http://api.smzdm.com/v2/youhui/articles/{}?channel_id=2&filtervideo=1&imgmode=0&show_dingyue=1&show_wiki=1'
comment_url_template = 'http://api.smzdm.com/v1/comments?article_id={}&atta=0&cate=new&get_total=1&ishot=1&limit=20&offset={}&type=faxian'


def get_urls_from_items(items_list):
    return [item_url_template.format(item['article_id']) for item in items_list]

def get_comment_urls_from_items(items_list):
    return [comment_url_template.format(item['article_id'],0) for item in items_list]

def get_next_comment_url(url, total_page):
    total_page = int(total_page)

    cur_offset = int(get_regex_group1('offset', url))
    limit = int(get_regex_group1('limit', url))
    article_id = get_regex_group1('article_id', url)

    urls = []
    for i in range(cur_offset + limit, total_page, limit):
        urls.append(comment_url_template.format(article_id, i))

    return urls


class SmzdmFaxianSpider(scrapy.Spider):
    name = "smzdm_faxian"
    #allowed_domains = ["faxian.smzdm.com"]
    start_urls = (
            list_url_template.format(page_limit, 0),
    )

    def parse(self, response):
        items_list = self._parse_list_items(response)
        for item in items_list:
            yield item

        if items_list:
            cur_offset = int(get_regex_group1('offset', response.url))
            yield scrapy.Request(list_url_template.format(page_limit, cur_offset + page_limit), callback=self.parse)

        for item_url in get_urls_from_items(items_list):
            yield scrapy.Request(item_url, callback=self.parse_item)

        for comment_url in get_comment_urls_from_items(items_list):
            yield scrapy.Request(comment_url, callback=self.parse_comment)
    

    def _parse_list_items(self, response):
        items_list = []
        json_obj = load_json(response, self.logger)
        if not json_obj:
            return items_list
        data_rows = get_json_hierarchy(json_obj, ['data','rows'])
        for row in data_rows:
            item = SmzdmListItem()
            for k, v in row.items():
                item[k.lower()] = v
            items_list.append(item)

        return items_list

    def parse_item(self, response):
        item = self._parse_item(response)
        if item:
            yield item
        
    def _parse_item(self, response):
        json_obj = load_json(response, self.logger)
        if not json_obj:
            return None

        data = get_json_hierarchy(json_obj, ['data',])
        item = SmzdmSingleItem()
        for k, v in data.items():
            item[k.lower()] = v
        return item

    def parse_comment(self, response):
        comment_list, total_pages = self._parse_comment(response)
        for comment in comment_list:
            yield comment
            
        for next_url in get_next_comment_url(response.url, total_pages):
            yield scrapy.Request(next_url, callback=self.parse_comment)
            

    def _parse_comment(self, response):
        comment_list = []
        json_obj = load_json(response, self.logger)
        if not json_obj:
            return comment_list, 0

        article_id = get_regex_group1('article_id', response.url)
        data_rows = get_json_hierarchy(json_obj, ['data','rows'])
        for row in data_rows:
            item = SmzdmCommentItem()
            item['article_id'] = article_id
            for k, v in row.items():
                item[k.lower()] = v
            comment_list.append(item)
        return comment_list, int(get_json_hierarchy(json_obj, ['data', 'total']))

