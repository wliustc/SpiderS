# -*- coding: utf-8 -*-
# coding:utf8
import sys
import json
import web

reload(sys)
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')




def from_parse(dd):
    dd = json.loads(dd)
    try:
        db.insert('t_hh_dianping_shop_comments_pet_all', **dd)
    except Exception as e:
        print e


for line in sys.stdin:
    from_parse(line)








    
    