# coding=utf8

import sys

import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')
brand_count = 24  # 一定需要改
category_type_dic = {
    # 添加方法，写函数
    u'支付子订单数': 'p_payOrderCnt',
    u'支付买家数': 'p_payBuyerCnt',
    u'访客数': 'p_uv',
    u'支付金额': 'p_payAmt',

}

device_dict = {
    '0': '所有终端',
    '1': 'PC端',
    '2': '无线端',
}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='o2o', user='root', pw='123456', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')

overview_dic = {
    u'支付金额': 'payAmt',
    u'客单价': 'payPct',
    u'支付转化率': 'payRate',
    u'支付商品件数': 'payItemQty',
    u'支付买家数': 'payBuyerCnt',
    u'老买家数占比': 'oldPayBuyerProportion',
    u'下单父订单数': 'orderParentIndentnum',
    u'支付父订单数': 'payParentIndentnum',
    u'下单转化率': 'orderRate',
    u'人均支付商品件数': 'avgPayItemCnt',
    u'浏览量': 'pv',
}

flow_structure_dic = {
    u'店铺收藏人数': 'shopFavCnt',
    u'商品收藏次数': 'itemFavCnt',
    u'人均浏览量（访问深度）': 'avgPv',
    u'人均停留时长(秒)': 'avgStayTime',
    u'访客数': 'uv',
    u'老访客数占比': 'oldUvProportion',
    u'商品详情页浏览量': 'itemDetailPv'
}

evaluation_analysis_dic = {
    'ppRatio': '性价比相关评价',
    'item': '商品相关评价',
    'package': '包装相关评价',
    'service': '服务相关评价',
    'logistics': '物流相关评价'
}

tmall_deficiency_dic = {
    u'老访客数': 'oldUv',
    u"店铺首页访客数": 'shopHomePageUv',
    u"店铺首页浏览量": 'shopHomePagePv',
    u"商品收藏人数": 'itemFavCnt',
    u"跳失率": 'hopRate',
    u"商品详情页访客数": 'itemDetailUv',
    u"被浏览商品数": 'beBroItemCnt',
    u"支付商品数": 'payItemQty',
    u"已发货父订单数": 'deliverGoodsParentIndentnum',
    u"售中申请退款金额": 'rfdApplyAmt',
    u"售中申请退款买家数": 'rfdApplyBuyerCnt',
}

sign = 0
dt = ''

index_dic ={
    '20': '20:00-20:59',
    '21': '21:00-21:59',
    '22': '22:00-22:59',
    '23': '23:00-23:59',
    '1': '1:00-1:59',
    '0': '0:00-0:59',
    '3': '3:00-3:59',
    '2': '2:00-2:59',
    '5': '5:00-5:59',
    '4': '4:00-4:59',
    '7': '7:00-7:59',
    '6': '6:00-6:59',
    '9': '9:00-9:59',
    '8': '8:00-8:59',
    '11': '11:00-11:59',
    '10': '10:00-10:59',
    '13': '13:00-13:59',
    '12': '12:00-12:59',
    '15': '15:00-15:59',
    '14': '14:00-14:59',
    '17': '17:00-17:59',
    '16': '16:00-16:59',
    '19': '19:00-19:59',
    '18': '18:00-18:59'
}

class ParseAll(object):
    def __init__(self):
        pass

    def p_payOrderCnt(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        json_obj = json.loads(content)
        # print json_obj
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = json_obj.get('data')

        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        if data:
            d = data.get('data')
            updateTime = data.get('updateTime')
            result['updateTime'] = updateTime
            period = d.get('period')
            if period:
                result['cate'] = cate
                for index, i in enumerate(period):

                    result['time_quantum'] = index_dic[str(index)]
                    result['num'] = i
                    try:
                        # print result
                        db.insert('t_spider_sycm_staccato_payOrderCnt', **result)
                    except Exception as e:
                        pass
    def p_payBuyerCnt(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        json_obj = json.loads(content)
        # print json_obj
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = json_obj.get('data')

        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        if data:
            d = data.get('data')
            updateTime = data.get('updateTime')
            result['updateTime'] = updateTime
            period = d.get('period')
            if period:
                result['cate'] = cate
                for index, i in enumerate(period):

                    result['time_quantum'] = index_dic[str(index)]
                    result['num'] = i
                    try:
                        # print result
                        db.insert('t_spider_sycm_staccato_payOrderCnt', **result)
                    except Exception as e:
                        pass
    def p_uv(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        json_obj = json.loads(content)
        # print json_obj
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = json_obj.get('data')

        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        if data:
            d = data.get('data')
            updateTime = data.get('updateTime')
            result['updateTime'] = updateTime
            period = d.get('period')
            if period:
                result['cate'] = cate
                for index, i in enumerate(period):

                    result['time_quantum'] = index_dic[str(index)]
                    result['num'] = i
                    try:
                        # print result
                        db.insert('t_spider_sycm_staccato_payOrderCnt', **result)
                    except Exception as e:
                        pass


    def p_payAmt(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        json_obj = json.loads(content)
        # print json_obj
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = json_obj.get('data')

        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        if data:
            d = data.get('data')
            updateTime = data.get('updateTime')
            result['updateTime'] = updateTime
            period = d.get('period')
            if period:
                result['cate'] = cate
                for index, i in enumerate(period):

                    result['time_quantum'] = index_dic[str(index)]
                    result['num'] = i
                    try:
                        # print result
                        db.insert('t_spider_sycm_staccato_payOrderCnt', **result)
                    except Exception as e:
                        pass


for line in sys.stdin:
    try:
        line_json = json.loads(line)
        meta = line_json.get('meta')
        content = line_json.get('content')
        cate = meta.get('cate')
        # print cate
        pa = ParseAll()
        if category_type_dic.get(cate):
            apply(getattr(pa, category_type_dic.get(cate)), (line,))
    except Exception, e:
        print e
        time.sleep(100)
    
    
    