import sys
import json
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = int(time.time())

def web_db_insert(data):
    db.insert('t_xsd_pptv_circle',**data)
for line in sys.stdin:
    line = json.loads(line)
	try:
       web_db_insert(line)
	except Exception,e:
       print e

    