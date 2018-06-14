# coding=utf8
'''女鞋-唯品会档期-档期详情-一周'''
import sys
import json
import web
# db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
#                   host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                  host='10.15.1.24')

temp_table='t_spider_belle_weipin_details_week'

#测试
#temp_table='t_spider_belle_weipin_details_history_test'

belle_columns = [
    'updateTime',
    'orderCnt',
    'avgOrderAmount',
    'saleMode',
    'dangqiName',
    'userCnt',
    'dt',
    'dangqiId',
    'uvConvert',
    'salesAmount',
    'goodsActureAmt',
    'brand',
    'saleTimeFrom',
    'uv',
    'actItmUv',
    'payCnt',
    'saleTimeTo',
    'payByrCnt',
    'logDate',
    'goodsCnt',
]
def insert_ali(ll):
    try:
        db.multiple_insert(temp_table, ll)
    except Exception, e:
        print e

def parse(line):
    ll_ali = []
    json_line = json.loads(line)
    meta = json_line.get('meta')
    content = json_line.get('content')
    dt = meta.get('dt')
    brand = meta.get('brand')
    updateTime = meta.get('updateTime')
    #print updateTime
    content_json = json.loads(content)
    singleResult = content_json.get('singleResult')
    if singleResult:
        list = singleResult.get('list')
        if list:
            for ll in list:
                ll['brand'] = brand
                ll['dt'] = dt
                ll['updateTime'] = updateTime

                result = {}
                for key_all, val_all in ll.items():
                    if key_all in belle_columns:
                        result[key_all] = val_all

                if len(ll_ali) > 1000:

                    ll_ali.append(result)
                    insert_ali(ll_ali)
                    ll_ali = []
                else:
                    # print result
                    ll_ali.append(result)

            # print ll_ali
            if ll_ali:
                insert_ali(ll_ali)

for line in sys.stdin:
    try:
        # print line
        parse(line)
        # pass
    except Exception, e:
        pass
