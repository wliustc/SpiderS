#coding:utf8
import web
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=13306, host='127.0.0.1')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def up(item):
    item = json.loads(item)
    category1_name = '宠物'
    shop_power_dict = {'10':'一星商户','15':'准二星商户','20':'二星商户','25':'准三星商户','30':'三星商户','35':'准四星商户','40':'四星商户','45':'准五星商户','50':'五星商户','0':'该商户暂无星级'}
    if item.get('branchName'):
        branchName='('+item.get('branchName')+')'
    else:
        branchName=''
    shop_id =  item.get('shop_id')
    shop_name = item.get('name')+branchName
    category1_id = item.get('shopType')
    last_update_dt = item.get('dt')
    city_id = item.get('city_id')
    city_name = item.get('city_name')
    biz_name = item.get('regionName')
    lng = item.get('shop_lng')
    lat = item.get('shop_lat')
    shop_power = str(item.get('shopPower'))
    category2_id = item.get('categoryId')
    category2_name = item.get('categoryName')
    phone_no = item.get('phone')
    address = item.get('shop_address')
    dt=item.get('dt')
    if shop_power in shop_power_dict:
        shop_power_title = shop_power_dict[shop_power]
    else:
        shop_power_title = shop_power
    sql = '''replace into o2o.t_hh_dianping_shop_info(shop_id,shop_name,category1_id,last_update_dt,city_id,city_name,biz_name,lng,lat,shop_power,shop_power_title,category1_name,category2_name,category2_id,phone_no,address) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (
        shop_id, shop_name, category1_id, last_update_dt, city_id, city_name, biz_name, lng, lat, shop_power,shop_power_title,category1_name,category2_name,category2_id,phone_no,address )
    sql1= '''insert into o2o.t_hh_dianping_shop_info_pet_hospital(shop_id,shop_name,category1_id,last_update_dt,city_id,city_name,biz_name,lng,lat,shop_power,shop_power_title,category1_name,category2_name,category2_id,phone_no,address,dt) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (
        shop_id, shop_name, category1_id, last_update_dt, city_id, city_name, biz_name, lng, lat, shop_power,shop_power_title,category1_name,category2_name,category2_id,phone_no,address,dt )
    try:
        db.query(sql)
        db.query(sql1)
    except Exception as e:
        print e

for line in sys.stdin:
    up(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    