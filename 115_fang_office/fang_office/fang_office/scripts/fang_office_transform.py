import sys
import json
import MySQLdb
import web
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
dbo2o = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

for line in sys.stdin:
    # print line
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
        sql = "INSERT INTO t_hh_office_building_source_info(%s) VALUES(%s)" % (key_str, value_str)
        # sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
        dbo2o.query(sql)

    except Exception,e:
        print e
        pass

    