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
    u'评价概况':'p_evaluate',
}

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')

class ParseAll(object):
    def __init__(self):
        pass

    def p_evaluate(self, item):
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
            itemDsr = data.get('itemDsr')
            logisticsDsr = data.get('logisticsDsr')
            serviceDsr = data.get('serviceDsr')
            if itemDsr and logisticsDsr and serviceDsr:
                item_rivalAvgValue = itemDsr.get('rivalAvgValue')
                item_syncRate = itemDsr.get('syncRate')
                item_value = itemDsr.get('value')
                result['item_rivalAvgValue'] = str(item_rivalAvgValue)
                result['item_value'] = str(item_value)
                result['item_syncRate'] = str(item_syncRate)

                logistics_rivalAvgValue = logisticsDsr.get('rivalAvgValue')
                logistics_syncRate = logisticsDsr.get('syncRate')
                logistics_value = logisticsDsr.get('value')
                result['logistics_rivalAvgValue'] = str(logistics_rivalAvgValue)
                result['logistics_syncRate'] = str(logistics_syncRate)
                result['logistics_value'] = str(logistics_value)

                service_rivalAvgValue = serviceDsr.get('rivalAvgValue')
                service_syncRate = serviceDsr.get('syncRate')
                service_value = serviceDsr.get('value')
                result['service_rivalAvgValue'] = str(service_rivalAvgValue)
                result['service_syncRate'] = str(service_syncRate)
                result['service_value'] = str(service_value)


                result['cate'] = cate
                try:
                    print result
                    db.insert('t_spider_sycm_staccato_grade', **result)
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
    