# coding=utf8
import sys
import json
import MySQLdb
import web
import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306, host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')
now = datetime.datetime.now().strftime('%Y-%m-%d')
#now = '2018-03-03'
for line in sys.stdin:
    try:
        items = json.loads(line)
        db.insert('t_spider_vip_realtime', **items)
    except:
        pass