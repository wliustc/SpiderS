#encoding=utf-8

import sys
import json
import MySQLdb
conn = MySQLdb.connect(host="10.15.1.24",port=3306,user="work",passwd="phkAmwrF",db="hillinsight",charset="utf8")
cursor = conn.cursor()

for line in sys.stdin:
    row = line.strip()
    data = json.loads(row)
    del data['_target_table']
    cols,args = zip(*data.iteritems())
    table = ""
    if 'loss_num' in cols:
        table = "t_hh_pet_hospital_traffic_data"
    elif "source_name" in cols:
        table = "t_hh_pet_hospital_traffic_data_source"
    elif "click_module" in cols:
        table = "t_hh_pet_hospital_merchantpage_click_info"
    sql = 'replace into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['%s' for i in range(len(cols))]))
    print sql
    try:
        cursor.execute(sql, args)
        conn.commit()
    except:
        if conn:
            conn.close()
conn.close()

    
    