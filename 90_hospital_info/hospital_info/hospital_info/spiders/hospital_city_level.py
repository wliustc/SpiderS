# -*- coding: utf-8 -*-
import scrapy
import re
from hospital_info.items import HospitalCityLevelItem

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/54.0.2840.98 Safari/537.36"}


class Hospital_City_Level_Spider(scrapy.Spider):

    name = 'hospital_city_level_spider'

    def start_requests(self):
        url = 'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8'
        yield scrapy.Request(url, headers=headers, callback=self.list1parse, dont_filter=True)

    def list1parse(self, response):
        content = response.body
        pattern = re.compile('<p><b><a href="([\s\S]*?)<h3>')
        province_list = re.findall(pattern, content)
        for pro in province_list[0: 31]:
            pattern1 = re.compile('\">([\s\S]*?)医院列表<')
            province = re.findall(pattern1, pro)[0]
            print province
            # items['province'] = province
            pattern2 = re.compile('<a href="(.*?)" title="([\s\S]*?)医院列表">')
            city_list = re.findall(pattern2, pro)
            print city_list
            # raw_input("enter")
            for city in city_list[1:]:
                city_link = 'http://www.a-hospital.com' + city[0]
                city_name = city[1]
                # items['city'] = city_name

                yield scrapy.Request(city_link, headers=headers, callback=self.list2parse,
                                     meta={'province': province, 'city_name': city_name},
                                     dont_filter=True)

    def list2parse(self, response):
        items = HospitalCityLevelItem()
        content = response.body
        province = response.meta['province']
        city_name = response.meta['city_name']
        level_reg = re.search('按<a href="([\s\S]*?)</ul>', content)
        level_con = level_reg.group(1)
        pattern = re.compile('<li><a href="(.*?)" title="[\s\S]*?">([\s\S]*?)<')
        level_list = re.findall(pattern, level_con)
        for level in level_list:
            if 'redlink' in level[0]:
                continue
            level_link = 'http://www.a-hospital.com' + level[0]
            level_name = level[1]
            items['level_name'] = level_name
            items['city_level_url'] = level_link
            items['province'] = province
            items['city'] = city_name

            yield items

    # def infoparse(self, response):
    #     content = response.body
    #     items = HospitalInfoItem()
    #     province = response.meta['province']
    #     city_name = response.meta['city_name']
    #     level_name = response.meta['level_name']
    #     pattern = re.compile('<li><b><a href=([\s\S]*?)</ul>')
    #     info_list = re.findall(pattern, content)
    #     for info in info_list:
    #         name_reg = re.search('title="([\s\S]*?)"', info)
    #         items['hospital'] = name_reg.group(1)
    #         address_reg = re.search('医院地址<.*?>：([\s\S]*?)<', info)
    #         items['address'] = address_reg.group(1)
    #         tel_reg = re.search('联系电话<.*?>：([\s\S]*?)<', info)
    #         if tel_reg:
    #             items['tel_info'] = tel_reg.group(1)
    #         else:
    #             items['tel_info'] = 'null'
    #         type_reg = re.search('经营方式<.*?>：([\s\S]*?)<', info)
    #         if type_reg:
    #             items['type'] = type_reg.group(1)
    #         else:
    #             items['type'] = 'null'
    #         items['province'] = province
    #         items['city'] = city_name
    #         items['level_name'] = level_name
    #
    #         yield items