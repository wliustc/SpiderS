# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlalchemy
import time
import datetime
import sys
import web
from jd_shangzhi.items import JdShangzhiliuliangItem
from jd_shangzhi.items import JdShangTrafficItem
from jd_shangzhi.items import JdShangTransctItem
from jd_shangzhi.items import JdShangGoodsItem
from jd_shangzhi.items import JdShangDealtraitItem
from jd_shangzhi.items import JdShangAftersalesItem
from jd_shangzhi.items import JdShangCoreItem
from jd_shangzhi.items import JdShangOrderdetailItem
from jd_shangzhi.items import JdShangOrderclientItem
from jd_shangzhi.items import JdShangGoodsdskuItem
from jd_shangzhi.items import JdShangzhiliuliangdownItem

class JdShangzhiPipeline(object):
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
            connect_args={'charset': 'utf8'})
        metadata = sqlalchemy.MetaData()
        self.table = {
            'liulianglaiyuan': sqlalchemy.Table('t_spider_jdweizhi_flow_source', metadata,
                                                sqlalchemy.Column('id', sqlalchemy.INT),
                                                sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                                sqlalchemy.Column('source', sqlalchemy.String(200)),
                                                sqlalchemy.Column('category1', sqlalchemy.String(45)),
                                                sqlalchemy.Column('category2', sqlalchemy.String(45)),
                                                sqlalchemy.Column('category3', sqlalchemy.String(45)),
                                                sqlalchemy.Column('shop_CustRate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('shop_CustRate_rate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('peer_UV', sqlalchemy.String(200)),
                                                sqlalchemy.Column('shop_UV', sqlalchemy.String(200)),
                                                sqlalchemy.Column('shop_UV_rate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('peer_CustRate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('uv_zhanbi', sqlalchemy.String(200)),
                                                sqlalchemy.Column('uv_zhanbi_rate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('scan', sqlalchemy.String(200)),
                                                sqlalchemy.Column('scan_rate', sqlalchemy.String(200)),
                                                sqlalchemy.Column('date', sqlalchemy.String(200)),
                                                sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                sqlalchemy.Column('fufei', sqlalchemy.String(200)),
                                                sqlalchemy.Column('sourceid', sqlalchemy.String(200)),
                                                sqlalchemy.Column('fathersourceid', sqlalchemy.String(200)),
                                                sqlalchemy.Column('fathername', sqlalchemy.String(255)),
                                                )
            , 'jiaoyigaikuang': sqlalchemy.Table('t_spider_jdweizhi_transact', metadata,
                                                 sqlalchemy.Column('id', sqlalchemy.INT),
                                                 sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdCustNum', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('AvgDepth', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('PV_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdAmt', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('PV', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('CustPriceAvg_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('UV_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdCustNum_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ToOrdRate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('SkipOut', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('AvgStayTime_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdNum_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ToOrdRate_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdAmt_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('CustPriceAvg', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('SkipOut_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('AvgDepth_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdProNum_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('AvgStayTime', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdNum', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('OrdProNum', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('UV', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('date', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                 ),
            'liulianggaikuo': sqlalchemy.Table('t_spider_jdweizhi_traffic', metadata,
                                               sqlalchemy.Column('id', sqlalchemy.INT),
                                               sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                               sqlalchemy.Column('jump_rate', sqlalchemy.String(200)),
                                               sqlalchemy.Column('visitors', sqlalchemy.String(200)),
                                               sqlalchemy.Column('stay', sqlalchemy.String(200)),
                                               sqlalchemy.Column('source', sqlalchemy.String(200)),
                                               sqlalchemy.Column('jump_rate_contrast', sqlalchemy.String(200)),
                                               sqlalchemy.Column('visitors_abnormal', sqlalchemy.String(200)),
                                               sqlalchemy.Column('views', sqlalchemy.String(200)),
                                               sqlalchemy.Column('Per_capita_views_abnormal',
                                                                 sqlalchemy.String(200)),
                                               sqlalchemy.Column('views_rate', sqlalchemy.String(200)),
                                               sqlalchemy.Column('views_abnormal', sqlalchemy.String(200)),
                                               sqlalchemy.Column('stay_abnormal', sqlalchemy.String(200)),
                                               sqlalchemy.Column('visitors_rate', sqlalchemy.String(200)),
                                               sqlalchemy.Column('stay_rate', sqlalchemy.String(200)),
                                               sqlalchemy.Column('jump_rate_abnormal', sqlalchemy.String(200)),
                                               sqlalchemy.Column('Per_capita_views_rate', sqlalchemy.String(200)),
                                               sqlalchemy.Column('Per_capita_views', sqlalchemy.String(200)),
                                               sqlalchemy.Column('date', sqlalchemy.String(200)),
                                               sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                               ),
            'shangpingaikuang': sqlalchemy.Table('t_spider_jdweizhi_goods', metadata,
                                                 sqlalchemy.Column('id', sqlalchemy.INT),
                                                 sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsAddBuyRate_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyCustNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyGoodsPieceNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ordGoodsPieceNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsConverRate_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyGoodsPieceNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsConcernNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyCustNum_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('saleGoodsNum_value', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ordAmt_value', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('visitedGoodsNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsBrowseNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('visitedGoodsNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsBrowseNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsConcernNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyGoodsNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addBuyGoodsNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsSaleRate_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsVisitorNum_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsVisitorNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsAddBuyRate_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ordAmt_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsSaleRate_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsConverRate_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('saleGoodsNum_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ordGoodsPieceNum_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsExposureRate_value',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsExposureRate_rate',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('goodsSaleRate_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ProSkipOut_value', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('ProSkipOut_rate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('date', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                 ),
            'jiaoyitezheng': sqlalchemy.Table('t_spider_jdweizhi_deal_trait', metadata,
                                              sqlalchemy.Column('id', sqlalchemy.INT),
                                              sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                              sqlalchemy.Column('peer_occupies', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Orders_amount', sqlalchemy.String(200)),
                                              sqlalchemy.Column('channel', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Orders_occupies', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Orders_money', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Orders_client', sqlalchemy.String(200)),
                                              sqlalchemy.Column('date', sqlalchemy.String(200)),
                                              sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                              ),
            'shouhoufenxi': sqlalchemy.Table('t_spider_jdweizhi_after_sale', metadata,
                                             sqlalchemy.Column('id', sqlalchemy.INT),
                                             sqlalchemy.Column('replyRatio_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numGs_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numFx_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtFx_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numTs_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numTh_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtFx_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ordDisRatio_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numGs_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numHh_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtHh_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numGd_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtHh_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtTh_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('amtTh_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numTh_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numHh_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ordDisRatioInd_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('replyRatio_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ordDisRatioInd_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numGd_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numTs_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ordDisRatio_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('numFx_value', sqlalchemy.String(200)),
                                             sqlalchemy.Column('date', sqlalchemy.String(200)),
                                             sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                             ),
            'hexinzhibiao': sqlalchemy.Table('t_spider_jdweizhi_ci', metadata,
                                             sqlalchemy.Column('id', sqlalchemy.INT),
                                             sqlalchemy.Column('Orders_sum', sqlalchemy.String(200)),
                                             sqlalchemy.Column('Orders_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('OrdersRate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('PV', sqlalchemy.String(200)),
                                             sqlalchemy.Column('PV_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('PVRate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('UV', sqlalchemy.String(200)),
                                             sqlalchemy.Column('UV_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('UVRate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('CustPriceAvg', sqlalchemy.String(200)),
                                             sqlalchemy.Column('CustPriceAvg_Price', sqlalchemy.String(200)),
                                             sqlalchemy.Column('CustPriceAvg_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('CustRate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('Cust_wireless_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('Cust_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The90', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The90Rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The90_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The30', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The30Rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('The30_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ShopCollectNum', sqlalchemy.String(200)),
                                             sqlalchemy.Column('App_population', sqlalchemy.String(200)),
                                             sqlalchemy.Column('ShopCollectNum_rate', sqlalchemy.String(200)),
                                             sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                             sqlalchemy.Column('date', sqlalchemy.String(200)),
                                             sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                             ),
            'dingdanmingxi': sqlalchemy.Table('t_spider_jdweizhi_order_details', metadata,
                                              sqlalchemy.Column('id', sqlalchemy.INT),
                                              sqlalchemy.Column('OrderID', sqlalchemy.String(200)),
                                              sqlalchemy.Column('cover_charge', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Order_time', sqlalchemy.String(200)),
                                              sqlalchemy.Column('title', sqlalchemy.String(200)),
                                              sqlalchemy.Column('coupon', sqlalchemy.String(200)),
                                              sqlalchemy.Column('raw_money', sqlalchemy.String(200)),
                                              sqlalchemy.Column('order_amount', sqlalchemy.String(200)),
                                              sqlalchemy.Column('source', sqlalchemy.String(200)),
                                              sqlalchemy.Column('freight', sqlalchemy.String(200)),
                                              sqlalchemy.Column('commodity_count', sqlalchemy.String(200)),
                                              sqlalchemy.Column('paytime', sqlalchemy.String(200)),
                                              sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                              sqlalchemy.Column('Payment', sqlalchemy.String(200)),
                                              sqlalchemy.Column('date', sqlalchemy.String(200)),
                                              sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                              )
            , 'kehushuju': sqlalchemy.Table('t_spider_jdweizhi_orders_client', metadata,
                                            sqlalchemy.Column('id', sqlalchemy.INT),
                                            sqlalchemy.Column('Orders_rate', sqlalchemy.String(200)),
                                            sqlalchemy.Column('Guest_piece', sqlalchemy.String(200)),
                                            sqlalchemy.Column('payPct', sqlalchemy.String(200)),
                                            sqlalchemy.Column('Guest_piece_rate', sqlalchemy.String(200)),
                                            sqlalchemy.Column('upt_rate', sqlalchemy.String(200)),
                                            sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                            sqlalchemy.Column('Orders_client_rate', sqlalchemy.String(200)),
                                            sqlalchemy.Column('client_type', sqlalchemy.String(200)),
                                            sqlalchemy.Column('Orders_rate_contrast', sqlalchemy.String(200)),
                                            sqlalchemy.Column('payPct_rate', sqlalchemy.String(200)),
                                            sqlalchemy.Column('upt', sqlalchemy.String(200)),
                                            sqlalchemy.Column('Orders_client', sqlalchemy.String(200)),
                                            sqlalchemy.Column('date', sqlalchemy.String(200)),
                                            sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                            )
            , 'shangpinmingxi': sqlalchemy.Table('t_spider_jdweizhi_goods_details', metadata,
                                                 sqlalchemy.Column('id', sqlalchemy.INT),
                                                 sqlalchemy.Column('huohao', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('id_', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('orderItemQty',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('views', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('Focus_on', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('addCartItemCnt',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('title', sqlalchemy.String(1000)),
                                                 sqlalchemy.Column('launch_time',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('comments', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('orderRate', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('visitors', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('orderAmt', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('orderBuyerCnt',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('url', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('UAworth', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('Purchase_one',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('Orders_quantity',
                                                                   sqlalchemy.String(200)),
                                                 sqlalchemy.Column('date', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('type', sqlalchemy.String(200)),
                                                 sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                 )
            ,'shangzhi_flow_source_down':sqlalchemy.Table('t_spider_jdweizhi_flow_source_down', metadata,
                                                 sqlalchemy.Column('id', sqlalchemy.INT),
                                                 sqlalchemy.Column('shop_name', sqlalchemy.String(255)),
                                                 sqlalchemy.Column('source', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('shop_UV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_UV',sqlalchemy.String(45)),
                                                 sqlalchemy.Column('PV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_PV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('jumplose',sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_jumplose', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('per_PV',sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_per_PV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('avg_time', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_avg_time', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('new_UV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_new_UV',sqlalchemy.String(45)),
                                                 sqlalchemy.Column('old_UV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('peer_old_UV', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('date', sqlalchemy.String(45)),
                                                 sqlalchemy.Column('dt', sqlalchemy.String(45)),
                                                 )
        }

    def time_parse(self, t):
        t = int(t)
        today = datetime.date.today()
        oneday = datetime.timedelta(days=t)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def process_item(self, item, spider):
        if isinstance(item, JdShangzhiliuliangItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if item['category2'] == None:
                item['category2']='null'
            if item['category3'] == None:
                item['category3']='null'
            insert_table = self.table['liulianglaiyuan'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangTransctItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['jiaoyigaikuang'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangTrafficItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['liulianggaikuo'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangGoodsItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['shangpingaikuang'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangDealtraitItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['jiaoyitezheng'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangAftersalesItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['shouhoufenxi'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangCoreItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['hexinzhibiao'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangOrderdetailItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['dingdanmingxi'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangOrderclientItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['kehushuju'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangGoodsdskuItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['shangpinmingxi'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()
        elif isinstance(item, JdShangzhiliuliangdownItem):
            conn = self.engine.connect()
            item['id'] = None
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            insert_table = self.table['shangzhi_flow_source_down'].insert().prefix_with('IGNORE')
            conn.execute(insert_table, **item)
            conn.close()        
        return item

    def chage_sql(self, db, spider_table, dt):
        sql_check = "select `name` from hillinsight.t_spider_JD_shangzhi as a where not exists(" \
                    "select distinct `shop_name` from hillinsight.%s as b where a.`name`=b.`shop_name` " \
                    "and `date`='%s');" % (spider_table, dt)  # 昨天

        temp = db.query(sql_check)
        if not temp:
            tmp = db.query('select * from hillinsight.t_spider_jdweizhi_spider '
                           'where `spider_name`="%s" and `dt`="%s";' % (spider_table, dt))  # 昨天)
            if tmp:
                db.query('update hillinsight.t_spider_jdweizhi_spider set `flag`=1 where '
                         '`spider_name`="%s" and `dt`="%s";' % (spider_table, dt))
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`spider_name`,`dt`,'
                         '`flag`) VALUE (NULL,"%s","%s","1")' % (spider_table, dt))

    def chage_type_sql(self, db, spider_table, name, dt):
        if name == 'shangzhi_goods_dsku':
            type = 'sku'
        else:
            type = 'spu'
        sql_check = "select `name` from hillinsight.t_spider_JD_shangzhi as a where not exists(" \
                    "select distinct `shop_name` from hillinsight.%s as b " \
                    "where a.`name`=b.`shop_name` and `type`='%s' and `date`='%s' );" % (spider_table, type, dt)  # 昨天

        temp = db.query(sql_check)
        if not temp:
            tmp = db.query('select * from hillinsight.t_spider_jdweizhi_spider '
                           'where `spider_name`="%s" and `dt`="%s";' % (spider_table + '_' + type, dt))  # 昨天)
            if tmp:
                db.query('update hillinsight.t_spider_jdweizhi_spider set `flag`=1 where '
                         '`spider_name`="%s" and `dt`="%s";' % (spider_table + '_' + type, dt))
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`spider_name`,`dt`,'
                         '`flag`) VALUE (NULL,"%s","%s","1")' % (spider_table + '_' + type, dt))

    def close_spider(self, spider):
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

        list_key = {'shangzhi_after_sale': 't_spider_jdweizhi_after_sale',
                    'shangzhi_core': 't_spider_jdweizhi_ci',
                    'shangzhi_liuliang': 't_spider_jdweizhi_flow_source',
                    'shangzhi_goods': 't_spider_jdweizhi_goods',
                    'shangzhi_goods_dsku': 't_spider_jdweizhi_goods_details',
                    'shangzhi_goods_dspu': 't_spider_jdweizhi_goods_details',
                    'shangzhi_order_detail': 't_spider_jdweizhi_order_details',
                    'shangzhi_order_client': 't_spider_jdweizhi_orders_client',
                    'shangzhi_traffic': 't_spider_jdweizhi_traffic',
                    'shangzhi_transact': 't_spider_jdweizhi_transact',
                    'shangzhi_deal_trait':'t_spider_jdweizhi_deal_trait',
                   'shangzhi_flow_source_down':'t_spider_jdweizhi_flow_source_down'}
        spider_table = list_key[spider.name]
        if spider_table == 't_spider_jdweizhi_goods_details':
            self.chage_type_sql(db, spider_table, spider.name, self.time_parse(1))
        elif spider_table == 't_spider_jdweizhi_orders_client':
            self.chage_sql(db, spider_table, self.time_parse(2))
        else:
            self.chage_sql(db, spider_table, self.time_parse(1))




    
    
    
    
    