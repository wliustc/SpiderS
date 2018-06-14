# coding=utf8
import sys
import json
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def parse(line):
    json_line = json.loads(line)
    meta = json_line.get('meta')
    content = json_line.get('content')
    dt = meta.get('dt')
    brand = meta.get('brand')
    content_json = json.loads(content)
    singleResult = content_json.get('singleResult')
    if singleResult:
        list = singleResult.get('list')
        for ll in list:
            ll['brandStoreName'] = brand
            ll['dt'] = dt
            # ll['brandStoreName'] = brand.replace('\n', '')
            # print ll
            try:
                db.insert('t_spider_vip_compass', **ll)
            except Exception, e:
                print e

    # db.insert('t_spider_vip_compass', **content_json)

for line in sys.stdin:
    try:
        parse(line)
    except Exception,e:
        pass
    