# coding=utf8
'''解析-女鞋-唯品会-档期-档期分析-流量分析-档期流量入口分布-本档期'''
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
        chart = singleResult.get('chart')
        if chart:
            data = chart.get('data')
            contrastScale = chart.get('contrastScale')
            if data:
                flowUv = data.get('flowUv')
                for a in flowUv:
                    for i,j in zip(contrastScale,a):
                        result = {}
                        result['brand'] = brand
                        result['brandType'] = brandType
                        result['brandName'] = brandName
                        result['firstSellDay'] = firstSellDay
                        result['lastSellDay'] = lastSellDay
                        result['updateTime'] = nowTime
                        result['dt'] = dt
                        result['name'] = i
                        result['num'] = j.get('y')
                        result['percentage'] = j.get('ratio')

                        print result
                        db.insert('t_spider_dangqi_dangqifenxi_liuliang', **result)

for line in sys.stdin:
    try:
        # print line
        parse(line)
        # pass
    except Exception, e:
        pass

    