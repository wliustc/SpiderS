#coding:utf8

import json
import time
import web
import sys
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
def from_trans(item):
    items = {}
    data = json.loads(item)['data']
    user_id = json.loads(item)['suid']
    brand = json.loads(item)['title']
    data = json.loads(data)
    for x in data['mods']['itemlist']['data']['auctions']:
        if user_id == x.get('user_id'):
            items['merchandise_url'] =  'https://detail.tmall.com/item.htm?id=' + x.get('nid')
            items['picture_url'] = 'https:' + x.get('pic_url')
            items['brand'] = brand
            items['dataid'] = x.get('nid')
            items['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            try:
                db.insert('t_xsd_tianmao_id_picture', **items)
            except Exception as e:
                print e

for line in sys.stdin:
    try:
    	from_trans(line)
    except Exception as e:
        print e











    
    