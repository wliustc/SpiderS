# coding=utf8

import sys

import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')
brand_count=24
category_type_dic = {
    u'交易': 'p_overview',
    u'流量构成': 'p_flow_structure',
    u'交易总览': 'p_trading_overview',
    u'商品效果': 'p_items_effect_detail',
    u'评价内容分析': 'p_evaluation_analysis',
    u'维权总览': 'p_claim',
    u'流量来源无线': 'p_flow_source',
    u'流量来源PC': 'p_flow_source',
    u'天猫日报缺失': 'p_tmall_deficiency'
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
    u'新访客数': 'newUv',
    u'老访客数':'oldUv',
    u'支付子订单数':'pay_num',
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


class ParseAll(object):
    def __init__(self):
        pass

    # 交易
    def p_overview(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = item_json.get('data')
        if data:
            title = data.get('title')
            data_list = data.get('data')
            if data:
                result['cate'] = cate
                for data in data_list:
                    # print title
                    for index, tt in enumerate(title):
                        if tt == u'统计日期':
                            result['select_date_begin'] = data[index]
                            result['select_date_end'] = data[index]
                        else:
                            result[overview_dic.get(tt)] = data[index]
                    try:
                        db.insert('t_spider_sycm_staccato_overview', **result)
                        pass
                    except Exception, e:
                        print e

    # 流量构成
    def p_flow_structure(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        data = item_json.get('data')
        result['cate'] = cate
        if data:
            title = data.get('title')
            data_list = data.get('data')
            if data:
                result['cate'] = cate
                for data in data_list:
                    # print title
                    for index, tt in enumerate(title):
                        if tt == u'统计日期':
                            result['select_date_begin'] = data[index]
                            result['select_date_end'] = data[index]
                        else:
                            result[flow_structure_dic.get(tt)] = data[index]
                    try:
                        db.insert('t_spider_sycm_staccato_flow_structure', **result)
                        # print result
                        pass
                    except Exception, e:
                        print e

    # 交易总览
    def p_trading_overview(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        month = meta.get('month')
        # print item_json
        data = item_json.get('data')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        result['cate'] = cate
        if data:
            for key, val in data.items():
                result[key] = val
            try:
                db.insert('t_spider_sycm_staccato_trading_overview', **result)
                pass
            except Exception, e:
                print e

    # 商品效果
    def p_items_effect_detail(self, item):
        global sign, dt
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        month = meta.get('month')
        data = item_json.get('data')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        result['cate'] = cate
        if data:
            data = data.get('data')
            if data:
                for d in data:
                    # result['itemId'] = d.get('itemId')
                    itemModel = d.get('itemModel')
                    for key, val in itemModel.items():
                        result[key] = val
                    itemEffectIndex = d.get('itemEffectIndex')
                    for key, val in itemEffectIndex.items():
                        result[key] = val
                    # print result
                    try:
                        # print result
                        pass
                        sign = 1
                        db.insert('t_spider_sycm_staccato_items_effect', **result)

                    except Exception, e:
                        print e

    # 评价内容分析
    def p_evaluation_analysis(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        imprEmotion = meta.get('imprEmotion')
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        month = meta.get('month')
        # print item_json
        data = item_json.get('data')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        result['cate'] = cate
        result['imprEmotion'] = imprEmotion
        if data:
            for key, val in data.items():
                content_list = val.get('keywords')
                if content_list:
                    result['category_name'] = evaluation_analysis_dic.get(key)
                    result['category_value'] = val.get('value')
                    result['category_ratio'] = val.get('ratio')
                    result_dic = {}
                    for content in content_list:
                        reviewCnt = content.get('reviewCnt')
                        name = content.get('name')
                        if result_dic.get(name):
                            # print reviewCnt
                            result_dic[name] = int(result_dic.get(name)) + int(reviewCnt)
                        else:
                            result_dic[name] = reviewCnt
                    for key1, val1 in result_dic.items():
                        try:
                            result['reviewCnt'] = val1
                            result['name'] = key1
                            # print result
                            db.insert('t_spider_sycm_staccato_imprEmotion', **result)
                        except Exception, e:
                            print e

    # 维权总览
    def p_claim(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        brand = meta.get('brand')
        result['brand'] = brand
        month = meta.get('month')
        # print item_json
        data = item_json.get('data')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        result['cate'] = cate
        if data:
            val_list = ['statDate', 'after_svr_rank_rate_1d_001']
            val_cyc_list = ['svrRankExceedRate']
            for key, val in data.items():
                if key in val_list:
                    result[key] = val.get('value')
                elif key in val_cyc_list:
                    result[key] = val.get('value')
                    result[key + 'cycleCrc'] = val.get('cycleCrc')
                else:
                    result[key] = val.get('value')
                    result[key + 'CycleCrc'] = val.get('cycleCrc')
                    result[key + 'RivalAvg'] = val.get('rivalAvg')
            try:
                db.insert('t_spider_sycm_staccato_claim', **result)
                print

            except Exception, e:
                print e

    # 流量来源1
    def p_flow_source1(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        data = item_json.get('data')
        result['cate'] = cate
        brand = meta.get('brand')
        result['brand'] = brand
        result['device'] = meta.get('device')
        if data:
            val_cyc_list = ['uv', 'crtByrCnt', 'crtRate']

            for d in data:
                for key, val in d.items():
                    if key in 'statDate':
                        result['statDate'] = val.get('value')
                    elif key in val_cyc_list:
                        result[key] = val.get('value')
                        result[key + 'CycleCrc'] = val.get('cycleCrc')
                    else:
                        result[key] = val
                try:
                    db.insert('t_spider_sycm_staccato_flow_source', **result)
                    # print result
                    pass

                except Exception, e:
                    print e

    # 流量来源
    def p_flow_source(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        data = item_json.get('data')
        result['cate'] = cate
        brand = meta.get('brand')
        result['brand'] = brand
        result['device'] = meta.get('device')
        if data:
            val_cyc_list = ['uv', 'payByrCnt', 'payRate', 'payAmt',
                            'uvValue', 'crtVldAmt', 'payPct', 'crtByrCnt',
                            'crtRate']
            val_list = ['pPageId', 'pageName', 'pageId', 'pageLevel', 'childPageType']
            children_list = ['children']
            for d in data:
                for key, val in d.items():

                    if key in val_cyc_list:
                        result[key] = val.get('value')
                        result[key + 'CycleCrc'] = val.get('cycleCrc')
                    elif key in val_list:
                        result[key] = val.get('value')

                try:
                    db.insert('t_spider_sycm_staccato_flow_source', **result)
                    # print result
                    pass
                except Exception, e:
                    print e

                # print type(d)
                children = d.get('children')
                # print children
                if children:
                    for child in children:
                        for key_child, val_child in child.items():
                            if key_child in val_cyc_list:
                                result[key_child] = val_child.get('value')
                                result[key_child + 'CycleCrc'] = val_child.get('cycleCrc')
                            elif key_child in val_list:
                                result[key_child] = val_child.get('value')
                        try:
                            db.insert('t_spider_sycm_staccato_flow_source', **result)
                            # print result

                            pass

                        except Exception, e:
                            print e

    def p_tmall_deficiency(self, item):
        result = {}
        item_json = json.loads(item)
        content = item_json.get('content')
        meta = item_json.get('meta')
        dt = item_json.get('dt')
        month = meta.get('month')
        result['dt'] = dt
        item_json = json.loads(content)
        cate = meta.get('cate')
        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        data = item_json.get('data')
        result['cate'] = cate
        brand = meta.get('brand')
        result['brand'] = brand
        if data:
            title = data.get('title')
            data_list = data.get('data')
            if data:
                result['cate'] = cate
                for data in data_list:
                    for index, tt in enumerate(title):
                        # print data[index]
                        if tt == u'统计日期':
                            result['select_date_begin'] = data[index]
                            result['select_date_end'] = data[index]
                        else:
                            result[tmall_deficiency_dic.get(tt)] = data[index]
                    try:
                        db.insert('t_spider_sycm_staccato_tmall_deficiency', **result)
                        pass
                    except Exception, e:
                        print e

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

if sign:
    data = db.query("select distinct brand from t_spider_sycm_staccato_overview where dt='%s';" % dt)
    data2 = db.query("select distinct brand from t_spider_sycm_staccato_claim where dt='%s';" % dt)
    if len(data) == brand_count and len(data2) == brand_count:
        db.query('insert into t_spider_table_sign(dt,sign,spider_name) value ("%s","%s","%s")' % (dt, "1", "all_brand"))

    
    
    
    
    