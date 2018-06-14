# -*- coding: utf-8 -*-
import scrapy
from hospital_project.items import HospitalProjectItem


class HealthSpider(scrapy.Spider):
    name = 'health'
    allowed_domains = ['yyk.99.com.cn']
    start_urls = ['http://yyk.99.com.cn/suixi/102481/',
                  'http://yyk.99.com.cn/changshu/76788/',
                  'http://yyk.99.com.cn/zhangjiagang/76838/',
                  'http://yyk.99.com.cn/duanzhou/111666/',
                  'http://yyk.99.com.cn/humen/119236/',
                  'http://yyk.99.com.cn/dongguan/111408/',
                  'http://yyk.99.com.cn/wuzhongqu/75969/',
                  'http://yyk.99.com.cn/suzhou/75996/',
                  'http://yyk.99.com.cn/daojiao/111627/',
                  'http://yyk.99.com.cn/nanchangqu/75589/',
                  'http://yyk.99.com.cn/szxxzdw/116455/',
                  'http://yyk.99.com.cn/szxxzdw/116694/',
                  'http://yyk.99.com.cn/szxxzdw/116904/',
                  'http://yyk.99.com.cn/hongdong/117486/',
                  'http://yyk.99.com.cn/kelan/73845/',
                  'http://yyk.99.com.cn/bama/101451/',
                  'http://yyk.99.com.cn/lingshan/114845/',
                  'http://yyk.99.com.cn/daan/100904/',
                  'http://yyk.99.com.cn/taonan/84649/',
                  'http://yyk.99.com.cn/wuhan/101512/',
                  'http://yyk.99.com.cn/xinghualing/73219/',
                  'http://yyk.99.com.cn/xiangyin/101245/',
                  'http://yyk.99.com.cn/yueyang/104206/',
                  'http://yyk.99.com.cn/wuhan/81541/',
                  'http://yyk.99.com.cn/cangwu/115470/',
                  'http://yyk.99.com.cn/cenxi/115520/',
                  'http://yyk.99.com.cn/cenxi/115525/',
                  'http://yyk.99.com.cn/jianghan/90254/',
                  'http://yyk.99.com.cn/jianghan/105048/',
                  'http://yyk.99.com.cn/ziyang/103181/',
                  'http://yyk.99.com.cn/szxxzdw/116828/',
                  'http://yyk.99.com.cn/shaoguan/113163/',
                  'http://yyk.99.com.cn/shixing/112846/',
                  'http://yyk.99.com.cn/qujiang/112792/',
                  'http://yyk.99.com.cn/shixing/112860/',
                  'http://yyk.99.com.cn/lianjiang/112183/',
                  'http://yyk.99.com.cn/kunshan/100962/',
                  ]

    def parse(self, response):
        item = HospitalProjectItem()
        count = response.xpath('//div[@class="w960"]/div/p/a').extract()
        count = len(count)
        if count == 3:
            # 所在省份
            item['hospital_province'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first()
            # 所在城市
            item['hospital_city'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first()            # 所在辖区
            item['hospital_county'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[3]/text()').extract_first().strip()
        elif count < 3:
            # 所在省份
            item['hospital_province'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first()
            # 所在城市
            item['hospital_city'] = None
            item['hospital_county'] = None

        else:
            item['hospital_province'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[2]/text()').extract_first().strip()
            item['hospital_city'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[3]/text()').extract_first().strip()
            item['hospital_county'] = response.xpath(
                '//div[@class="w960"]/div/p[@class="bnleft"]/a[4]/text()').extract_first().strip()
        # 医院名称
        item['hospital_name'] = response.xpath('/html/head/title/text()').extract_first().strip()
        # 医院别名
        item['hospital_alias'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[1]/span/text()').extract_first()
        # 医院等级
        item['hospital_grade'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[3]/span/text()').extract_first()
        # 地址
        hospital_addrs = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[5]/span/text()').extract_first()
        if hospital_addrs:
            item['hospital_addrs'] = hospital_addrs
        else:
            item['hospital_addrs'] = None
        # 电话
        item['hospital_phone'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[4]/span/@title').extract_first()
        # 经营方式
        item['business_practice'] = response.xpath(
            '//div[@class="mainleft"]/div[@class="border_wrap"]/div/div/ul/li[2]/text()').extract_first().strip()
        # 数据来源
        item['data_source'] = '99-健康网'
        print item
        yield item

