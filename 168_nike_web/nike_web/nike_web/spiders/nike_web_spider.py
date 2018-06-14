# -*- ccoding: utf-8 -*-
import scrapy
import re
import json
from nike_web.items import NikeWebItem
import datetime
cate_list = ['男子-鞋类/7puZoi3', '男子-服装/1mdZ7pu', '女子-鞋类/7ptZoi3', '女子-Clothing/1mdZ7pt', '男孩/7pv', '女孩/7pw']


class Nike_Web_Spider(scrapy.Spider):

    name = 'nike_web_spider'

    def start_requests(self):
        for cate in cate_list:
            url = 'https://store.nike.com/html-services/gridwallData?country=CN&lang_locale=zh_CN&gridwallPath={}'.format(cate)
            cate_name = re.findall('(.*?)/', cate)[0]
            yield scrapy.Request(url, callback=self.parse_list, meta={'category': cate_name}, dont_filter=True)

    def parse_list(self, response):
        content = response.body
        cate_name = response.meta['category']
        json_con = json.loads(content)
        goods_list = json_con['sections'][0]['items']
        for info in goods_list:
            url = info['pdpUrl']
            yield scrapy.Request(url, callback=self.parse_detail, meta={'category': cate_name}, dont_filter=True)
        next_page = json_con['nextPageDataService']
        if next_page:
            next_url = 'https://store.nike.com' + next_page
            yield scrapy.Request(next_url, callback=self.parse_list, meta={'category': cate_name}, dont_filter=True)

    def parse_detail(self, response):
        content = response.body
        cate_name = response.meta['category']
        items = NikeWebItem()
        pattern = re.search('INITIAL_REDUX_STATE=([\s\S]*?);</script>', content)
        if pattern:
            json_con = json.loads(pattern.group(1))
            info_list = json_con['Threads']['products']
            for key in info_list:
                info = info_list[key]
                kuanhao = info['styleColor']
                color = info['colorDescription']
                title = info['title']
                subtitle = info['subTitle']
                price = info['currentPrice']
                employee_price = info['employeePrice']
                description = info['descriptionPreview']
                sub_category = info.get('category')
                size_list = info.get('skus')
                size = ''
                if size_list:
                    for i in size_list:
                        size = size + i['localizedSize'] + '|'
                items['url'] = response.url
                items['title'] = title
                items['subtitle'] = subtitle
                items['price'] = price
                items['color'] = color
                items['kuanhao'] = kuanhao
                items['description'] = description
                items['category'] = cate_name
                items['sub_category'] = sub_category
                items['size'] = size
                items['employee_price'] = employee_price
                items['dt'] = datetime.datetime.now().strftime('%Y-%m-%d')

                yield items
    
    