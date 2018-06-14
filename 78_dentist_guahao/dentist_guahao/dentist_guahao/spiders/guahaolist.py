# -*- coding: utf-8 -*-

import math
import scrapy
import json
from dentist_guahao.items import YankeguahaoItem
from dentist_guahao.guahao_json_obj import json_obj


def get_city_code():
    resultList = []
    provinces = json_obj['provinces']
    for province in provinces:
        citys = []
        try:
            citys = province['cities']
        except:
            pass
        if len(citys) > 0:
            for city in citys:
                item = {}
                item['province_name'] = province['areaName']
                item['province_id'] = province['areaId']
                item['city_id'] = city['areaId']
                item['city_name'] = city['areaName']
                resultList.append(item)
        else:
            item = {}
            item['province_name'] = province['areaName']
            item['province_id'] = province['areaId']
            resultList.append(item)
    return resultList


class BaiduDoctorHospital(scrapy.Spider):
    name = 'guahao_doctor'

    def start_requests(self):
        city_list=get_city_code()
        for city_item in city_list:
            province_name=city_item['province_name']
            province_id = int(city_item['province_id'])
            city_name = city_item.get('city_name',None)
            city_id = int(city_item.get('city_id',None))
            if city_id is not None:
                #&pageNo=1
                base_url = 'https://www.guahao.com/search/expert?dt=&phone=&sort=haoyuan&ht=all&diagnosis=&hk=&hospitalId=&hl=all&imagetext=&activityId=&weightActivity=&fhc=&standardDepartmentId=&hydate=all&fg=&ipIsShanghai=false&mf=true&iSq=&consult=&c=%s&dty=&volunteerDoctor=&o=all&searchAll=Y&q=眼科&p=%s&ci=%s&es=all&pi=%s&hdi=' % (
                city_name, province_name, city_id, province_id)
                url='%s&pageNo=1' %(base_url)
                yield scrapy.Request(url,meta={'province_name':province_name,'province_id':province_id,'city_name':city_name,'city_id':city_id,'base_url':base_url},dont_filter=True)
            else:
                base_url = 'https://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=眼科&pi=%s&p=%s&ci=all&c=不限&o=all&es=all&hl=all&ht=all&hk=&dt=&dty=&hdi=&mf=true&fg=0&ipIsShanghai=false&searchAll=Y&hospitalId=&standardDepartmentId=&consult=&volunteerDoctor=&imagetext=&phone=&diagnosis=&sort=haoyuan&hydate=all&activityId=&weightActivity=' % (
                province_id, province_name)
                url = '%s&pageNo=1' % (base_url)
                yield scrapy.Request(url, meta={'province_name': province_name, 'province_id': province_id,'city_name': province_name, 'city_id': province_id,'base_url':base_url},dont_filter=True)


    def parse(self, response):
        base_url=response.meta['base_url']
        province_name=response.meta['province_name']
        city_name = response.meta['city_name']
        if ('retry' in response.meta.keys()) and response.meta['retry'] < 0:
            return
        else:
            doctor_items = response.xpath('//*[@id="g-cfg"]/div[1]/div[3]/ul/li')
            for doctor in doctor_items:
                item={}
                link=doctor.xpath('./div[2]/a/@href')[0].extract()
                item['province_name']=province_name
                item['city_name']=city_name
                item['link']=link
                yield scrapy.Request(link,meta=response.meta,callback=self.parse_getdetial,dont_filter=True)
            # 根据count 提取，生成分页url
            total_result_str=response.xpath('//*[@id="J_ResultNum"]/text()').extract()
            total_result=int(total_result_str[0])
            page_num = int(math.ceil(float(total_result) / 16))
            for i in range(2, page_num + 1):
                url="%s&pageNo=%s" %(base_url,i)
                yield scrapy.Request(url,meta=response.meta,callback=self.parse_page_data,dont_filter=True)
    def parse_page_data(self, response):
        province_name=response.meta['province_name']
        city_name = response.meta['city_name']
        doctor_items = response.xpath('//*[@id="g-cfg"]/div[1]/div[3]/ul/li')
        for doctor in doctor_items:
            link=doctor.xpath('./div[2]/a/@href')[0].extract()
            yield scrapy.Request(link,callback=self.parse_getdetial,dont_filter=True)

    def parse_getdetial(self, response):
        item = YankeguahaoItem()
        base_info=response.xpath('//*[@id="g-cfg"]/div[1]/section/div[1]')
        name=base_info.xpath('./div[2]/h1/strong/text()')[0].extract()
        technical_title=''.join(base_info.xpath('./div[2]/h1/span/text()').extract())
        specil_skill=''.join(base_info.xpath('./div[2]/div[3]/span/text()').extract())
        summary=''.join(base_info.xpath('./div[2]/div[4]/a/@data-description').extract())
        mark_count=''.join(base_info.xpath('./div[1]/p[2]/span/text()').extract())
        comment_count=''.join(response.xpath('//*[@id="g-cfg"]/div[2]/div/div/section[4]/div[1]/div/a/strong/text()').extract())
        hospitals=response.xpath('//*[@id="card-hospital"]/div/p')
        hospital_infos={}
        for hospital in hospitals:
            hospital_name=''.join(hospital.xpath('./a[1]/@title').extract())
            hospital_link=''.join(hospital.xpath('./a[1]/@href').extract())
            hospital_infos[hospital_name]=hospital_link

        comment_grade=''.join(response.xpath('//*[@id="expert-rate"]/a/strong/text()').extract())
        bespeak=''.join(response.xpath('//*[@id="g-cfg"]/div[1]/section/div[2]/div[2]/div[2]/strong[1]/text()').extract())
        action_count=''.join(response.xpath('//*[@id="g-cfg"]/div[1]/section/div[2]/div[2]/div[2]/strong[2]/text()').extract())
        item['name']=name
        item['technical_title'] =technical_title
        item['specil_skill'] =specil_skill
        item['mark_count'] =mark_count
        item['comment_grade'] =comment_grade
        item['bespeak'] =bespeak
        item['action_count'] =action_count
        item['comment_count'] =comment_count
        item['summary'] =summary
        item['hospital_info']=hospital_infos
        yield item
    
    
    
    
    
    