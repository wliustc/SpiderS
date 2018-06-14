# coding:utf-8

import json
import web
import time
import sys

# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



for line in sys.stdin:
    item = json.loads(line)
    try:
        db.insert('t_xsd_amap_EyeHospital', **item)
    except Exception as e:
        print e




    