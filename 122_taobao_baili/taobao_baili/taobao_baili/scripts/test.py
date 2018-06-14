    #coding:utf8

import sys
import time
import re
import json
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def tranform1(lin):
    lin = json.loads(lin)
    try:
        db.insert('t_spider_xianhua_id', **lin)
    except:
        pass
for i in sys.stdin:
    tranform1(i)
    
    
    
    