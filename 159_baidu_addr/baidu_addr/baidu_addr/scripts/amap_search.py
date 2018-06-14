#coding:utf8
import web
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



def from_parse(dd):
    dd = json.loads(dd)
    try:
        db.insert('t_spider_amap_search', **dd)
        #db.insert('t_spider_amap_search_new',**dd)
    except Exception as e:
        print e


for line in sys.stdin:
    from_parse(line)

    
    
    