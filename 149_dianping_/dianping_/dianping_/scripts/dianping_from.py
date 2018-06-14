# coding:utf8
import sys
import json
import time
import web
import json
reload(sys)
sys.setdefaultencoding('utf8')
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')






def from_parse(dd):
    item = json.loads(dd)
    dt = item.get('dt')
    shop_id = item.get('shop_id')
    deal_id = item.get('deal_id')
    if deal_id:
        category = item.get('category')
        title = item.get('title')
        new_price = item.get('new_price')
        old_price = item.get('old_price')
        sales = item.get('sales')
        start_time = item.get('start_time')
        end_time = item.get('end_time')
        description = item.get('description')
        if description:
            description = description.replace(',', '、').replace('，', '、')
        city_id = item.get('city_id')
        city_name = item.get('city_name')
        sql = '''replace into t_spider_m_dianping_deal_pet(deal_id,dt,shop_id,category,title,new_price,old_price,sales,start_time,end_time,description,city_id,city_name) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'''%(
            deal_id, dt, shop_id, category, title, new_price, old_price, sales, start_time, end_time, description, city_id,city_name)
        


        try:
            # db.insert('t_hh_dianping_shop_comments_yanke', **dd)
            db.query(sql)
        except Exception as e:
            print e



for line in sys.stdin:
    from_parse(line)



