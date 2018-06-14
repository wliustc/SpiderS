# -*- coding: utf-8 -*-
from ..items import BoosDirectHireItem
import scrapy
from scrapy.selector import Selector
import re
from ..date_time import time_zh
import time
class BoosSpider(scrapy.Spider):
    name = "Boos"
    allowed_domains = ["zhipin.com"]


    def __init__(self, *args, **kwargs):  # 继承并初始化函数
        super(BoosSpider, self).__init__(*args, **kwargs)  # 继承类
        self.gongsi_recruitment_url = 'https://www.zhipin.com/gongsi/{}'
        self.gongsi_type = 'https://www.zhipin.com/gongsi/{}?page=100&ka=page-100'
        self.page_url = 'http://www.zhipin.com{}?page={}'
        self.position_url = 'http://www.zhipin.com{}'
        self.a ='https://www.zhipin.com{}?page=100&ka=page-100'
        self.start_urls = []


    def start_requests(self):
        gongsi_list = ['r115845.html', 'r34832.html', 'r127537.html',
                       'r109238.html', 'r222553.html', 'r85429.html',
                       'r462311.html', 'r407272.html', 'r280622.html',
                       'r177117.html', 'r478903.html']
        for uuid in gongsi_list:
            url = self.gongsi_recruitment_url.format(uuid)
            yield scrapy.Request(url, dont_filter=True, meta={'url': url})


    def parse(self, response):
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.parse, meta=response.meta, dont_filter=True)
        else:
            html = response.body
            position_type = Selector(text=html).xpath('//*[@class="inner job-category"]/a/text()').extract()
            position_href = Selector(text=html).xpath('//*[@class="inner job-category"]/a/@href').extract()
            for i in zip(position_href[1:], position_type[1:]):
                url = self.a.format(i[0])
                uid = i[0]
                yield scrapy.Request(url, dont_filter=True, callback=self.type_html, meta={'type': i[1], 'uid': uid, 'url': url} )


    def type_html(self, response):
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.type_html, meta=response.meta, dont_filter=True)
        else:
            classes = response.meta['type']
            html = response.body
            gather_data = Selector(text=html).xpath('//*[@class="job-list"]/div[@class="page"]/a/text()').extract()
            if len(gather_data) != 0:
                for page in range(int(gather_data[0]), int(gather_data[-1])+1):
                    url = self.page_url.format(response.meta['uid'], page)
                    yield scrapy.Request(url, dont_filter=True, callback=self.page_xml, meta={'classes': classes, 'url': url})
            else:
                position_uid = Selector(text=html).xpath('//*[@class="job-list"]/ul/li/a/@href').extract()
                for uid in position_uid:
                    url = self.position_url.format(uid)
                    yield scrapy.Request(url, dont_filter=True, callback=self.position, meta={'classes': classes, 'url': url})


    def page_xml(self, response):
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.page_xml, meta=response.meta, dont_filter=True)
        else:
            classes = response.meta['classes']
            html = response.body
            position_uid = Selector(text=html).xpath('//*[@class="job-list"]/ul/li/a/@href').extract()
            for uid in position_uid:
                url = self.position_url.format(uid)
                yield scrapy.Request(url, dont_filter=True, callback=self.position, meta={'classes': classes, 'url': url})


    def position(self, response):
        if response.status != 200:
            yield scrapy.Request(response.meta['url'], callback=self.position, meta=response.meta, dont_filter=True)
        else:
            # url = response.url
            item = BoosDirectHireItem()
            html = response.body
            #职位类型
            Job_type = response.meta['classes']
            Job_type = re.sub(r'(\d)', '', Job_type)[0:-2]
            #职位
            Job_title = ''.join(Selector(text=html).xpath('//*[@class="job-primary"]//div[@class="name"]/text()').extract())
            if len(Job_title) == 0:
                yield scrapy.Request(response.meta['url'], callback=self.position, meta=response.meta, dont_filter=True)
            else:
                #发布时间
                release_time = ''.join(Selector(text=html).xpath('//*[@class="job-primary"]//span[@class="time"]/text()').extract())
                release_time = time_zh(release_time)
                #薪资
                salary = ''.join(Selector(text=html).xpath('//*[@class="job-primary"]//span[@class="badge"]/text()').extract())
                #地点/经验/学历
                information = Selector(text=html).xpath('//*[@class="job-primary"]/div[@class="info-primary"]/p/text()').extract()
                if len(information) != 0:
                    recruiting_city = information[0]
                    experience = information[1]
                    learn = information[2]
                else:
                    recruiting_city, experience, learn = '', '', ''
                #职位关键字
                keyword = ','.join(Selector(text=html).xpath('//*[@class="job-primary"]/div[@class="info-primary"]/div[@class="job-tags"]/span/text()').extract())
                #职位描述
                describe = Selector(text=html).xpath('//*[@class="job-sec"]/div[@class="text"]/text()').extract()
                Job_describe = ','.join(describe).replace('\t', '').replace('\n', '').replace(' ', '')
                #公司名称
                company = ''.join(Selector(text=html).xpath('*//a[@ka="job-detail-company"]/text()').extract())
                re_keyword = Job_title, keyword, Job_describe
                re_keyword = re.findall(u'数据分析|量化策略|大数据|机器学习',''.join(re_keyword))
                if len(re_keyword) != 0:
                    if len(re_keyword) != 1:
                        for i in re_keyword:
                            if i == i:
                                re_keyword.remove(i)
                        keyword = ','.join(re_keyword)
                    else:
                        keyword = ''.join(re_keyword)
                item['company'] = company
                item['Job_title'] = Job_title
                item['Job_type'] = Job_type
                item['Job_describe'] = Job_describe
                item['keyword'] = keyword
                item['recruiting_city'] = recruiting_city
                item['payment'] = salary
                item['learn'] = learn
                item['experience'] = experience
                item['source'] = 'Boos直聘'
                item['release_time'] = release_time
                item['task_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item


    