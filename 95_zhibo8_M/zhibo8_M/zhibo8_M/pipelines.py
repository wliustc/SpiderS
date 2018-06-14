# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#db = web.database(dbn='mysql', db='ttt', user='root', pw='123456', port=3306, host='127.0.0.1')

class AppDownloadPipeline(object):
    def process_item(self, item, spider):

        try:
            if item.get('nickname'):
                db.insert('t_xsd_pptv_hot',**item)
             else:
              	db.insert('t_xsd_pptv_circle',**item)
        except Exception as e:
            print e
    
    