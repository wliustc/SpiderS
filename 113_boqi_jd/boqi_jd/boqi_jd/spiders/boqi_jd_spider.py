# -*- coding: utf-8 -*-
import scrapy
import re
import time
from boqi_jd.items import BoqiJdItem

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/59.0.3071.115 Safari/537.36'
}


class Boqi_jd_Spider(scrapy.Spider):

    name = 'boqi_jd_spider'

    def start_requests(self):
        url = 'https://mall.jd.com/index-31231.html#'
        yield scrapy.Request(url, headers=headers, callback=self.category_parse, dont_filter=True)

    def category_parse(self, response):
        content = response.body
        pattern = re.compile('<dl class="sub-pannel">([\s\S]*?)</dl>')
        cate_con = re.findall(pattern, content)
        for con in cate_con:
            pattern1 = re.search('class="sub-tit-link">([\s\S]*?)<', con)
            category1_name = pattern1.group(1)
            pattern2 = re.compile('<li class="leaf">[\s\S]*?<a href="(.*?)".*?">(.*?)<')
            cate2_con = re.findall(pattern2, con)
            for con2 in cate2_con:
                page_num = '1'
                # url = 'https' + con2[0]
                pattern2_1 = re.search('90555-(\d+?)-', con2[0])
                cate2_id = pattern2_1.group(1)
                category2_name = con2[1]
                url = 'https://module-jshop.jd.com/module/getModuleHtml.html?appId=90555&orderBy=99&pageNo=%s' \
                      '&direction=1&categoryId=%s&pageSize=24&pageInstanceId=2910564&moduleInstanceId=3' \
                      '9635644&prototypeId=75&templateId=414060&layoutInstanceId=39635644&origin=0&shopId=31231&' \
                      'venderId=32359&callback=jshop_module_render_callback&_=1501662787296' % (page_num, cate2_id)
                yield scrapy.Request(url, headers=headers, callback=self.list_parse,
                                     meta={'category1_name': category1_name, 'category2_name': category2_name,
                                           'page_num': page_num, 'cate2_id': cate2_id},
                                     dont_filter=True)

    def list_parse(self, response):
        content = response.body
        page_num = response.meta['page_num']
        cate2_id = response.meta['cate2_id']
        category1_name = response.meta['category1_name']
        category2_name = response.meta['category2_name']
        pattern = re.compile('data-id=\\\\"(\d+?)\\\\"')
        id_list = re.findall(pattern, content)
        for goods_id in id_list:
            url = 'https://item.jd.com/%s.html' % goods_id
            pattern1 = re.search('<.*?'+goods_id+'.*?>已有<em>(\d+)<', content)
            comment_num = pattern1.group(1)
            yield scrapy.Request(url, headers=headers, callback=self.detail_parse, meta=
            {'category1_name': category1_name, 'category2_name': category2_name, 'goods_id': goods_id, 'comment_num':
             comment_num},
                                 dont_filter=True)
        if '<span>下一页</span>' not in content:
            page_num = str(int(page_num)+1)
            url = 'https://module-jshop.jd.com/module/getModuleHtml.html?appId=90555&orderBy=99&pageNo=%s' \
                  '&direction=1&categoryId=%s&pageSize=24&pageInstanceId=2910564&moduleInstanceId=3' \
                  '9635644&prototypeId=75&templateId=414060&layoutInstanceId=39635644&origin=0&shopId=31231&' \
                  'venderId=32359&callback=jshop_module_render_callback&_=1501662787296' % (page_num, cate2_id)
            yield scrapy.Request(url, headers=headers, callback=self.list_parse,
                                 meta={'category1_name': category1_name, 'category2_name': category2_name,
                                       'page_num': page_num, 'cate2_id': cate2_id},
                                 dont_filter=True)

    def detail_parse(self, response):
        content = str(response.body).decode('gb18030').encode('utf-8')
        category1_name = response.meta['category1_name']
        category2_name = response.meta['category2_name']
        goods_id = response.meta['goods_id']
        comment_num = response.meta['comment_num']
        pattern1 = re.search('品牌： <[\s\S]*?>([\s\S]*?)<', content)
        brand = ''
        if pattern1:
            brand = pattern1.group(1)
        url = 'https://p.3.cn/prices/mgets?type=1&area=1&pdtk=&pduid=' \
              '1067890109&pdpin=&pin=null&pdbp=0&skuIds=J_%s&ext=11000000&source=item-pc' % goods_id
        yield scrapy.Request(url, headers=headers, callback=self.price_parse, meta=
        {'category1_name': category1_name, 'category2_name': category2_name, 'goods_id': goods_id, 'comment_num':
            comment_num, 'brand': brand}, dont_filter=True)

    def price_parse(self, response):
        content = response.body
        items = BoqiJdItem()
        category1_name = response.meta['category1_name']
        category2_name = response.meta['category2_name']
        goods_id = response.meta['goods_id']
        comment_num = response.meta['comment_num']
        brand = response.meta['brand']
        pattern = re.search('"op":"(.*?)"', content)
        price = pattern.group(1)
        items['category1_name'] = category1_name
        items['category2_name'] = category2_name
        items['goods_id'] = goods_id
        items['comment_num'] = comment_num
        items['brand'] = brand
        items['price'] = price
        items['collect_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        yield items
    