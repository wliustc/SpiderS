# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlalchemy
from weixinsmall.items import WeixinsmallItem
from weixinsmall.items import WeixinsmallTakerItem
from weixinsmall.items import WeixinsmallTopicInfoItem
from weixinsmall.items import WeixinsmallTopicUserInfoItem
from weixinsmall.items import WeixinsmallbidslstItem
from weixinsmall.items import WeixinsmallSponsorItem

class WeixinsmallPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeixinsmallItem):
            conn = sqlalchemy.create_engine(
            'mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_list', metadata,
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_title', sqlalchemy.String(255)),
                                           sqlalchemy.Column('topic_abstract', sqlalchemy.TEXT),
                                           sqlalchemy.Column('topic_view_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_ctime_standard', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('homecity', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_like_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('amount', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_address', sqlalchemy.String(255)),
                                           sqlalchemy.Column('market_price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_collect_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('pricetype', sqlalchemy.String(45)),
                                           sqlalchemy.Column('pricetypename', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_status', sqlalchemy.String(45)),
                                           sqlalchemy.Column('last_bid_price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_url', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_url', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_tags', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_cell', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_realname', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, WeixinsmallTakerItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
                                            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_taker', metadata,
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('total', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('order_ctime', sqlalchemy.String(45)),
                                           sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                           sqlalchemy.Column('date', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, WeixinsmallTopicInfoItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_topicinfo', metadata,
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_order', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_view_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_comment_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_like_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_collect_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_sponsor_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_title', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_abstract', sqlalchemy.TEXT),
                                           sqlalchemy.Column('allowcommenting', sqlalchemy.String(45)),
                                           sqlalchemy.Column('group_members', sqlalchemy.String(45)),
                                           sqlalchemy.Column('price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('market_price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('amount', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_bid_hours', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_address', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_tags', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_limited_buying', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_sold_amout', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_order_price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('scope_level', sqlalchemy.String(45)),
                                           sqlalchemy.Column('pic_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('status', sqlalchemy.String(45)),
                                           sqlalchemy.Column('sponsor_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('btn_pricetypename', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, WeixinsmallTopicUserInfoItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_topicuserinfo', metadata,
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_status', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_cell', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_wechat_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_realname', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_address', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_email', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_ctime', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_level', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_name', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_alias', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_title', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_follow_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_follower_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_survey_score', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_relation_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_topic_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_homecity', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userGender', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userRegfrom', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userType', sqlalchemy.String(45)),
                                           sqlalchemy.Column('sceneId', sqlalchemy.String(45)),
                                           sqlalchemy.Column('credit', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userName', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_quotas', sqlalchemy.String(45)),
                                           sqlalchemy.Column('homecity', sqlalchemy.String(45)),
                                           sqlalchemy.Column('btnfollow', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, WeixinsmallbidslstItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_topicbidslstinfo', metadata,
                                           sqlalchemy.Column('userName', sqlalchemy.String(255)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('homecity', sqlalchemy.String(45)),
                                           sqlalchemy.Column('bid_price', sqlalchemy.String(45)),
                                           sqlalchemy.Column('bid_ctime', sqlalchemy.String(45)),
                                           sqlalchemy.Column('bid_status', sqlalchemy.String(45)),
                                           sqlalchemy.Column('bid_statusname', sqlalchemy.String(45)),
                                           sqlalchemy.Column('id', sqlalchemy.String(45)),
                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)
        elif isinstance(item, WeixinsmallSponsorItem):
            conn = sqlalchemy.create_engine('mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
            metadata = sqlalchemy.MetaData(conn)
            users_table = sqlalchemy.Table('t_spider_xiangwushuo_Sponsor', metadata,
                                           sqlalchemy.Column('topic_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_status', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_cell', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_wechat_id', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_realname', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_address', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_email', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_secret', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_ctime', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_alias', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_title', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_follow_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_follower_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_survey_score', sqlalchemy.String(45)),                                           
                                           sqlalchemy.Column('user_email', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_relation_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_topic_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_comment_count', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_homecity', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userGender', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userType', sqlalchemy.String(45)),
                                           sqlalchemy.Column('credit', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_help_flowers', sqlalchemy.String(45)),
                                           sqlalchemy.Column('userName', sqlalchemy.String(45)),
                                           sqlalchemy.Column('user_quotas', sqlalchemy.String(45)),

                                           )
            insert_table = users_table.insert().prefix_with('IGNORE')
            insert_table.execute(item)

        return item

    
    
    
    