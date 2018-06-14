# -*- encoding:utf-8 -*-
import scrapy
import re
import json

get_price_url = """http://pas.suning.com/nsitemsale_{}_0000000000_100_025_0250101_0_2__6.html"""
get_detail_url = """http://product.m.suning.com/pds-web/ajax/itemParaJsonp_000000000{}_R1901001_10051_itemParameter.html?callback=itemParameter"""
get_itemlist_url = """http://search.suning.com/emall/mobile/clientSearch.jsonp?cf=&channelId=MOBILE&ci={}&cityId=9173&cp=0&ct=-1&istongma=1&iv=-1&operate=0&ps=40&sc=&set=5&st=0&v=1.3"""
_mapping = {'next_page': re.compile(r'cp=(\d+)'),
            'cate_id': re.compile(r'ci=(\d+)')}


class SuningSpider(scrapy.Spider):
    name = "suning_goods"
    allowed_domains = ["suning.com"]

    def __init__(self, categoryId, task_date, *args, **kwargs):
        super(SuningSpider, self).__init__(*args, **kwargs)
        cate_ids = categoryId.split(",")
        self.start_urls = []
        for ct_id in cate_ids:
            itemlist_url = get_itemlist_url.format(ct_id)
            self.start_urls.append(itemlist_url)
        self.task_date = task_date

    def parse(self, response):
        if self.is_access_controled(response):
            self.logger.warning(response.body)
            self.logger.warning("I'm fucking controlled!" + response.url)

        json_obj = None
        try:
            json_obj = json.loads(response.body)
        except:
            self.logger.warning("response body is not json")
            self.logger.warning(response.body)

        if json_obj and json_obj.has_key("goods"):
            goods = json_obj["goods"]

            for item in goods:
                price_url = get_price_url.format(item['catentryId'])
                item['task_date'] = self.task_date
                item['categoryId'] = get_regex_group1('cate_id', response.url)
                yield scrapy.Request(price_url, meta={'item': item, 'retry': 0}, callback=self.parse_price_item,
                                     dont_filter=True)

            if len(goods) > 0:
                next_data_value = int(get_regex_group1('next_page', response.url)) + 1
                next_url = re.sub('cp=\d+', 'cp={}'.format(next_data_value), response.url)
                if next_data_value <= 2:
                    yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_price_item(self, response):
        retry = response.meta['retry']
        if self.is_access_controled(response):
            self.logger.warning(response.body)
            self.logger.warning("I'm fucking controlled! retry %s times" % retry + response.url)
            if retry < 3:
                retry += 1
                item = response.meta['item']
                yield scrapy.Request(response.url, meta={'item': item, 'retry': retry}, callback=self.parse_price_item,
                                     dont_filter=True)
        json_obj = None
        try:
            json_obj = json.loads(response.body)
        except:
            self.logger.warning("response body is not json")
            self.logger.warning(response.body)
            if retry < 3:
                retry += 1
                yield scrapy.Request(response.url, meta={'retry': retry}, callback=self.parse_price_item,
                                     dont_filter=True)
        item = response.meta['item']
        if json_obj:
            item['priceDetail'] = json_obj
            detail_url = get_detail_url.format(item['catentryId'])
            yield scrapy.Request(detail_url, meta={'item': item, 'retry': 0}, callback=self.parse_item_detail,
                                 dont_filter=True)

    def parse_item_detail(self, response):
        retry = response.meta['retry']
        if self.is_access_controled(response):
            self.logger.warning(response.body)
            print("I'm fucking controlled! retry %s times" % retry + response.url)
            if retry < 3:
                item = response.meta['item']
                retry += 1
                yield scrapy.Request(response.url, meta={'item': item, 'retry': retry}, callback=self.parse_item_detail,
                                     dont_filter=True)
        json_str = response.body
        json_str = json_str[:-1]
        json_str = json_str.replace('itemParameter(', '')
        json_obj = None
        try:
            json_obj = json.loads(json_str)
        except:
            self.logger.warning("response body is not json")
            self.logger.warning(json_str)
            if retry < 3:
                retry += 1
                item = response.meta['item']
                yield scrapy.Request(response.url, meta={'item': item, 'retry': retry}, callback=self.parse_item_detail,
                                     dont_filter=True)
            else:
                yield {}
        item = response.meta['item']
        item['detail'] = json_obj
        yield {'content': item}

    def is_access_controled(self, response):
        if response.status >= 400:
            return True
        expect_list = ['pas.suning.com', 'product.m.suning.com', 'search.suning.com']
        for el in expect_list:
            if el in response.url:
                return False
        if 'passport.suning.com' in response.body or 'passport.m.suning.com' in response.body:
            return True
        return True


def get_regex_group1(key, _str, default=None):
    p = _mapping[key]
    m = p.search(_str)
    if m:
        return m.group(1)
    return default
