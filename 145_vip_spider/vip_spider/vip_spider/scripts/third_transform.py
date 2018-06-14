# coding=utf8
import sys
import json
import MySQLdb
import web
import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

for line in sys.stdin:
    try:
        items = json.loads(line)
        key_str = ','.join('`%s`' % k for k in items.keys())
        value_str = ','.join(
            'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v) for v in
            items.values())
        kv_str = ','.join(
            "`%s`=%s" % (k, 'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v))
            for (k, v)
            in items.items())
        sql = "INSERT INTO t_spider_vip_avgOrder(%s) VALUES(%s)" % (key_str, value_str)
        sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
        db.query(sql)
        #now = datetime.datetime.now().strftime('%Y-%m-%d')
        #db.query('insert into t_spider_vip_sign(dt,sign,spider_name) value ("{}","1","{}");'.format(now, 'third_table_spider'))
    except:
        pass
now = datetime.datetime.now().strftime('%Y-%m-%d')
db.query('insert into t_spider_vip_sign(dt,sign,spider_name) value ("{}","1","{}");'.format(now, 'third_table_spider'))
    