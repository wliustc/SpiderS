import sys
import web
import json
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
def process(item):
    items = json.loads(item)
    try:
        db.insert('t_xsd_black_bird_activity',**items)
    except Exception as e:
        print e

for line in sys.stdin:
    process(line)
    