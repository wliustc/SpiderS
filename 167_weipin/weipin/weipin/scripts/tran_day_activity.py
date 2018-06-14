# coding=utf8
'''解析-女鞋和运动-唯品会档期-档期详情-下半部分-每天跑昨天增量'''
import sys
import json
import web
import datetime

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                  host='10.15.1.24')

#nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def parse(line):
    json_line = json.loads(line)
    meta = json_line.get('meta')
    content = json_line.get('content')
    brand = meta.get('brand')
    firstSellDay = meta.get('firstSellDay')
    lastSellDay = meta.get('lastSellDay')
    updateTime = meta.get('updateTime')
    brandType = meta.get('brandType')
    brandName = meta.get('brandName')
    dt = meta.get('dt')
    content_json = json.loads(content)
    singleResult = content_json.get('singleResult')
    if singleResult:
        chart = singleResult.get("chart")
        data = chart.get("data")
        sales = data.get("sales")
        goodsCnt = data.get("goodsCnt")
        goodsActureAmt = data.get("goodsActureAmt")
        flowUv = data.get("flowUv")
        flowConversion = data.get("flowConversion")
        orderCnt = data.get("orderCnt")
        consumerCount = data.get("consumerCount")
        avgUserSalesAmount = data.get("avgUserSalesAmount")
        couponAmt = data.get("couponAmt")
        stockAmtOnline = data.get("stockAmtOnline")
        for a,b,c,d,e,f,g,h,i,j in zip(sales,goodsCnt,goodsActureAmt,flowUv,flowConversion,orderCnt,consumerCount,avgUserSalesAmount,couponAmt,stockAmtOnline):
            for k, l, m, n, o, p, q, r, s, t in zip(a, b, c, d, e, f, g, h, i, j):
                result = {}
                result['brand'] = brand
                result['brandType'] = brandType
                result['brandName'] = brandName
                result['firstSellDay'] = firstSellDay
                result['lastSellDay'] = lastSellDay
                result['updateTime'] = updateTime
                result['dt'] = dt
                result['activatyDay'] = k.get('x')
                result['sales'] = k.get('y')
                result['goodsCnt'] = l.get('y')
                result['goodsActureAmt'] = m.get('y')
                result['flowUv'] = n.get('y')
                result['flowConversion'] = o.get('y')
                result['orderCnt'] = p.get('y')
                result['consumerCount'] = q.get('y')
                result['avgUserSalesAmount'] = r.get('y')
                result['couponAmt'] = s.get('y')
                result['stockAmtOnline'] = t.get('y')

                print result
                db.insert('t_spider_belle_weipin_details_history_every', **result)


for line in sys.stdin:
    try:
        # print line
        parse(line)
        # pass
    except Exception, e:
        pass


