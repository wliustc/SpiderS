# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from weibo_shoes.items import LoadContentItem
from weibo_shoes.items import LoadCommentItem
from weibo_shoes.items import LoadMSearchItem
import MySQLdb
class LoadContentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LoadContentItem) or  isinstance(item,LoadMSearchItem):
            conn = MySQLdb .connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
                                   connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            item['weibo_text']=MySQLdb.escape_string(item['weibo_text'])
            temp = {'star_name': item['star_name'], 'weibo_id': item['weibo_id'], 'url': item['url'],
                    'created_at': item['created_at'], 'weibo_text': item['weibo_text'],
                    'followers_count': item['followers_count'],
                    'statuses_count': item['statuses_count'], 'urank': item['urank'],
                    'retweeted_id': item['retweeted_id'],
                    'retweeted_text': item['retweeted_text'], 'reposts_count': item['reposts_count'],
                    'comments_count': item['comments_count'],
                    'attitudes_count': item['attitudes_count'], 'getdate': item['getdate'],
                    'pinpai':item['pinpai'],'weibo_uid':item['weibo_uid'],'src':item['src']
                    }
            cur.execute(
                "insert IGNORE  into `hillinsight`.`tt_spiderman_weibo_chose_pin` (`id`,`star_name`,`weibo_id`,`url`,`created_at`,`weibo_text`,"
                "`followers_count`,`statuses_count`,`urank`,`retweeted_id`,`retweeted_text`,`reposts_count`,`comments_count`,"
                "`attitudes_count`,`getdate`,`pinpai`,`weibo_uid`,`src`) "
                "VALUES (NULL,'%(star_name)s','%(weibo_id)s','%(url)s','%(created_at)s','%(weibo_text)s','%(followers_count)s',"
                "'%(statuses_count)s','%(urank)s','%(retweeted_id)s','%(retweeted_text)s',"
                "'%(reposts_count)s','%(comments_count)s','%(attitudes_count)s','%(getdate)s','%(pinpai)s',"
                "'%(weibo_uid)s','%(src)s');"
                % temp
                )
            conn.commit()
            cur.close()
            conn.close()
        elif isinstance(item, LoadCommentItem):
            conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
                                   connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
            cur = conn.cursor()

            temp = {'comment_id': item['comment_id'], 'created_at': item['created_at'], 'source': item['source'],
                    'comment_user_id': item['comment_user_id'], 'comment_user_name': item['comment_user_name'],
                    'text': item['text'],
                    'like_counts': item['like_counts'], 'weibo_uid': item['weibo_uid'],
                    'pinpai': item['pinpai'],
                    'weibo_id': item['weibo_id'], 'dt': item['dt'],
                    }
            cur.execute(
                "insert IGNORE  into `hillinsight`.`tt_spiderman_weibo_chose_pin_comment` (`id`,`comment_id`,`created_at`,`source`,"
                "`comment_user_id`,`comment_user_name`,"
                "`text`,`like_counts`,`weibo_uid`,`pinpai`,`weibo_id`,`dt`) "
                "VALUES (NULL,'%(comment_id)s','%(created_at)s','%(source)s','%(comment_user_id)s','%(comment_user_name)s',"
                "'%(text)s','%(like_counts)s','%(weibo_uid)s','%(pinpai)s','%(weibo_id)s','%(dt)s')"
                % temp
            )
            conn.commit()
            cur.close()
            conn.close()
        return item

    
    
    
    
    
    
    
    
    
    