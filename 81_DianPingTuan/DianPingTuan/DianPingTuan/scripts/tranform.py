import sys
import json
import web

db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

for line in sys.stdin:
    try:
        json_line = json.loads(line)
        
        res = db.insert('t_hh_dianping_shop_comments_test_tmp', **json_line)
        print line
    except Exception,e:
        pass