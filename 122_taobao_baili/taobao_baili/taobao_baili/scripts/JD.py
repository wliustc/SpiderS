#coding:utf8

import json
import sys
import time
import web
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
def from_trans1(item):
    items = {}
    data = json.loads(item)['data']
    key_word = json.loads(item)['key_word']
    city = json.loads(item)['city']
    data = json.loads(data)

    for x in data['mods']['itemlist']['data']['auctions']:
        if len(x.get('icon')) !=0:
            if x['icon'][0]['title'] == u'尚天猫，就购了':
                items['sag'] = u'天猫'
            else:
                items['sag'] = u'淘宝'
        else:
            items['sag'] = u'淘宝'
        items['city'] = city
        items['key_word'] = key_word
        items['uid'] = x.get('nid')
        items['task_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        try:
            db.insert('t_spider_xianhua_id_new', **items)
        except Exception as e:
            print e

            
            
def from_trans(item):
    
    try:
        data = json.loads(item)
        sql = '''update t_spider_xianhua_id set sag='{sag}' where uid='{uid}' '''.format(
                sag = item['sag'],uid=item['uid']
            )
        db.query(sql)
    except Exception as e:
        print e
        
for line in sys.stdin:
    try:
    	from_trans(line)
    except Exception as e:
        print e
        














    
    
    
    
    
    
    
    
    
    