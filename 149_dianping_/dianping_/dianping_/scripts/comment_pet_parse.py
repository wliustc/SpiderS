# -*- coding: utf-8 -*-
# coding:utf8
import sys
import json
import web

reload(sys)
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#delete_sql = '''DELETE FROM o2o.t_hh_dianping_shop_comments WHERE shop_id in (SELECT distinct dianping_id as shop_id FROM pet_cloud.hospital_base_information WHERE dianping_id is not null and dianping_id!=0)'''
#delete_sql = '''DELETE FROM t_hh_dianping_shop_comments_pet WHERE dt='2018-03-30' '''
#db.query(delete_sql)



def from_parse(dd):
    dd = json.loads(dd)
    try:
        db.insert('t_hh_dianping_shop_comments_pet', **dd)
        dd.pop('dt')
        db.insert('t_hh_dianping_shop_comments', **dd)


    except Exception as e:
        print e


for line in sys.stdin:
    from_parse(line)








    
    
    
    
    
    