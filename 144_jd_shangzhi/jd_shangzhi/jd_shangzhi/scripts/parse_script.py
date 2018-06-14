# coding:utf8
import json
import sys
from collections import OrderedDict
import sqlalchemy
import time

reload(sys)
sys.setdefaultencoding("utf-8")

parses_dict = {
    u'交易概况': 'transact',
    u'流量概括': 'traffic',
    u'商品概览': 'goods',
    u'商品明细sku': 'goods_details',
    u'商品明细spu': 'goods_details',
    u'交易特征': 'deal_trait',
    u'售后分析': 'after_sale',
    u'下单客户分析': 'Orders_client',
    u'核心指标': 'Core_KPI',
    u'流量来源': 'flow_source',
    u'订单明细': 'order_details'
}


class parses(object):

    def __init__(self):
        metadata = sqlalchemy.MetaData()
        self.table={
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
            'liulianglaiyuan': sqlalchemy.Table('t_spider_jdweizhi_flow_source', metadata,
                                                  sqlalchemy.Column('id', sqlalchemy.INT),
                                                  sqlalchemy.Column('shop_name', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('source_type', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('shop_CustRate', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('peer_UV', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('source', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('shop_UV', sqlalchemy.String(200)),
                                                  sqlalchemy.Column('peer_CustRate', sqlalchemy.String(200)),
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
            , 'shouhoufenxi': sqlalchemy.Table('t_spider_jdweizhi_after_sale', metadata,
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
                                               )
            , 'jiaoyitezheng': sqlalchemy.Table('t_spider_jdweizhi_deal_trait', metadata,
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
                                                )
            , 'liulianggaikuo': sqlalchemy.Table('t_spider_jdweizhi_traffic', metadata,
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
                                                        sqlalchemy.Column('date', sqlalchemy.String(200)),
                                                        sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                        ),
            'shangpinmingxi': sqlalchemy.Table('t_spider_jdweizhi_goods_details', metadata,
                                                                sqlalchemy.Column('id', sqlalchemy.INT),
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
                                                                sqlalchemy.Column('dt', sqlalchemy.String(200)),
                                                                )

        }

    def transact(self, datas):
        # 交易概况
        item = {}
        item['type'] = 'jiaoyigaikuang'
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'jiaoyigaikuang'
                item['date'] = '访问受限'
                yield item
                return
        # 下单商品件数
        item['OrdProNum'] = data['content']['OrdProNum']['value']
        # 下单百分比
        rates = data['content']['OrdProNum']['rate']
        item['OrdProNum_rate'] = "%.2f%%" % (rates * 100)
        # 客单价
        item['CustPriceAvg'] = data['content']['CustPriceAvg']['value']
        # 百分比
        CustPriceAvg_rates = data['content']['CustPriceAvg']['rate']
        item['CustPriceAvg_rate'] = "%.2f%%" % (CustPriceAvg_rates * 100)
        # 人均浏览量
        item['AvgDepth'] = data['content']['AvgDepth']['value']
        # 百分比
        AvgDepth_rates = data['content']['AvgDepth']['rate']
        item['AvgDepth_rate'] = "%.2f%%" % (AvgDepth_rates * 100)
        # 平均停留时长
        item['AvgStayTime'] = data['content']['AvgStayTime']['value']
        # 百分比
        AvgStayTime_rates = data['content']['AvgStayTime']['rate']
        item['AvgStayTime_rate'] = "%.2f%%" % (AvgStayTime_rates * 100)
        # 下单转化率
        item['ToOrdRate'] = data['content']['ToOrdRate']['value']
        # 百分比
        ToOrdRate_rates = data['content']['ToOrdRate']['rate']
        item['ToOrdRate_rate'] = "%.2f%%" % (ToOrdRate_rates * 100)
        # 下单金额
        item['OrdAmt'] = data['content']['OrdAmt']['value']
        # 百分比
        OrdAmt_rates = data['content']['OrdAmt']['rate']
        item['OrdAmt_rate'] = "%.2f%%" % (OrdAmt_rates * 100)
        # 跳失率
        item['SkipOut'] = data['content']['SkipOut']['value']
        # 百分比
        SkipOut_rates = data['content']['SkipOut']['rate']
        item['SkipOut_rate'] = "%.2f%%" % (SkipOut_rates * 100)
        # 浏览量
        item['PV'] = data['content']['PV']['value']
        # 百分比
        PV_rates = data['content']['PV']['rate']
        item['PV_rate'] = "%.2f%%" % (PV_rates * 100)
        # 下单客户数
        item['OrdCustNum'] = data['content']['OrdCustNum']['value']
        # 百分比
        OrdCustNum_rates = data['content']['OrdCustNum']['rate']
        item['OrdCustNum_rate'] = "%.2f%%" % (OrdCustNum_rates * 100)
        # 下单单量
        item['OrdNum'] = data['content']['OrdNum']['value']
        # 百分比
        OrdNum_rates = data['content']['OrdNum']['rate']
        item['OrdNum_rate'] = "%.2f%%" % (OrdNum_rates * 100)
        # 访客数
        item['UV'] = data['content']['UV']['value']
        # 百分比
        UV_rates = data['content']['UV']['rate']
        item['UV_rate'] = "%.2f%%" % (UV_rates * 100)
        item['shop_name'] = shop_name
        item['date'] = datas['date']
        yield item

    def traffic(self, datas):
        # 流量概括
        '''source:渠道，visitors：访客数，visitors_rate：访客对比，visitors_abnormal：异常天数
           views：浏览量，views_rate浏览量对比，views_abnormal：异常天数，jump_rate：跳失率，jump_rate_contrast：跳失率对比
           jump_rate_abnormal：异常天数，Per_capita_views：人均浏览量，Per_capita_views_rate：人均浏览量对比，Per_capita_views_abnormal：异常天数
           stay：平均停留时长（秒），stay_rate：平均停留时长对比，stay_abnormal：异常天数
        '''
        field_list = ['source', 'visitors', 'visitors_rate', 'visitors_abnormal', 'views', 'views_rate',
                      'views_abnormal', 'jump_rate', 'jump_rate_contrast', 'jump_rate_abnormal', 'Per_capita_views',
                      'Per_capita_views_rate', 'Per_capita_views_abnormal', 'stay', 'stay_rate', 'stay_abnormal']
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'liulianggaikuo'
                item['date'] = '访问受限'
                yield item
                return
        for i in data['content']['data']:
            item = dict(zip(field_list, i))
            item['type'] = 'liulianggaikuo'
            for key in item.keys():
                if 'rate' in key:
                    item[key] = "%.2f%%" % (item[key] * 100)
                elif isinstance(item.get(key), float):
                    item[key] = '%.2f' % item.get(key)
            item['shop_name'] = shop_name
            item['date'] = datas['date']
            yield item

    def goods(self, datas):
        # 商品概况
        '''
        goodsAddBuyRate_value:商品加购率，addBuyCustNum_value：加购客户数，addBuyGoodsPieceNum_rate：加购商品件数对比
        ordGoodsPieceNum_value：下单商品件数，goodsConverRate_value：商品转化率，addBuyGoodsPieceNum_value：加购商品件数
        goodsConcernNum_rate：商品关注数对比，addBuyCustNum_rate：加购客户数对比，saleGoodsNum_value：动销商品数
        ordAmt_value：下单金额，visitedGoodsNum_rate：被访问商品数对比，goodsBrowseNum_value：商品浏览量，visitedGoodsNum_value：被访问商品数
        goodsBrowseNum_rate：商品浏览量对比，goodsConcernNum_value：商品关注数，addBuyGoodsNum_rate：商品加购率对比
        goodsSaleRate_rate：商品动销率对比，goodsVisitorNum_rate：商品访客数对比，goodsVisitorNum_value：商品访客数
        addBuyGoodsNum_value：加购商品数，goodsExposureRate_rate：商品曝光率对比，goodsAddBuyRate_rate：商品加购率对比
        ordAmt_rate：下单金额对比，goodsSaleRate_value：商品动销率，goodsConverRate_rate：商品转化率对比
        saleGoodsNum_rate：动销商品数对比，ordGoodsPieceNum_rate：下单商品件数对比，goodsExposureRate_value：商品曝光率
        '''
        item = {}
        shop_name = datas['shop_name']
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'shangpingaikuang'
                item['date'] = '访问受限'
                yield item
                return
        for i in data['content']:
            item[i + '_value'] = data['content'].get(i).get('value')
            item[i + '_rate'] = "%.2f%%" % (data['content'].get(i).get('rate') * 100)
        for i in item:
            if i in ['goodsAddBuyRate_value', 'goodsConverRate_value', 'goodsSaleRate_value',
                     'goodsExposureRate_value']:
                item[i] = "%.2f%%" % (item[i] * 100)
        item['shop_name'] = shop_name
        item['type'] = 'shangpingaikuang'
        item['date'] = datas['date']
        yield item

    def goods_details(self, datas):
        # 商品明细
        '''title:商品名称，visitors：访客数，views：浏览量，Focus_on：商品关注数,addCartItemCnt：加购商品件数,Purchase_one：加购人数
           orderBuyerCnt：下单客户数,Orders_quantity：下单单量,orderItemQty：下单商品件数,orderAmt：下单金额,orderRate：下单转化率,UAworth：UV价值
           comments：评价数,launch_time：上架时间,id_:sku或spu,url:商品地址
        '''
        field_list = ['title', 'visitors', 'views', 'Focus_on', 'addCartItemCnt', 'Purchase_one', 'orderBuyerCnt',
                      'Orders_quantity', 'orderItemQty', 'orderAmt', 'orderRate', 'UAworth', 'comments', 'launch_time',
                      'id_', 'url']
        cate = datas['cate']
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'shangpinmingxi'
                item['date'] = '访问受限'
                yield item
                return
        #       print cate
        if cate == u'商品明细spu':
            for i in data['content']['gridData']['data'][:-1]:
                i = i[:-1]
                item = dict(zip(field_list, i))
                item['UAworth'] = "%.2f%%" % (item['UAworth'])
                item['shop_name'] = shop_name
                item['type'] = 'shangpinmingxi'
                item['date'] = datas['date']
                yield item
        else:
            for i in data['content']['gridData']['data'][:-1]:
                i = i[:-1]
                url = 'https://item.jd.com/%s.html' % i[-1]
                i.append(url)
                item = dict(zip(field_list, i))
                item['UAworth'] = "%.2f%%" % (item['UAworth'])
                item['shop_name'] = shop_name
                item['type'] = 'shangpinmingxi'
                item['date'] = datas['date']
                yield item

    def deal_trait(self, datas):
        # 交易特征
        '''
         channel:渠道,Orders_client:下单客户数,Orders_amount:下单单量,
         Orders_money:下单金额,Orders_occupies:下单金额占比店铺
         peer_occupies:同行同级均值

        '''
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'jiaoyitezheng'
                item['date'] = '访问受限'
                yield item
                return
        field_list = ['channel', 'Orders_client', 'Orders_amount', 'Orders_money', 'Orders_occupies', 'peer_occupies']
        for i in data['content']['feature']['data']:
            item = dict(zip(field_list, i))
            for i in item:
                if i in ['peer_occupies', 'Orders_occupies']:
                    item[i] = "%.2f%%" % (item[i] * 100)
            item['shop_name'] = shop_name
            item['type'] = 'jiaoyitezheng'
            item['date'] = datas['date']
            yield item

    def after_sale(self, datas):
        # 售后分析
        '''
        numFx_rate:返修换新量对比，numTh_value：退货量，amtTh_rate：退货金额对比
        amtTh_value：退货金额，numTh_rate：退货量对比，numFx_value：返修换新量
        replyRatio_value：工单回复率，replyRatio_rate：工单回复率对比
        numGs_value：工商投诉数量，numGd_value：工单量，amtFx_value：返修换新金额
        numHh_value：换良量，numTs_value：用户投诉数量
        '''
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'shouhoufenxi'
                item['date'] = '访问受限'
                yield item
                return
        shop_name = datas['shop_name']
        item = {}
        for i in data['content']['summary']:
            # print i
            item[i + '_value'] = data['content']['summary'].get(i).get('value')
            if data['content']['summary'].get(i).get('rate') != '-':
                item[i + '_rate'] = "%.2f%%" % (data['content']['summary'].get(i).get('rate') * 100)
            else:
                item[i + '_rate'] = data['content']['summary'].get(i).get('rate')
        item['shop_name'] = shop_name
        item['type'] = 'shouhoufenxi'
        item['date'] = datas['date']
        yield item

    def insert_into_table(self,items):
        for item in items:
            if item:
                if item['type'] == 'hexinzhibiao':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['hexinzhibiao'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'liulianglaiyuan':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))

                    insert_table = self.table['liulianglaiyuan'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'dingdanmingxi':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['dingdanmingxi'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'kehushuju':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['kehushuju'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'shouhoufenxi':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['shouhoufenxi'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'jiaoyitezheng':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['jiaoyitezheng'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'liulianggaikuo':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['liulianggaikuo'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'jiaoyigaikuang':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['jiaoyigaikuang'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'shangpingaikuang':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['shangpingaikuang'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()
                elif item['type'] == 'shangpinmingxi':
                    conn = engine.connect()
                    item['id'] = None
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    insert_table = self.table['shangpinmingxi'].insert().prefix_with('IGNORE')
                    conn.execute(insert_table, **item)
                    conn.close()


    def Orders_client(self, datas):
        # 下单客户分析
        '''
        potCustNum:潜在客户
        visitCustNum:访客数
        orderCustNum：下单客户
        client_type:客户类型,Orders_client:下单客户数,Orders_client_rate:下单客户数对比
        Orders_rate：下单客户数占比，Orders_rate_contrast：下单客户数占比对比，upt：客单量
        upt_rate：客单量对比，Guest_piece：客单件数，Guest_piece_rate：客单件数对比，
        payPct：客单价，payPct_rate：客单价对比
        '''
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'kehushuju'
                item['date'] = '访问受限'
                yield item
                return
        # 客户数据
        client_data = data['content']['info']
        # print client_data
        # 客户类型
        # print data
        field_list = ['client_type', 'Orders_client', 'Orders_client_rate', 'Orders_rate', 'Orders_rate_contrast',
                      'upt', 'upt_rate', 'Guest_piece', 'Guest_piece_rate', 'payPct', 'payPct_rate']
        for i in data['content']['list']['data']:
            if i[0] == 1:
                i[0] = u'全部下单客户'
            elif i[0] == 0:
                i[0] = u'新下单客户'
            else:
                i[0] = u'全部下单客户'
            i = i
            item = dict(zip(field_list, i))
            for key in item:
                if key in ['Orders_rate', 'Guest_piece_rate', 'upt_rate', 'Orders_client_rate', 'Orders_rate_contrast',
                           'payPct_rate'] and item[key]:
                    item[key] = "%.2f%%" % (item[key] * 100)
            item['shop_name'] = shop_name
            item['type'] = 'kehushuju'
            item['date'] = datas['date']
            #           print item
            yield item

    def Core_KPI(self, datas):
        # 核心指标
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'hexinzhibiao'
                item['date'] = '访问受限'
                yield item
                return
        item = {}
        data = data['content']['summary']
        # print data
        # 下单金额
        item['Orders_sum'] = data['OrdAmt']['value']
        # 下单金额无线占比
        item['Orders_rate'] = '%.2f%%' % (data['OrdAmt']['MobileRate'] * 100)
        # 较前一天
        item['OrdersRate'] = '%.2f%%' % (data['OrdAmt']['ComYesterdayRate'] * 100)
        # 浏览量
        item['PV'] = data['PV']['value']
        # 浏览量无线占比
        item['PV_rate'] = '%.2f%%' % (data['PV']['MobileRate'] * 100)
        # 较前一天
        item['PVRate'] = '%.2f%%' % (data['PV']['ComYesterdayRate'] * 100)
        # 访客数
        item['UV'] = data['UV']['value']
        # 访客数无线占比
        item['UV_rate'] = '%.2f%%' % (data['UV']['MobileRate'] * 100)
        # 较前一天
        item['UVRate'] = '%.2f%%' % (data['UV']['ComYesterdayRate'] * 100)
        # 客单价
        item['CustPriceAvg'] = data['CustPriceAvg']['value']
        # 客单价无线客单
        item['CustPriceAvg_Price'] = data['CustPriceAvg']['MobileCustPrice']
        # 较前一天
        item['CustPriceAvg_rate'] = '%.2f%%' % (data['CustPriceAvg']['ComYesterdayRate'] * 100)
        # 下单转化率
        item['CustRate'] = '%.2f%%' % (data['CustRate']['value'] * 100)
        # 下单转化无线转化
        item['Cust_wireless_rate'] = '%.2f%%' % (data['CustRate']['MobileCustRate'] * 100)
        # 较前一天
        item['Cust_rate'] = '%.2f%%' % (data['CustRate']['ComYesterdayRate'] * 100)
        # 90天重复购买率
        item['The90'] = '%.2f%%' % (data['The90RepeatPurchaseRate']['value'] * 100)
        # 90天重复购买率APP渠道占比
        item['The90Rate'] = '%.2f%%' % (data['The90RepeatPurchaseRate']['AppCustRate'] * 100)
        # 较前一天
        item['The90_rate'] = '%.2f%%' % (data['The90RepeatPurchaseRate']['ComYesterdayRate'] * 100)
        # 30天重复购买率
        item['The30'] = '%.2f%%' % (data['The30RepeatPurchaseRate']['value'] * 100)
        # 30天重复购买率APP渠道占比
        item['The30Rate'] = '%.2f%%' % (data['The30RepeatPurchaseRate']['AppCustRate'] * 100)
        # 较前一天
        item['The30_rate'] = '%.2f%%' % (data['The30RepeatPurchaseRate']['ComYesterdayRate'] * 100)
        # 店铺关注人数
        item['ShopCollectNum'] = data['ShopCollectNum']['value']
        # 店铺关注人数APP渠道
        item['App_population'] = data['ShopCollectNum']['AppCustNum']
        # 较前一天
        item['ShopCollectNum_rate'] = '%.2f%%' % (data['ShopCollectNum']['ComYesterdayRate'] * 100)
        item['shop_name'] = shop_name
        item['type'] = 'hexinzhibiao'
        item['date'] = datas['date']
        yield item

    def flow_source(self, datas):
        # 流量来源
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'liulianglaiyuan'
                item['date'] = '访问受限'
                yield item
                return
        source = datas['source']
        field_list = ['source_type', 'shop_UV', 'peer_UV', 'shop_CustRate', 'peer_CustRate', 'source']
        # print source
        for i in data['content']['flowSource']['data']:
            i.append(source)
            item = dict(zip(field_list, i))
            for key in item:
                if key in ['shop_CustRate', 'peer_CustRate']:
                    item[key] = '%.2f%%' % (item[key] * 100)
            item['shop_name'] = shop_name
            item['type'] = 'liulianglaiyuan'
            item['date'] = datas['date']
            yield item

    def order_details(self, datas):
        # 订单明细
        '''
        OrderID:订单号，source：订单来源,title:商品名称，raw_money优惠前金额,commodity_count:下单商品件数
        coupon:优惠金额,order_amount:订单金额,freight:运费,cover_charge:服务费,Order_time:下单时间
        paytime:付款时间,Payment:付款方式

        '''
        field_list = ['OrderID', 'source', 'title', 'raw_money', 'commodity_count', 'coupon', 'order_amount', 'freight',
                      'cover_charge', 'Order_time', 'paytime', 'Payment']
        shop_name = datas['shop_name']
        try:
            data = json.loads(datas['data'])
        except Exception as e:
            if '访问受限' in datas['data']:
                item={}
                item['shop_name'] = shop_name
                item['type'] = 'dingdanmingxi'
                item['date'] = '访问受限'
                yield item
                return

        for i in data['content']['data']:
            item = dict(zip(field_list, i[0:-2]))
            item['shop_name'] = shop_name
            item['type'] = 'dingdanmingxi'
            item['date'] = datas['date']
            # print item
            yield item


pa = parses()

engine = sqlalchemy.create_engine(
    'mysql+mysqldb://writer:hh$writer@10.15.1.24:3306/hillinsight?charset=utf8',
    connect_args={'charset': 'utf8'})
for line in sys.stdin:
    if not line.strip():
        continue
    data=json.loads(line)
    cate = json.loads(line)['cate']
    if parses_dict.get(cate):
        items = list(apply(getattr(pa, parses_dict.get(cate)), (data,)))
        pa.insert_into_table(items)
