import sys

import time
import web
import json

db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def web_db_insert(data):
    try:
        db.insert('t_hh_dianping_tuangou_deal_info',**data)
    except:
        pass


for line in sys.stdin:
    try:
        line_json = json.loads(line)
        new_price = line_json.get('new_price')
        if not new_price:
            line_json['new_price'] = 0
        old_price = line_json.get('old_price')
        if not old_price or old_price == []:
            line_json['old_price'] = 0
        sales = line_json.get('sales')
        if not sales or sales == []:
            line_json['sales'] = 0
        if line_json.get('deal_id'):
            web_db_insert(line_json)
    except Exception,e:
        pass
    
    