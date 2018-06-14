# coding=utf8
import sys
import json
import MySQLdb
import web
import datetime
import traceback
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#now = '2018-03-03'
for line in sys.stdin:
    try:
        items = json.loads(line)
        if items['priceText'] == []:
            items['priceText'] = ''
        items['origin_data'] = str(items['origin_data'])
        db.insert('t_spider_dianping_food', **items)
    except:
        traceback.print_exc()