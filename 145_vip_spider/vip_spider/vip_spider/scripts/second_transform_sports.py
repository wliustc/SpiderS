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
        sql = "INSERT INTO t_spider_vip_flowEntrance_sport(%s) VALUES(%s)" % (key_str, value_str)
        sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
        db.query(sql)
    except:
        pass
now = datetime.datetime.now().strftime('%Y-%m-%d')
#now = '2018-03-01'
the_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
db.query('insert into t_spider_vip_sign(dt,sign,spider_name,datetime1) value ("{}","1","{}","{}");'.format(now, 'second_table_sports_spider', the_time))
    
    
    
    
    
    