# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
from scrapy.http import HtmlResponse
import json
from yanke_haodaifu.haodaifu_link import haodaifu_links
from yanke_haodaifu.items import YankehaodaifuItem
class HaodaofulistSpider(scrapy.Spider):
    name = 'haodaofulist'
    allowed_domains = ["www.guahao.com"]
    def start_requests(self):
        rfile=haodaifu_links
        for line in rfile:
            url=line.strip()
            yield scrapy.Request(url,meta={'base_url':url[0:len(url)-1]})


    def parse(self, response):
        base_url=response.meta['base_url']
        tables=response.xpath('//*[@id="gray"]//tbody[1]//table')
        for table in tables:
            doctor_link=''.join(table.xpath('./tr[1]/td[2]/a[1]/@href').extract())
            yield scrapy.Request(doctor_link,callback=self.parse_detial,dont_filter=True)
        atags = response.xpath('//div[@class="p_bar"]//a')
        for a in atags:
            a_text=''.join(a.xpath('./text()').extract())
            if '共' in a_text.strip():
                page_num=int(re.sub('[^0-9]+','',a_text.strip()))+1
                for pageid in range(2,page_num+1):
                    url = "%s%s" % (base_url, pageid)
                    yield scrapy.Request(url,callback=self.parse_page_data,dont_filter=True)


    def parse_page_data(self, response):
        tables = response.xpath('//*[@id="gray"]//tbody[1]//table')
        for table in tables:
            doctor_link = ''.join(table.xpath('./tr[1]/td[2]/a[1]/@href').extract())
            item = {}
            item["doctor_link"] = doctor_link
            yield scrapy.Request(doctor_link, callback=self.parse_detial, dont_filter=True)

    def parse_detial(self, response):
        item=YankehaodaifuItem()
        script_str = (response.xpath('//script/text()').extract())
        for s in script_str:
            if 'BigPipe.onPageletArrive' in s:
                start = s.index('(') + 1
                end = s.rindex(')')
                s = s[start:end]
                json_obj = json.loads(s)

                id = json_obj["id"]
                if id == "bp_top":
                    content = json_obj['content']
                    response = HtmlResponse(url="my HTML string", body=content, encoding='utf-8')
                    nav = response.xpath('//div[@class="luj"]')[0]
                    province_name = ''.join(nav.xpath('./a[3]/text()').extract())
                    hospital_name = ''.join(nav.xpath('./a[4]/text()').extract())
                    room = ''.join(nav.xpath('./a[5]/text()').extract())
                    name = ''.join(nav.xpath('./a[6]/text()').extract())
                    item['province_name'] = province_name
                    item['hospital_name'] = hospital_name
                    item['room'] = room
                    item['name'] = name
                elif id == "bp_doctor_about":
                    content = json_obj['content']
                    response = HtmlResponse(url="my HTML string", body=content, encoding='utf-8')
                    middletr_table = response.xpath('//div[@class="middletr"]/div[1]/table[1]')
                    trs = middletr_table.xpath('./tr')
                    technical_title = ''
                    for tr in trs:
                        test_technical_title = ''.join(''.join(tr.xpath('./td[2]/text()').extract()).split())
                        if '职称' in test_technical_title:
                            technical_title = ''.join(tr.xpath('./td[3]/text()').extract())
                    proffession = ''.join(
                        response.xpath('.//div[@id="full_DoctorSpecialize"]/text()').extract()).strip()
                    summary = ''.join(response.xpath('.//div[@id="full"]/text()').extract()).strip()
                    comment_bar = response.xpath('//div[@class="r-p-part clearfix"]')[0]
                    comment_grade = ''.join(comment_bar.xpath('.//p[@class="r-p-l-score"]/text()').extract())
                    extr_infos = comment_bar.xpath('./div[@class="fl score-part"]//span/text()')

                    for extr_info in extr_infos:
                        fields = ''.join(extr_info.extract()).split("：")
                        k = fields[0]
                        v = fields[1]
                    item['summary'] = summary
                    item['comment_grade'] = ''.join(comment_grade.split())
                    item['technical_title'] = technical_title
                    item['proffession'] = proffession
                    yield item

    
    
    