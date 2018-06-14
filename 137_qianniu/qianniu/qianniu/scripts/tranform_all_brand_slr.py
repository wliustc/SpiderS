# coding=utf8
# 维权分析解析脚本
import sys

import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')
brand_count = 24



db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='o2o', user='root', pw='123456', port=3306, host='127.0.0.1')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')





# 维权分析
def parse(item):
    item_json = json.loads(item)
    content = item_json.get('content')
    meta = item_json.get('meta')
    dt = item_json.get('dt')
    catename = meta.get('catename')
    cateid = meta.get('cateid')
    brand = meta.get('brand')
    month = meta.get('month')
    # print month
    if content:
        data = content.get('data')
        for detail in data:
            # print detail
            result = {}
            item = detail.get('item')
            result['rfdSucAmt'] = detail.get('rfdSucAmt').get('value')
            result['payOrdCnt'] = detail.get('payOrdCnt').get('value')
            result['rfdSucCnt'] = detail.get('rfdSucCnt').get('value')
            result['payAmt'] = detail.get('payAmt').get('value')
            rfdReason = detail.get('rfdReason')
            itemId = item.get('itemId')
            result['itemId'] = itemId
            pictUrl = item.get('pictUrl')
            result['pictUrl'] = pictUrl
            detailUrl = item.get('detailUrl')
            result['detailUrl'] = detailUrl
            title = item.get('title')
            result['brand'] = brand
            result['title'] = title
            result['dt'] = dt
            result['catename'] = catename
            result['cateid'] = cateid
            result['rfdReason'] = json.dumps(rfdReason)
            result['select_date_begin'] = month[0]
            result['select_date_end'] = month[1]
            try:
                db.insert('t_spider_sycm_staccato_safeguard_legal_rights',**result)
            except:
                pass

for line in sys.stdin:
    try:
        parse(line)


    except Exception, e:
        print e

db.query('insert into t_spider_table_sign(spider_name,sign,dt) value("all_brand_slr","1","%s")' % time.strftime('%Y-%m-%d', time.localtime(time.time())))

    
    
    