# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from tx_shippin.items import TxShipinItem
class TxShipinPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TxShipinItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_tx_shipin', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('title', sqlalchemy.String(255)),
                                           sqlalchemy.Column('item_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('type', sqlalchemy.String(255)),
                                           sqlalchemy.Column('score', sqlalchemy.String(45)),
                                           sqlalchemy.Column('count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('floor', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dubo', sqlalchemy.String(45)),
                                           sqlalchemy.Column('zizhi', sqlalchemy.String(45)),
                                           sqlalchemy.Column('year', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('url', sqlalchemy.String(100)),
            )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item

    
    
    
    
    
    