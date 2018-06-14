# coding=utf8

import sys

import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')
brand_count = 24
category_type_dic = {
    u'交易': 'p_overview',

}

device_dict = {
    '0': '所有终端',
    '1': 'PC端',
    '2': '无线端',
}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')

overview_dic = {
    u'新访客数': 'newUv',
    u'老访客数': 'oldUv',
    u'支付子订单数':'pay_num',
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
                        print result
                        db.insert('t_spider_sycm_staccato_new_old_uv', **result)
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

    