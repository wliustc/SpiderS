# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jd_real_time.items import JdRealTimeItem
from jd_real_time.items import JdRealTimeTopItem
from jd_real_time.items import JdRealTimeHourItem
from jd_real_time.items import JdRealTimeFlowSource
import sqlalchemy
class JdRealTimePipeline(object):
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
        metadata = sqlalchemy.MetaData()
        self.table = {
            'liulianglaiyuan': sqlalchemy.Table('t_spider_jd_read_time', metadata,
                                                sqlalchemy.Column('shop_name', sqlalchemy.String(255)),
                                                sqlalchemy.Column('CustPriceAvg', sqlalchemy.String(45)),
                                                sqlalchemy.Column('CustPriceAvg_ytd', sqlalchemy.String(45)),
                                                sqlalchemy.Column('CustPriceAvg_ytdRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdProNum', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdProNum_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdProNum_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdProNum_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdProNum_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdAmt', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdAmt_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdAmt_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdAmt_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdAmt_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdCustNum', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdCustNum_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdCustNum_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdCustNum_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdCustNum_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdNum', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdNum_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdNum_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdNum_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('OrdNum_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('ToOrdRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('ToOrdRate_ytd', sqlalchemy.String(45)),
                                                sqlalchemy.Column('ToOrdRate_ytdRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('PV', sqlalchemy.String(45)),
                                                sqlalchemy.Column('PV_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('PV_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('PV_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('PV_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('ShopCollectNum', sqlalchemy.String(45)),
                                                sqlalchemy.Column('CartUserNum', sqlalchemy.String(45)),
                                                sqlalchemy.Column('UV', sqlalchemy.String(45)),
                                                sqlalchemy.Column('UV_channelPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('UV_ytdTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('UV_ytdTimeRate', sqlalchemy.String(45)),
                                                sqlalchemy.Column('UV_ytdPercent', sqlalchemy.String(45)),
                                                sqlalchemy.Column('realTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('compareTime', sqlalchemy.String(45)),
                                                sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                                sqlalchemy.Column('spuid', sqlalchemy.String(45)),
                                                sqlalchemy.Column('imgurl', sqlalchemy.String(255)),                                                
                                                ),
            'real_time_top':sqlalchemy.Table('t_spider_jd_read_time_top', metadata,
                                             sqlalchemy.Column('date', sqlalchemy.String(255)),
                                             sqlalchemy.Column('shop_name', sqlalchemy.String(45)),
                                             sqlalchemy.Column('title', sqlalchemy.TEXT),
                                             sqlalchemy.Column('xiadan_jine', sqlalchemy.String(45)),
                                             sqlalchemy.Column('xiandan_kehu', sqlalchemy.String(45)),
                                             sqlalchemy.Column('xiadan_danliang', sqlalchemy.String(45)),
                                             sqlalchemy.Column('pv', sqlalchemy.String(45)),
                                             sqlalchemy.Column('uv', sqlalchemy.String(45)),
                                             sqlalchemy.Column('change', sqlalchemy.String(45)),
                                             sqlalchemy.Column('top', sqlalchemy.String(45)),
                                             sqlalchemy.Column('imgurl', sqlalchemy.String(255)),
                                             sqlalchemy.Column('spuid', sqlalchemy.String(45)),
                                             sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                            ),
            'real_time_hour':sqlalchemy.Table('t_spider_jd_real_time_trend', metadata,
                                              sqlalchemy.Column('date', sqlalchemy.String(45)),
                                              sqlalchemy.Column('shop_name', sqlalchemy.String(255)),
                                              sqlalchemy.Column('OrdProNum', sqlalchemy.TEXT),
                                              sqlalchemy.Column('PV', sqlalchemy.String(45)),
                                              sqlalchemy.Column('OrdAmt', sqlalchemy.String(45)),
                                              sqlalchemy.Column('OrdCustNum', sqlalchemy.String(45)),
                                              sqlalchemy.Column('OrdNum', sqlalchemy.String(45)),
                                              sqlalchemy.Column('UV', sqlalchemy.String(45)),
                                              sqlalchemy.Column('hour', sqlalchemy.String(45)),
                                              sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                             ),
            'real_time_flowsource':sqlalchemy.Table('t_spider_jd_real_time_flowsource', metadata,
                                                    sqlalchemy.Column('source', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('shop_name', sqlalchemy.String(255)),
                                                    sqlalchemy.Column('source_id', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('visit_num', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('visit_rate', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('indChannel', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('has_sub', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('has_sub', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('fathersourcename', sqlalchemy.String(255)),
                                                    sqlalchemy.Column('fathersourceid', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                                    sqlalchemy.Column('date', sqlalchemy.String(45)),
                                                   )

        }


    def process_item(self, item, spider):
        if isinstance(item, JdRealTimeItem):
            conn = self.engine.connect()
            insert_table = self.table['liulianglaiyuan'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        if isinstance(item, JdRealTimeTopItem):
            conn = self.engine.connect()
            insert_table = self.table['real_time_top'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdRealTimeHourItem):
            conn = self.engine.connect()
            insert_table = self.table['real_time_hour'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdRealTimeFlowSource):
            conn = self.engine.connect()
            insert_table = self.table['real_time_flowsource'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        return item

    
    
    
    
    
    
    
    
    
    