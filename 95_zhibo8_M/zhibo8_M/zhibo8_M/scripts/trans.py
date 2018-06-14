import sys
import json
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

for line in sys.stdin:
    line = json.loads(line)
    try:
        db.insert('t_xsd_pptv_circle', **line)
    except Exception,e:
        print e