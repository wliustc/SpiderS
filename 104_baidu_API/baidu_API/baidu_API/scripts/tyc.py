# coding:utf-8
# 百度jl解析
import json
import web
import sys


# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

def baidu_(i):
        # item = json.loads(i)
        try:
            db.insert('tyc_yake_new', **i)
        except Exception as e:
            print e
	    #try:
         #   sql = '''UPDATE sheet2 SET lat='{lat}',lng='{lng}',province='{province}',city='{city}',district='{district}',sign='{sign}' WHERE id='{id}' '''.format(
          #      lat=i['lat'],lng=i['lng'],province=i['province'],id=i['id'],city=i['city'],district=i['district'],sign='1'
           # )
            #db.query(sql)
        #except Exception as e:
         #   print e




for line in sys.stdin:
    baidu_(json.loads(line))


# with open(r'E:\baidu_amap\baidu.jl') as f:
#     for i in f.readlines():
#         baidu_(json.loads(i))










    
    
    