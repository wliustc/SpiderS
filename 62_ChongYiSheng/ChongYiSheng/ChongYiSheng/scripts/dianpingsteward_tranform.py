import sys
import web
import json

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.24')
db_insert = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


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
    try:
        line_json = json.loads(line)
        
        if 'settlement_price' in line_json:
            db_insert.insert('test_ChongYiShengConsume', **line_json)
        elif 'calDate' in line_json:
            db_insert.insert('t_spider_ChongYiSheng_PV', **line_json)
        else:
            deal_id = line_json.get('dpDealGroupId')
            dphospital_list,dphospital_id = get_shop_list(deal_id)
            line_json['dphospital_id'] = dphospital_id
            line_json['dphospital_list'] = dphospital_list
            db_insert.insert('test_ChongYiShengBuy', **line_json)
    except:
        pass
    # print json.dumps(line_json)


# dd = {"dpSailedTipMsg": "", "processId": 28771853, "endDate": "2017-11-16", "mthospital_list": "", "mtDealGroupId": 42670845, "mthospital_name": "", "dphospital_id": 6124971, "ownerName": "\u738b\u51a0\u7ae5", "mtSailedNum": 189, "ownerTel": "13609832443", "channelStatus": 3, "title": "\u5ba0\u9890\u751f\u52a8\u7269\u533b\u9662\u6c88\u9633\u7231\u514b\u5a01\u5206\u9662(\u5ba0\u7269\u57fa\u7840\u4f53\u68c0\u5957\u9910)", "mtUrl": "http://www.meituan.com/deal/42670845.html", "brief": "", "buttons": "", "mthospital_id": "", "dphospital_name": "", "dpSailedTip": "", "dphospital_list": [{"6124971": "\u5ba0\u9890\u751f\u52a8\u7269\u533b\u9662(\u6c88\u9633\u7231\u514b\u5a01\u5206\u9662)"}], "status": 3, "outBizId": "", "mtSailedTip": "", "price": "39.00\u5143", "dpSailedNum": 112, "write_time": "2017-08-11 18:59:34", "merchantType": 5, "dpDealGroupId": 22357550, "mtSailedTipMsg": "", "endTip": "", "ownerId": 2104872, "dpUrl": "http://t.dianping.com/deal/22357550", "customerId": 40126992}
