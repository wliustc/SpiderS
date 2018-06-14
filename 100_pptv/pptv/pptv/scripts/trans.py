import sys
import web
import json

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

def process(item):
    items = json.loads(item)
    try:
        db.insert('t_xsd_pptv',**items)
    except Exception as e:
       	print e

for line in sys.stdin:
    process(line)
    