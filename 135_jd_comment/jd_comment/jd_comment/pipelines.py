# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jd_comment.items import JdCommentItem
from jd_comment.items import JdSkuItem
import sqlalchemy

class JdCommentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JdSkuItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            item['id']=None
            users_table = sqlalchemy.Table('jd_sku_data', metadata,
                                           sqlalchemy.Column('id', sqlalchemy.INT),
                                           sqlalchemy.Column('sku', sqlalchemy.String(100)),
                                           sqlalchemy.Column('spu', sqlalchemy.String(100)),
                                           sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                           sqlalchemy.Column('brand', sqlalchemy.String(200)),
                                           sqlalchemy.Column('price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('chicun', sqlalchemy.String(45)),
                                           sqlalchemy.Column('yanse', sqlalchemy.String(45)),
                                           sqlalchemy.Column('title', sqlalchemy.String(2000)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, JdCommentItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('jd_sku_comment', metadata,
                                           sqlalchemy.Column('sku', sqlalchemy.String(100)),
                                           sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                           sqlalchemy.Column('brand', sqlalchemy.String(200)),
                                           sqlalchemy.Column('price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('comments', sqlalchemy.TEXT),
                                           sqlalchemy.Column('comment_id', sqlalchemy.TEXT),
                                           sqlalchemy.Column('comment_type', sqlalchemy.String(45)),
                                           sqlalchemy.Column('good_comment_rate', sqlalchemy.String(45)),
                                           sqlalchemy.Column('comment_time', sqlalchemy.String(45)),
                                           sqlalchemy.Column('comments_name', sqlalchemy.String(45)),
                                           sqlalchemy.Column('score', sqlalchemy.String(45)),
                                           sqlalchemy.Column('reply', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('chicun', sqlalchemy.String(45)),
                                           sqlalchemy.Column('yanse', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        return item


    