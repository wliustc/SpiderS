import sys
import json
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
def mys(qd_dict):
    qd_dict = json.loads(qd_dict)
    try:
        db.insert('t_xsd_zhibo8', **qd_dict)
    except Exception as e:
        print e
        
for line in sys.stdin:
   	mys(line)

    
    
    
    