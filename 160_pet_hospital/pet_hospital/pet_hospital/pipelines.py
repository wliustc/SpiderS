# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import spiders.db
import datetime
import time

class PetHospitalPipeline(object):
    def __init__(self, dbArgs, table_all, table_source, table_click):
        self.dbArgs = dbArgs
        self.table_all = table_all
        self.table_source = table_source
        self.table_click = table_click
        self.task_date = datetime.date.today().strftime("%Y-%m-%d")
        self.file_path = "./data/"

    @classmethod
    def from_crawler(cls, crawler):
        dbArgs = dict(
            host='10.15.1.14',
            database='hillinsight',
            user='work',
            password='phkAmwrF',
            charset='utf8',
        )
        return cls(
            dbArgs,
            table_all = 't_app_pet_hospital_traffic_data',
            table_source = 't_app_pet_hospital_traffic_data_source',
            table_click = 't_app_pet_hospital_merchantpage_click_info'
        )

    def open_spider(self, spider):
        spiders.db.create_engine(**self.dbArgs)
        pass

    def close_spider(self, spider):
        pass
    def process_item(self, item, spider):
        if 'loss_num' in item:

            spiders.db.insert(self.table_all,True,**dict(item))
            return item
        elif "source_name" in item:
            spiders.db.insert(self.table_source,True,**dict(item))
            return item
        elif "click_module" in item:
            spiders.db.insert(self.table_click,True,**dict(item))
            return item


    
    