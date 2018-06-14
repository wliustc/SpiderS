#coding:utf8


import web
import json
import sys

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

for line in sys.stdin:
    item = json.loads(line)
    try:
        db.insert('t_spider_airui_index', **item)
    except Exception as e:
        print e, '#WWW'
    