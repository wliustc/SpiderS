# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from somefangchan.items import Somefangchan_yingshangItem
class SomefangchanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Somefangchan_yingshangItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('some_fangchan', metadata,
                                           sqlalchemy.Column('deal_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('provice', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('platform', sqlalchemy.String(45)),
                                           sqlalchemy.Column('title', sqlalchemy.String(200)),
                                           sqlalchemy.Column('statics', sqlalchemy.String(45)),
                                           sqlalchemy.Column('open_time', sqlalchemy.String(45)),
                                           sqlalchemy.Column('type', sqlalchemy.String(200)),
                                           sqlalchemy.Column('mianji', sqlalchemy.String(100)),
                                           sqlalchemy.Column('need', sqlalchemy.String(500)),
                                           sqlalchemy.Column('city', sqlalchemy.String(100)),
                                           sqlalchemy.Column('address', sqlalchemy.String(200)),
                                           sqlalchemy.Column('distract', sqlalchemy.String(45)),
                                           sqlalchemy.Column('developer', sqlalchemy.String(200)),
                                           sqlalchemy.Column('connect_name', sqlalchemy.String(45)),
                                           sqlalchemy.Column('connect_duty', sqlalchemy.String(100)),
                                           sqlalchemy.Column('connect_phone', sqlalchemy.String(45)),
                                           sqlalchemy.Column('connect_mphone', sqlalchemy.String(45)),
                                           sqlalchemy.Column('connect_email', sqlalchemy.String(100)),
                                           sqlalchemy.Column('price', sqlalchemy.String(200)),
            )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item

    
    