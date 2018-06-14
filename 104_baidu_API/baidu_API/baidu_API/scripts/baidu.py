# coding:utf-8
# 百度jl解析
import json
import web
import time
import sys
import MySQLdb

# db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')
#db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


# times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# with open(r'E:\gongs_\baidu_js\beijing.jl','r') as f:
#     for i in f.readlines():
#
#         item = json.loads(i)
#         try:
#             db.insert('t_xsd_baidu_yake', **item)
#         except Exception as e:
#             print e
db = MySQLdb.connect(host="10.15.1.24", user="writer", passwd="hh$writer", db="hillinsight", charset="utf8")
def up(time):
    
	try:
      	db.insert('t_xsd_baidu_glasses',**item)
    except Exception as e:
       	print e
    return item




for line in sys.stdin:
    up(json.loads(line))


    #item = json.loads(line)
    #try:
     #   db.insert('t_xsd_baidu_yake', **item)
    #except Exception as e:
    #    print e




    
    
    
    
    
    
    