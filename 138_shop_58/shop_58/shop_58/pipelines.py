# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from shop_58.items import Tongcheng58Item
import sqlalchemy
class Shop58Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,Tongcheng58Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_shangpu_58', metadata,
                                           sqlalchemy.Column('deal_id', sqlalchemy.String(30)),
                                           sqlalchemy.Column('title', sqlalchemy.String(255)),
                                           sqlalchemy.Column('city', sqlalchemy.String(255)),
                                           sqlalchemy.Column('district', sqlalchemy.String(255)),
                                           sqlalchemy.Column('bdistrict', sqlalchemy.String(255)),
                                           sqlalchemy.Column('addr', sqlalchemy.String(255)),
                                           sqlalchemy.Column('lng', sqlalchemy.String(45)),
                                           sqlalchemy.Column('lat', sqlalchemy.String(45)),
                                           sqlalchemy.Column('price', sqlalchemy.String(20)),
                                           sqlalchemy.Column('update_time', sqlalchemy.String(100)),
                                           sqlalchemy.Column('type', sqlalchemy.String(100)),
                                           sqlalchemy.Column('miaoshu', sqlalchemy.TEXT),
                                           sqlalchemy.Column('connect', sqlalchemy.String(200)),
                                           sqlalchemy.Column('phone', sqlalchemy.String(200)),
                                           sqlalchemy.Column('statics', sqlalchemy.String(200)),
                                           sqlalchemy.Column('img', sqlalchemy.TEXT),
                                           sqlalchemy.Column('area', sqlalchemy.String(200)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item
    