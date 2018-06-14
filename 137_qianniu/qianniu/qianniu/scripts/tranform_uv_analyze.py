# coding=utf8

import sys

import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')
brand_count = 24
category_type_dic = {
    u'访客分析': 'p_uv_analyze'
}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')

sign = 0
dt = ''


class ParseAll(object):
    def __init__(self):
        pass

    # 访客分析
    def p_uv_analyze(self, item):
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
            customs = data.get('customs')
            if customs:
                for c in customs:
                    customs_uv = c.get('uv')
                    customs_orderBuyerCnt =c.get('orderBuyerCnt')
                    customs_orderRate = c.get('orderRate')
                    customs_ratio = c.get('ratio')
                    customs_name = c.get('name')
                    result['customs_uv'] = customs_uv
                    result['customs_orderBuyerCnt'] = customs_orderBuyerCnt
                    result['customs_orderRate'] = customs_orderRate
                    result['customs_ratio'] = customs_ratio
                    result['customs_name'] = customs_name
                    try:
                        print result
                        db.insert('t_spider_sycm_staccato_new_old_order', **result)
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

# if sign:
#     data = db.query("select distinct brand from t_spider_sycm_staccato_overview where dt='%s';" % dt)
#     data2 = db.query("select distinct brand from t_spider_sycm_staccato_claim where dt='%s';" % dt)
#     if len(data) == brand_count and len(data2) == brand_count:
#         db.query('insert into t_spider_table_sign(dt,sign,spider_name) value ("%s","%s","%s")' % (dt, "1", "all_brand"))

    