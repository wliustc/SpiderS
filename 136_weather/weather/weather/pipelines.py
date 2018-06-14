# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from weather.items import Weatherhttp2Item
from weather.items import Weatherhttp1Item
from weather.items import Weatherhttp3Item
import sqlalchemy
class WeatherPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Weatherhttp2Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            item['id']=None
            users_table = sqlalchemy.Table('t_spider_weather_unkown_http2', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('city', sqlalchemy.String(200)),
                                           sqlalchemy.Column('date', sqlalchemy.String(200)),
                                           sqlalchemy.Column('temp', sqlalchemy.String(200)),
                                           sqlalchemy.Column('wind', sqlalchemy.String(200)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                           sqlalchemy.Column('statics', sqlalchemy.String(200)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, Weatherhttp1Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            item['id']=None
            users_table = sqlalchemy.Table('t_spider_weather_unkown_http1', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('city', sqlalchemy.String(100)),
                                           sqlalchemy.Column('date', sqlalchemy.String(100)),
                                           sqlalchemy.Column('bWendu', sqlalchemy.String(100)),
                                           sqlalchemy.Column('yWendu', sqlalchemy.String(100)),
                                           sqlalchemy.Column('tianqi', sqlalchemy.String(100)),
                                           sqlalchemy.Column('fengxiang', sqlalchemy.String(100)),
                                           sqlalchemy.Column('fengli', sqlalchemy.String(100)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(100)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, Weatherhttp3Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            item['id']=None
            users_table = sqlalchemy.Table('t_spider_weather_unkown_http3', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('T', sqlalchemy.String(45)),
                                           sqlalchemy.Column('Tmax', sqlalchemy.String(45)),
                                           sqlalchemy.Column('Tmin', sqlalchemy.String(45)),
                                           sqlalchemy.Column('PP', sqlalchemy.String(45)),
                                           sqlalchemy.Column('city', sqlalchemy.String(45)),
                                           sqlalchemy.Column('city_latitude', sqlalchemy.String(45)),
                                           sqlalchemy.Column('city_longitude', sqlalchemy.String(45)),
                                           sqlalchemy.Column('date', sqlalchemy.String(45)),
                                           sqlalchemy.Column('city_name', sqlalchemy.String(200)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)

        return item


    
    