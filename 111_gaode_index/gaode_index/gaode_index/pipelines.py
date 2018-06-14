# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from map_gapde.items import MapStaticspeopleItem
class MapGapdePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,MapStaticspeopleItem):
            #`hillinsight`.`tt_new_table`
            # conn = pymysql.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
            #                        connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
            # cur = conn.cursor()
            try:
                conn = pymysql.connect(host='localhost', user='root', passwd='111111', db='qfliu', charset='utf8',
                                       connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
                cur = conn.cursor()
                temp={'city':item['city'],'spot_id':item['spot_id'],'dt':item['dt'],'val':item['val'],
                      }
                cur.execute('insert into o2o.t_hh_gaode_hotspots_daily_trend_data(`ghtd_id`,`city`,`spot_id`,`dt`,`val`) '
                      'VALUES (NULL,"%(city)s","%(spot_id)s","%(dt)s","%(val)s");'
                        %temp
                      )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                if e.args[0]==1062:
                    print('Duplicate')
                pass
        return item
