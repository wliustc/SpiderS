# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaiduApiPipeline(object):
    def process_item(self, item, spider):
        id = scrapy.Field()
        data_id = scrapy.Field()
        legalpersonid = scrapy.Field()
        name = scrapy.Field()
        reginstitute = scrapy.Field()
        reglocation = scrapy.Field()
        companyorgtype = scrapy.Field()
        legalpersonname = scrapy.Field()
        regstatus = scrapy.Field()
        company_name = scrapy.Field()
        businessscope = scrapy.Field()
        industry = scrapy.Field()
        baidu_addr = scrapy.Field()
        city = scrapy.Field()
        district = scrapy.Field()
        province = scrapy.Field()
        street = scrapy.Field()
        poi_desc = scrapy.Field()
        lng = scrapy.Field()
        lat = scrapy.Field()
        mc_lng = scrapy.Field()
        mc_lat =scrapy.Field()
        catalog = scrapy.Field()
        return item

    