# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from sqlalchemy.dialects.mysql import DOUBLE
from meituan_pet_server.items import MeituanPetHospitalshopItem
from meituan_pet_server.items import MeituanPetHospitalItem
from meituan_pet_server.items import Meituan_to_Dp_Item
from meituan_pet_server.items import MeituanPetAppdealIdItem
from meituan_pet_server.items import MeituanPetAppyankeItem
from meituan_pet_server.items import MeituanPetAppcommentItem
from meituan_pet_server.items import MeituanPetAppweizhiItem
from meituan_pet_server.items import MeituanPetAppYankecommentItem
class MeituanPetHospitalPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,MeituanPetHospitalshopItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_meituan_shop_info', metadata,
                                           sqlalchemy.Column('mtshop_id', sqlalchemy.String(100)),
                                           sqlalchemy.Column('mtshop_name', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('score', DOUBLE),
                                           sqlalchemy.Column('pinglun_num', sqlalchemy.BIGINT()),
                                           sqlalchemy.Column('shop_sale_num', sqlalchemy.BIGINT()),
                                           sqlalchemy.Column('address', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('avg_price', DOUBLE),
                                           sqlalchemy.Column('city_name', sqlalchemy.String(120)),
                                           sqlalchemy.Column('type', sqlalchemy.String(120)),
                                           sqlalchemy.Column('distract', sqlalchemy.String(120)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(120)),
                                           sqlalchemy.Column('host', sqlalchemy.String(120)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetHospitalItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_meituan_item_info', metadata,
                                           sqlalchemy.Column('mtshop_id', sqlalchemy.String(100)),
                                           sqlalchemy.Column('mtdeal_id', sqlalchemy.String(100)),
                                           sqlalchemy.Column('deal_detail', sqlalchemy.TEXT),
                                           sqlalchemy.Column('price', sqlalchemy.String(120)),
                                           sqlalchemy.Column('old_price', sqlalchemy.String(120)),
                                           sqlalchemy.Column('sold', sqlalchemy.String(120)),
                                           sqlalchemy.Column('score', sqlalchemy.String(120)),
                                           sqlalchemy.Column('pingjia_num', sqlalchemy.String(120)),
                                           sqlalchemy.Column('start_time', sqlalchemy.String(120)),
                                           sqlalchemy.Column('end_time', sqlalchemy.String(120)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(120)),
                                           sqlalchemy.Column('title', sqlalchemy.String(120)),
                                           sqlalchemy.Column('describe', sqlalchemy.String(120)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,Meituan_to_Dp_Item):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_pet_meituan_to_dianping_info', metadata,
                                           sqlalchemy.Column('mtdealid', sqlalchemy.String(100)),
                                           sqlalchemy.Column('brandName', sqlalchemy.String(100)),
                                           sqlalchemy.Column('start_time', sqlalchemy.String(120)),
                                           sqlalchemy.Column('end_time', sqlalchemy.String(120)),
                                           sqlalchemy.Column('originalPrice',DOUBLE),
                                           sqlalchemy.Column('title', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('coupontitle', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('price', DOUBLE),
                                           sqlalchemy.Column('orderTitle', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('dpDealGroupId', sqlalchemy.String(120)),
                                           sqlalchemy.Column('shop_id', sqlalchemy.String(120)),
                                           sqlalchemy.Column('shop_name', sqlalchemy.String(120)),
                                           sqlalchemy.Column('addr', sqlalchemy.String(1200)),
                                           sqlalchemy.Column('avgscore', DOUBLE),
                                           sqlalchemy.Column('dpShopId', sqlalchemy.String(120)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('solds', DOUBLE),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetAppdealIdItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_meituan_deal_id', metadata,
                                           sqlalchemy.Column('deal_id', sqlalchemy.String(100)),
                                           sqlalchemy.Column('title', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('price', sqlalchemy.BIGINT()),
                                           sqlalchemy.Column('old_price', sqlalchemy.BIGINT()),
                                           sqlalchemy.Column('text', sqlalchemy.String(1000)),
                                           sqlalchemy.Column('sale', sqlalchemy.BIGINT()),
                                           sqlalchemy.Column('dt', sqlalchemy.String(20)),
                                           sqlalchemy.Column('shop_id', sqlalchemy.String(100)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetAppyankeItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/o2o?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_hh_meituan_shop_info_tmp', metadata,
                                           sqlalchemy.Column('dpsi_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('shop_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('shop_name', sqlalchemy.String(64)),
                                           sqlalchemy.Column('category1_id', sqlalchemy.INT),
                                           sqlalchemy.Column('category2_id', sqlalchemy.INT),
                                           sqlalchemy.Column('last_update_dt', sqlalchemy.DATE),
                                           sqlalchemy.Column('dt', sqlalchemy.String(20)),
                                           sqlalchemy.Column('city_id', sqlalchemy.INT),
                                           sqlalchemy.Column('city_name', sqlalchemy.String(64)),
                                           sqlalchemy.Column('address', sqlalchemy.String(256)),
                                           sqlalchemy.Column('lng', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('lat', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('avg_price', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('shop_power', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('lat', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('phone_no', sqlalchemy.String(200)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                           sqlalchemy.Column('avgscore', sqlalchemy.String(50)),
                                           sqlalchemy.Column('shop_power', sqlalchemy.String(50)),
                                           sqlalchemy.Column('comments_num', sqlalchemy.INT),
                                           sqlalchemy.Column('historyCouponCount', sqlalchemy.INT),
                                           sqlalchemy.Column('shop_power', sqlalchemy.String(50)),
                                           sqlalchemy.Column('brand', sqlalchemy.String(100)),
                                           sqlalchemy.Column('comments_num', sqlalchemy.String(100)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetAppcommentItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_hh_meituan_shop_comments_tmp', metadata,
                                           sqlalchemy.Column('dsc_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('shop_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('comment_id', sqlalchemy.String(32)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(32)),
                                           sqlalchemy.Column('user_name', sqlalchemy.String(32)),
                                           sqlalchemy.Column('total_score', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('dt', sqlalchemy.String(20)),
                                           sqlalchemy.Column('hash', sqlalchemy.String(100)),
                                           sqlalchemy.Column('comment_text', sqlalchemy.TEXT),
                                           sqlalchemy.Column('comment_dt', sqlalchemy.DATE),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetAppweizhiItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('tuangou_meituan_shop_weizhi', metadata,
                                           sqlalchemy.Column('shop_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('shop_name', sqlalchemy.String(255)),
                                           sqlalchemy.Column('lng', sqlalchemy.String(45)),
                                           sqlalchemy.Column('lat', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
            )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,MeituanPetAppYankecommentItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_hh_meituan_shop_comments_yanke', metadata,
                                           sqlalchemy.Column('dsc_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('shop_id', sqlalchemy.BIGINT),
                                           sqlalchemy.Column('comment_id', sqlalchemy.String(32)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(32)),
                                           sqlalchemy.Column('user_name', sqlalchemy.String(32)),
                                           sqlalchemy.Column('total_score', sqlalchemy.FLOAT),
                                           sqlalchemy.Column('dt', sqlalchemy.String(20)),
                                           sqlalchemy.Column('hash', sqlalchemy.String(100)),
                                           sqlalchemy.Column('comment_text', sqlalchemy.TEXT),
                                           sqlalchemy.Column('comment_dt', sqlalchemy.DATE),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    