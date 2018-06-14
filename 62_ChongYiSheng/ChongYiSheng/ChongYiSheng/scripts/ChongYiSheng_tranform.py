import sys
import web
import json

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.24')


def get_shop_list(deal_id):
    data = db.query("select shop_id,shop_name from t_hh_dianping_shop_info where shop_id in (select distinct shop_id from t_hh_dianping_tuangou_deal_info where deal_id='%s' and dt=curdate());" % str(deal_id))
    if data:
        list_ = []
        dphospital_id = ''
        for d in data:
            item = {}
            item[d.get('shop_id')]=d.get('shop_name')
            list_.append(item)
            dphospital_id = d.get('shop_id')
        return json.dumps(list_),dphospital_id
    else:
        return '',''

for line in sys.stdin:
    line_json = json.loads(line)
    deal_id = line_json.get('dpDealGroupId')
    dphospital_list,dphospital_id = get_shop_list(deal_id)
    line_json['dphospital_id'] = dphospital_id
    line_json['dphospital_list'] = dphospital_list
    print json.dumps(line_json)

    