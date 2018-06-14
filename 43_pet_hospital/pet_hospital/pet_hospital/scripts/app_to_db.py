#encoding=utf-8

import sys
import json
import MySQLdb
conn = MySQLdb.connect(host="10.15.1.14",port=3306,user="work",passwd="phkAmwrF",db="hillinsight",charset="utf8")
cursor = conn.cursor()
conn1 = MySQLdb.connect(host="10.15.1.24",port=3306,user="writer",passwd="hh$writer",db="hillinsight",charset="utf8")
cursor1 = conn1.cursor()

for line in sys.stdin:
    row = line.strip()
    data = json.loads(row)
    #del data['_target_table']
    cols,args = zip(*data.iteritems())
    table = ""
    if 'loss_num' in cols:
        table = "t_app_pet_hospital_traffic_data"
    elif "source_name" in cols:
        table = "t_app_pet_hospital_traffic_data_source"
    elif "click_module" in cols:
        table = "t_app_pet_hospital_merchantpage_click_info"
    sql = 'replace into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['%s' for i in range(len(cols))]))
    print sql
    try:
        cursor.execute(sql, args)
        conn.commit()
        cursor1.execute(sql, args)
        conn1.commit()
    except:
        if conn:
            conn.close()
        if conn1:
            conn1.close()
conn.close()
conn1.close()

    
    
    
    
    
    
    