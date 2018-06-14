# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
from it_juzi.items import TiJuzinew_compitem
from it_juzi.items import TiJuzinew_inverstfirm
from it_juzi.items import TiJuzinew_inversttable
from it_juzi.items import TiJuzi_newsfull
class TiJuziPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,TiJuzinew_compitem):
            conn = sqlalchemy.create_engine('mysql+pymysql://root:111111@localhost:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('itjiezi_new_company', metadata,
                                           sqlalchemy.Column('company_id', sqlalchemy.String(100)),
                                           sqlalchemy.Column('brand', sqlalchemy.String(100)),
                                           sqlalchemy.Column('category', sqlalchemy.String(100)),
                                           sqlalchemy.Column('shot_descript', sqlalchemy.String(100)),
                                           sqlalchemy.Column('infor', sqlalchemy.TEXT),
                                           sqlalchemy.Column('company_full_name', sqlalchemy.String(45)),
                                           sqlalchemy.Column('found_time', sqlalchemy.String(45)),
                                           sqlalchemy.Column('guimo', sqlalchemy.String(45)),
                                           sqlalchemy.Column('investtime', sqlalchemy.String(45)),
                                           sqlalchemy.Column('money', sqlalchemy.String(45)),
                                           sqlalchemy.Column('investors', sqlalchemy.String(100)),
                                           sqlalchemy.Column('start_people', sqlalchemy.TEXT),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,TiJuzinew_inverstfirm):
            conn = sqlalchemy.create_engine('mysql+pymysql://root:111111@localhost:3306/hillinsight?charset=utf8',
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
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,TiJuzinew_inversttable):
            conn = sqlalchemy.create_engine('mysql+pymysql://root:111111@localhost:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('it_jiezi_invest_table', metadata,
                                           sqlalchemy.Column('comp_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('type', sqlalchemy.String(45)),
                                           sqlalchemy.Column('x', sqlalchemy.String(100)),
                                           sqlalchemy.Column('y', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dype', sqlalchemy.String(100)),
                                           sqlalchemy.Column('invest_filed', sqlalchemy.TEXT),
                                           sqlalchemy.Column('invest_lunci', sqlalchemy.String(500)),
                                           sqlalchemy.Column('invent_manage', sqlalchemy.TEXT),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item,TiJuzi_newsfull):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('it_jiezi_investnew_context_end', metadata,
                                           sqlalchemy.Column('news_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('title', sqlalchemy.String(500)),
                                           sqlalchemy.Column('tag', sqlalchemy.String(100)),
                                           sqlalchemy.Column('new_date', sqlalchemy.String(45)),
                                           sqlalchemy.Column('source', sqlalchemy.String(100)),
                                           sqlalchemy.Column('context', sqlalchemy.TEXT),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('url', sqlalchemy.String(200)),
                                           )
            insert_table=users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item
    