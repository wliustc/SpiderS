import json
import web
import sys


# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def baidu_(i):
        # item = json.loads(i)
        try:
            db.insert('t_xsd_dianping_lianpinpuzi', **i)
        except Exception as e:
            print e





for line in sys.stdin:
    baidu_(json.loads(line))