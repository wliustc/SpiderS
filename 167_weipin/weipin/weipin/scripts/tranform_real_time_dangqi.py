# coding=utf8
'''解析-女鞋和运动-实时-小时级数据'''
import sys
import json
import web
import datetime
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                  host='10.15.1.24')


nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def parse(line):
    json_line = json.loads(line)
    meta = json_line.get('meta')
    content = json_line.get('content')
    dt = meta.get('dt')
    brand = meta.get('brand')
    firstSellDay = meta.get('firstSellDay')
    lastSellDay = meta.get('lastSellDay')
    brandType = meta.get('brandType')
    brandName = meta.get('brandName')
    content_json = json.loads(content)
    singleResult = content_json.get('singleResult')
    if singleResult:
        sum_data = singleResult.get('sum_data')
        if sum_data:
            result = {}
            result['brand'] = brand
            result['dt'] = dt
            result['uv'] = sum_data.get('uv')
            result['salesAmount'] = sum_data.get('sales')
            result['goodsCnt'] = sum_data.get('salesAmount')
            result['updatetime'] = nowTime
            result['goodsActureAmt'] = sum_data.get('goodsActureAmt')
            result['orderCnt'] = sum_data.get('orderCnt')
            result['avgOrderAmount'] = sum_data.get('unitPrice')
            result['userCnt'] = sum_data.get('consumerCount')
            result['uvConvert'] = sum_data.get('conversion')
            result['saleTimeFrom'] = firstSellDay
            result['saleTimeTo'] = lastSellDay
            result['saleMode'] = brandType
            result['dangqiName'] = brandName
            db.insert('t_spider_belle_weipin_activity_details', **result)
            # print result
        chart = singleResult.get('chart')
        if chart:
            data = chart.get('data')
            if data:
                consumerCount= data.get('consumerCount')
                conversion = data.get('conversion')
                goodsActureAmt = data.get('goodsActureAmt')
                orderCnt = data.get('orderCnt')
                sales = data.get('sales')
                salesAmount = data.get('salesAmount')
                unitPrice = data.get('unitPrice')
                uv = data.get('uv')
                for a, b, c, d, e, f, g, h in zip(consumerCount, conversion, goodsActureAmt, orderCnt, sales, salesAmount,
                                                  unitPrice, uv):
                    for i, j, k, l, m, n, o, p in zip(a, b, c, d, e, f, g, h):
                        result = {}
                        result['brand'] = brand
                        result['brandType'] = brandType
                        result['brandName'] = brandName
                        result['firstSellDay'] = firstSellDay
                        result['lastSellDay'] = lastSellDay
                        result['updateTime'] = nowTime
                        result['dt'] = dt
                        result['activityTime'] = i.get('x')
                        result['consumerCount'] = i.get('y')
                        result['conversion'] = j.get('y')
                        result['goodsActureAmt'] = k.get('y')
                        result['orderCnt'] = l.get('y')
                        result['sales'] = m.get('y')
                        result['salesAmount'] = n.get('y')
                        result['unitPrice'] = o.get('y')
                        result['uv'] = p.get('y')
                        print result
                        db.insert('t_spider_belle_weipin_activity_dnagqi_harfhour', **result)

for line in sys.stdin:
    try:
        # print line
        parse(line)
        # pass
    except Exception, e:
        pass

    
    
    
    