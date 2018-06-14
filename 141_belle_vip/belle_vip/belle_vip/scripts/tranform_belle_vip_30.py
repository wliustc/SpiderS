# coding=utf8
import sys
import json
import web
import time

# db_hillinsight = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                  host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

temp_table = 't_spider_vip_compass_temp'
data_table = 't_spider_vip_compass'
spider_name = 'belle_sport_30'
sign_table = 't_spider_vip_sign'
brand_count = 15

belle_columns = [
    'warehouseName',
    'brandStoreName',
    'goodsPicUrl',
    'returnedAmountPct',
    'goodsCtr',
    'maxBrandId',
    'maxGoodsId',
    'rejectedAndReturnedPct',
    'vipshopPrice',
    'goodsName',
    'rejectedAndReturnedCnt',
    'goodsAmt',
    'conversion',
    'avgUserCnt',
    'sizeName',
    'brandGoodsAvgCtr',
    'onSaleStockAmt',
    'returnedAmt',
    'goodsUrl',
    'goodsCntWithoutReturn',
    'goodsMoney',
    'rejectedGoodsCnt',
    'optGroup',
    'avgGoodsCtr',
    'vendorName',
    'hotType',
    'rejectedAmt',
    'userCnt',
    'lv3Category',
    'goodsCnt',
    'brandStoreSn',
    'todayLeavingCnt',
    'logDate',
    'itemNo',
    'onSaleStockCnt',
    'goodsCode',
    'rejectedAmountPct',
    'rejectedAndReturnedAmt',
    'vendorCode',
    'avgUv',
    'sellingRatio',
    'returnedGoodsCnt',
    'uv',
    'brandName',
    'collectUserCnt',
    'todayLeavingAmt',
    'avgCollectUserCnt',
    'goodsAmtWithoutReturn',
    'avgConversion',
    'dt',
    'orderGoodsPrice',
    'goodsActureAmt'
]


def insert_ali(ll):
    try:
        db.multiple_insert('t_spider_vip_compass_temp', ll)
        # db_hillinsight.insert('t_spider_vip_compass', **ll)
    except Exception, e:
        print e


def parse(line):
    global sign
    global dt
    ll_ali = []
    json_line = json.loads(line)
    meta = json_line.get('meta')
    content = json_line.get('content')
    dt = meta.get('dt')
    brand = meta.get('brand')
    content_json = json.loads(content)
    singleResult = content_json.get('singleResult')
    if singleResult:
        list = singleResult.get('list')

        if list:
            sign = 1
            pass
            for ll in list:
                ll['brandStoreName'] = brand
                ll['dt'] = dt
                result = {}
                for key_ll, val_ll in ll.items():
                    if key_ll in belle_columns:
                        result[key_ll] = val_ll
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


                # db.insert('t_spider_vip_compass', **content_json)


for line in sys.stdin:
    try:
        # print line
        parse(line)
        # pass
    except Exception, e:
        pass

if sign:
    # if 1:
    data_brand = db.query('select distinct brandStoreName from %s;' % temp_table)
    if len(data_brand) == brand_count:
        data = db.query('select min(logDate) as min_log_date,max(logDate) as max_log_date from %s;' % temp_table)
        if data:
            data = data[0]
            min_log_date = data.get('min_log_date')
            max_log_date = data.get('max_log_date')
            # print min_log_date
            db.query("delete from %s where logDate BETWEEN '%s' AND '%s'" % (data_table, min_log_date, max_log_date))
            db.query('insert into %s select distinct * from %s;' % (data_table, temp_table))
            db.query('delete from %s;' % temp_table)
            sql = '''select * from(
            select logdate,brandStoreName,goodsCode,goodsname,lv3category,count(*),'t_spider_vip_compass' as tbl
            from t_spider_vip_compass
            where logdate>= date_sub(current_date,interval 31 day)
            group by logdate,brandStoreName,goodsCode,goodsname,lv3category
            having count(*)>1)q
            limit 100
            union all
            select the_date,brand,'' as goodsCode,'' as goodsname,''as lv3category,count(*),'t_spider_vip_whole_index' as tbl
            from t_spider_vip_whole_index
            group by the_date,brand
            having count(*)>1
            ;'''
            resutl = db.query(sql)
            if resutl:
                #db.query('delete from t_spider_vip_sign_run')
                pass
            else:
                db.query('insert into %s(logDate,dt,sign,spider_name,datetime1) value ("%s","%s","1","belle_30","%s");' % (
                    sign_table, min_log_date + ',' + max_log_date, dt,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

                db.query('delete from t_spider_vip_sign_run')








    
    