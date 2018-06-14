#coding:utf-8
#百度jl解析
import json
import MySQLdb
import test_trans_geo as Geo
import sys
import gevent
import time
# db = MySQLdb.connect(host='127.0.0.1', user="root", passwd="123456", db="test", charset="utf8")
db = MySQLdb.connect(host='10.15.1.24', user="writer", passwd="hh$writer", db="hillinsight", charset="utf8")
cur = db.cursor()
times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
def baidu(html):
    htm = json.loads(html)
    city = htm['province']
    citys = htm['city']
    keyword = htm['keyword']
    name = htm['content']['name']
    area_name = htm['content']['area_name']
    addr = htm['content']['addr']
    area = htm['content']['area']
    geo = htm['content']['geo']
    geo = geo.strip().split('|')[1].split(";")[0]
    x = float(geo.split(',')[0])
    y = float(geo.split(',')[1])
    lta = Geo.trans_geo(x,y)
    std_tag = htm['content']['std_tag']
    uid = htm['content']['uid']
    if keyword == u'abc':
        sql = (
            "insert into t_spider_the_pharmacy(province,city,keyword,name,area_name,addr,area,std_tag,lng,lat,geo_x,geo_y,uid,time)"
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (city, citys, keyword, name, area_name, addr, area, std_tag, lta[0], lta[1], geo.split(',')[0], geo.split(',')[1], uid, times)
    else:
        sql = (
            "insert into t_xsd_dental(province,city,keyword,name,area_name,addr,area,std_tag,lng,lat,geo_x,geo_y,uid,time)"
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (city, citys, keyword, name, area_name, addr, area, std_tag, lta[0], lta[1], geo.split(',')[0], geo.split(',')[1], uid, times)
    try:
        cur.execute(sql, lis)
        db.commit()
    except Exception, e:
        pass
        # print "insert error:", e

#     print city,keyword,name,area_name,addr,area,std_tag,lta,geo.split(',')
# with open(r'E:\gongs_\Baidu\sichuan.jl', 'rb') as f:
#     html = f.readlines()
#     sp = []
#     for i in html:
#         sp.append(gevent.spawn(baidu,i))
# gevent.joinall(sp)

for line in sys.stdin:
    baidu(line)
cur.close()
db.close()    
 
    
    