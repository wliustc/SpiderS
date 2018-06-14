# coding=utf8
'''女鞋-唯品会-商品-商品详情-档期-分天查看-全部-昨天增量'''
import sys
import json
import web



db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,host='10.15.1.24')


# 女鞋
temp_table='t_spider_vip_compass_dangqi_history_new'
# 运动
#temp_table='t_spider_vip_compass_sport_dangqi_history'

belle_columns = [
    'logDate',
    'vendorCode',
    'vendorName',
    'brandStoreName',
    'brandStoreSn',
    'brandName',
    'optGroup',
    'warehouseName',
    'maxGoodsId',
    'maxBrandId',
    'todayLeavingCnt',
    'todayLeavingAmt',
    'goodsUrl',
    'goodsCode',
    'goodsName',
    'itemNo',
    'sizeName',
    'vipshopPrice',
    'goodsPicUrl',
    'lv3Category',
    'hotType',
    'orderGoodsPrice',
    'goodsActureAmt',
    'onSaleStockCnt',
    'onSaleStockAmt',
    'userCnt',
    'avgUserCnt',
    'goodsMoney',
    'goodsCnt',
    'goodsAmt',
    'goodsCntWithoutReturn',
    'goodsAmtWithoutReturn',
    'sellingRatio',
    'allStockCnt',
    'dt',
    'allStockAmt',
    'uv',
    'avgUv',
    'conversion',
    'avgConversion',
    'collectUserCnt',
    'avgCollectUserCnt',
    'goodsCtr',
    'avgGoodsCtr',
    'brandGoodsAvgCtr',
    'rejectedGoodsCnt',
    'rejectedAmountPct',
    'rejectedAmt',
    'returnedGoodsCnt',
    'returnedAmountPct',
    'returnedAmt',
    'rejectedAndReturnedCnt',
    'rejectedAndReturnedPct',
    'rejectedAndReturnedAmt'
]
def insert_ali(ll):
    try:
        db.multiple_insert(temp_table, ll)
        # db_hillinsight.insert('t_spider_vip_compass', **ll)
    except Exception, e:
        print e

def parse(line):
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
            for ll in list:
                ll['brandStoreName'] = brand
                ll['dt'] = dt
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

    
    