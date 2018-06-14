# -*- coding: utf-8 -*-
from hillinsight.storage import dbs

db = dbs.create_engine("hillinsight", online=False, master=True)

def get_shops():
    
    shops = db.query('''select shopId from t_dianping_yaodian where is_crawl=0 and voteTotal!=0;''')

    return [e['shopId'] for e in shops]

def _get_proxy():
    urls = db.query('''
    select url from t_hh_proxy_list where domain ='dianping.com' and valid>0 order by update_time desc limit 100;''')

    return [e['url'] for e in urls]

def _set_is_crawl(shop_id):
    db.query('update t_dianping_yaodian set is_crawl=1 where shopId={};'.format(shop_id))
