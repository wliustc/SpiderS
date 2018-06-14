# coding=utf8
import sys
import json
import web

db_update = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def parse(line):
    line_json = json.loads(line)
    shop_id = line_json.get('shop_id')
    gaode_id = line_json.get('gede_id')
    db_update.query('update  set review_id=%s where amap_uid=%s' % (shop_id,gaode_id))


for line in sys.stdin:
    parse(line)