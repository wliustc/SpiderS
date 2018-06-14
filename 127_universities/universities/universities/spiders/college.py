# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
import json, re
from scrapy import Request
from universities.items import UniversitiesItem


class CollegeSpider(scrapy.Spider):
    name = "college"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = ['http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?messtype=jsonp&callback=&size=50']

    def parse(self, response):
        data = response.body
        data = data[1:-2]
        # print data
        content_json = json.loads(data)
        school_list = content_json.get('school')
        if school_list:
            for school in school_list:
                school_id = school.get('schoolid')
                url = 'http://edu.people.gkcx.eol.cn/schoolhtm/schoolTemple/school%s.htm' % school_id
                yield Request(url, callback=self.parse_detail, meta={'school': school})
            if not response.meta.get('sign'):
                totalRecord = content_json.get('totalRecord')
                if totalRecord:
                    num = totalRecord.get('num')
                    page = int(num) / 50
                    for i in xrange(2, page + 2):
                        url = 'http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?messtype=jsonp&callback=&size=50&page=' + str(
                            i)
                        yield Request(url, callback=self.parse, meta={'sign': 1})

    def parse_detail(self, response):
        item = UniversitiesItem()
        item['school'] = response.meta['school']
        item['content'] = response.body
        jianjie = re.findall('href="(.*?)">学校简介</a>', response.body)
        if jianjie:
            jianjie_url = urljoin(response.url, jianjie[0])
            yield Request(jianjie_url, callback=self.parse_jianjie, meta={'item': item})
        else:
            yield item

    def parse_jianjie(self, response):
        item = response.meta['item']
        item['jianjie_content'] = response.body

        yield item
