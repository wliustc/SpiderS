# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from m_dianping.items import DianpingShopItem
from m_dianping.items import DianpingDealItem

class DianpingPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DianpingShopItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                     connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_m_dianping_shop_jianshen', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('searchword', sqlalchemy.String(255)),
                                           sqlalchemy.Column('city_name', sqlalchemy.String(255)),
                                           sqlalchemy.Column('city_id', sqlalchemy.String(255)),
                                           sqlalchemy.Column('branchName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('categoryId', sqlalchemy.String(255)),
                                           sqlalchemy.Column('categoryName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('cityId', sqlalchemy.String(255)),
                                           sqlalchemy.Column('shop_id', sqlalchemy.String(255)),
                                           sqlalchemy.Column('matchText', sqlalchemy.String(255)),
                                           sqlalchemy.Column('name', sqlalchemy.String(255)),
                                           sqlalchemy.Column('priceText', sqlalchemy.String(255)),
                                           sqlalchemy.Column('regionName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('reviewCount', sqlalchemy.String(255)),
                                           sqlalchemy.Column('scoreText', sqlalchemy.String(255)),
                                           sqlalchemy.Column('shopPower', sqlalchemy.String(255)),
                                           sqlalchemy.Column('shopType', sqlalchemy.String(255)),
                                           sqlalchemy.Column('shop_address', sqlalchemy.String(255)),
                                           sqlalchemy.Column('phone', sqlalchemy.String(255)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(255)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, DianpingDealItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                 connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_m_dianping_deal_jianshen', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('title', sqlalchemy.String(255)),
                                           sqlalchemy.Column('shop_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('oldprice', sqlalchemy.String(45)),
                                           sqlalchemy.Column('soldNum', sqlalchemy.String(45)),
                                           sqlalchemy.Column('deal_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('desc', sqlalchemy.TEXT),
                                           sqlalchemy.Column('type', sqlalchemy.String(255)),
                                           sqlalchemy.Column('detail', sqlalchemy.TEXT),
                                           sqlalchemy.Column('buy_know', sqlalchemy.TEXT),
                                           sqlalchemy.Column('start_time', sqlalchemy.String(45)),
                                           sqlalchemy.Column('end_time', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item

    
    
    
    
    
    
    