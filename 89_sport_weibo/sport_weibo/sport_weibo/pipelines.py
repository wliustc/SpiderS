# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from load_content.items import LoadContentItem
import pymysql
class LoadContentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LoadContentItem):
            conn = pymysql.connect(host='localhost', user='root', passwd='111111', db='qfliu', charset='utf8',
                                   connect_timeout=5000, cursorclass=pymysql.cursors.DictCursor)
            cur = conn.cursor()
            temp = {'star_name': item['star_name'], 'weibo_id': item['weibo_id'], 'url': item['url'],
                    'created_at': item['created_at'], 'weibo_text': item['weibo_text'],
                    'followers_count': item['followers_count'],
                    'statuses_count': item['statuses_count'], 'urank': item['urank'],
                    'retweeted_id': item['retweeted_id'],
                    'retweeted_text': item['retweeted_text'], 'reposts_count': item['reposts_count'],
                    'comments_count': item['comments_count'],
                    'attitudes_count': item['attitudes_count'], 'getdate': item['getdate'],
                    }
            cur.execute(
                "insert into qfliu.t_spiderman_weibo_star (`id`,`star_name`,`weibo_id`,`url`,`created_at`,`weibo_text`,"
                "`followers_count`,`statuses_count`,`urank`,`retweeted_id`,`retweeted_text`,`reposts_count`,`comments_count`,"
                "`attitudes_count`,`getdate`) "
                "VALUES (NULL,'%(star_name)s','%(weibo_id)s','%(url)s','%(created_at)s','%(weibo_text)s','%(followers_count)s',"
                "'%(statuses_count)s','%(urank)s','%(retweeted_id)s','%(retweeted_text)s',"
                "'%(reposts_count)s','%(comments_count)s','%(attitudes_count)s','%(getdate)s');"
                % temp
                )
            conn.commit()
            cur.close()
            conn.close()
        return item
