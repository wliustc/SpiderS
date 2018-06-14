# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from gongjiao_8684.items import Gongjiao8684Item
import sqlalchemy
class Gongjiao8684Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,Gongjiao8684Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('public_bus_from_8684', metadata,
                                           sqlalchemy.Column('provice', sqlalchemy.String(200)),
                                           sqlalchemy.Column('city', sqlalchemy.String(200)),
                                           sqlalchemy.Column('tran_type', sqlalchemy.String(200)),
                                           sqlalchemy.Column('line_name', sqlalchemy.String(200)),
                                           sqlalchemy.Column('title', sqlalchemy.String(200)),
                                           sqlalchemy.Column('transform_time', sqlalchemy.String(200)),
                                           sqlalchemy.Column('piaojia', sqlalchemy.String(2000)),
                                           sqlalchemy.Column('company', sqlalchemy.String(45)),
                                           sqlalchemy.Column('update_time', sqlalchemy.String(200)),
                                           sqlalchemy.Column('descript', sqlalchemy.TEXT),
                                           sqlalchemy.Column('direct', sqlalchemy.String(200)),
                                           sqlalchemy.Column('bus_sum_num', sqlalchemy.INT),
                                           sqlalchemy.Column('port_num', sqlalchemy.INT),
                                           sqlalchemy.Column('port_name', sqlalchemy.String(2000)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item

    
    