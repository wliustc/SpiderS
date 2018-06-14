# coding=utf8
'''解析-运动和女鞋唯品会实时商品 按档期排 按销售量排取TOP10'''
import sys
import json
import web
# db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
#                   host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                  host='10.15.1.24')


temp_table='t_spider_belle_goods_top'

belle_columns = [
    'goodsPicUrl',
    'goodsName',
    'vipshopPrice',
    'goodsStockCnt',
    'goodsStockAmt',
    'dayUv',
    'dayPv',
    'dayUserCnt',
    'dayGoodsCnt',
    'daySalesAmount',
    'dayAddcartCnt',
    'conversion',
    'sellingRatio',
    'dayUvCtr',
    'goodsUrl',
    'lv3Category',
    'dayActureAmt',
    'updateTime',
    'brand',
    'dt',
    'goodsCode',
    'firstSellDay',
    'lastSellDay',
    'brandType',
    'brandName',
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
    firstSellDay = meta.get('firstSellDay')
    lastSellDay = meta.get('lastSellDay')
    brandType = meta.get('brandType')
    brandName = meta.get('brandName')
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
                ll['firstSellDay'] = firstSellDay
                ll['lastSellDay'] = lastSellDay
                ll['brandType'] = brandType
                ll['brandName'] = brandName

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

    
    