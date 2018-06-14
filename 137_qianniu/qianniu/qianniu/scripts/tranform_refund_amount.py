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
    u'首页整体看板':'p_overall',

}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')

class ParseAll(object):
    def __init__(self):
        pass

    def p_overall(self, item):
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
        data = json_obj.get('content')

        result['select_date_begin'] = month[0]
        result['select_date_end'] = month[1]
        if data:
            data_obj = data.get('data')
            if data_obj:
                result['statDate'] = str(data_obj.get('statDate'))
                uv = data_obj.get('uv')
                cartCnt = data_obj.get('cartCnt')
                payByrCnt = data_obj.get('payByrCnt')
                olderPayAmt = data_obj.get('olderPayAmt')
                cartByrCnt = data_obj.get('cartByrCnt')
                pv = data_obj.get('pv')
                payRate = data_obj.get('payRate')
                payOrdCnt = data_obj.get('payOrdCnt')
                payAmt = data_obj.get('payAmt')
                cltItmCnt = data_obj.get('cltItmCnt')
                rfdSucAmt = data_obj.get('rfdSucAmt')
                payPct = data_obj.get('payPct')
                payItmCnt = data_obj.get('payItmCnt')
                payOldByrCnt = data_obj.get('payOldByrCnt')
                tkExpendAmt=data_obj.get('tkExpendAmt')
                uv = uv.get('value')
                cartCnt = cartCnt.get('value')
                payByrCnt = payByrCnt.get('value')
                olderPayAmt = olderPayAmt.get('value')
                cartByrCnt = cartByrCnt.get('value')
                pv = pv.get('value')
                payRate = payRate.get('value')
                payOrdCnt = payOrdCnt.get('value')
                payAmt = payAmt.get('value')
                cltItmCnt = cltItmCnt.get('value')
                rfdSucAmt = rfdSucAmt.get('value')
                payPct = payPct.get('value')
                payItmCnt = payItmCnt.get('value')
                payOldByrCnt = payOldByrCnt.get('value')
                tkExpendAmt = tkExpendAmt.get('value')
                if uv:
                    result['uv'] = str(uv)
                if cartCnt:
                    result['cartCnt'] = str(cartCnt)
                if payByrCnt:
                    result['payByrCnt'] = str(payByrCnt)
                if olderPayAmt:
                    result['olderPayAmt'] = str(olderPayAmt)
                if cartByrCnt:
                    result['cartByrCnt'] = str(cartByrCnt)
                if pv:
                    result['pv'] = str(pv)
                if payRate:
                    result['payRate'] = str(payRate)
                if payOrdCnt:
                    result['payOrdCnt'] = str(payOrdCnt)
                if payAmt:
                    result['payAmt'] = str(payAmt)
                if cltItmCnt:
                    result['cltItmCnt'] = str(cltItmCnt)
                if rfdSucAmt:
                    result['rfdSucAmt'] = str(rfdSucAmt)
                if payPct:
                    result['payPct'] = str(payPct)
                if payItmCnt:
                    result['payItmCnt'] = str(payItmCnt)
                if payOldByrCnt:
                    result['payOldByrCnt'] = str(payOldByrCnt)
                if tkExpendAmt:
                    result['tkExpendAmt'] = str(tkExpendAmt)
                    result['cate'] = cate
                try:
                    db.insert('t_spider_sycm_staccato_zhengti', **result)
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
    
    
    
    