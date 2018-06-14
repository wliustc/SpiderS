# coding=utf8

import sys,json,web
reload(sys)
sys.setdefaultencoding('utf-8')
import time
brand_count = 24
sku_columns = [
    'skuPayAmt',
    'skuPayItemQty',
    'skuName',
    'skuId',
    'skuPrice',
    'skuStock',
    'skuNewAddCartItemCnt',
    'skuAvgPayPrice',
    'skuPayBuyerCnt',
    'skuOrderBuyerCnt',
    'skuOrderAmt',
    'skuOrderItemQty'
]
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                  host='10.15.1.24')

data_table = 't_spider_sycm_staccato_items_sku'


dt = ''
sign = 0

def insert_ali(ll):
    try:
        db.insert(data_table, **ll)
    except Exception, e:
        print e


def parse(line):
    global sign, dt
    line_json = json.loads(line)
    meta = line_json.get('meta')
    # print line
    cate = meta.get('cate')
    goods_id = meta.get('goods_id')
    brand = meta.get('brand')
    content = line_json.get('content')
    dt = line_json.get('dt')
    data_dt = line_json.get('data_dt')
    if content:
        content_json = json.loads(content)
        if content_json:
            data = content_json.get('data')
            if data:
                data = data.get('data')
                if data:
                    for d in data:
                        if d:
                            result = {}
                            for key_d,val_d in d.items():
                                if key_d in sku_columns:
                                    result[key_d] = val_d
                            result['dt'] = dt
                            result['cate'] = cate
                            result['goods_id'] = goods_id
                            result['brand'] = brand
                            result['data_dt'] = data_dt
                            sign = 1
                            insert_ali(result)




for line in sys.stdin:
    parse(line)
    
if sign:
    data = db.query("select distinct brand from t_spider_sycm_staccato_items_sku where dt='%s';" % dt)
    if len(data) == brand_count:
        db.query('insert into t_spider_table_sign(dt,sign,spider_name) value ("%s","%s","%s")' % (dt, "1", "all_brand_sku"))

    
    
    
    
    
    
    
    