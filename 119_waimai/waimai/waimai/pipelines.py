# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import re
from waimai.items import WaimaibaiduShoplistItem
from waimai.items import WaimaibaiduItem
from waimai.items import WaimaieleShoplistItem
from waimai.items import WaimaieleItem
from waimai.items import WaimaimeituanShoplistItem
from waimai.items import WaimaimeituanItem
class WaimaiPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WaimaibaiduItem):
            conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            temp = {'frm': item['frm'], 'goods_id': item['goods_id'], 'goods_name': item['goods_name'],
                    'month_sales': item['month_sales'], 'price': item['price'],
                    'shop_id': item['shop_id'],
                    'dt':item['dt']
            }
        #uidx_frm_city_shopid是个唯一ID
            cur.execute(
                "insert into `o2o`.`t_hh_waimai_goods_info_snapshot` (`wgd_id`,`frm`,`goods_id`,`goods_name`,"
                "`month_sales`,`price`,`shop_id`,`dt`) "
                "VALUES (NULL,'%(frm)s','%(goods_id)s','%(goods_name)s','%(month_sales)s','%(price)s',"
                "'%(shop_id)s','%(dt)s');"
                % temp
                )
            conn.commit()
            cur.close()
            conn.close()
        elif isinstance(item, WaimaibaiduShoplistItem):
            conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                                    connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
            cur = conn.cursor()
            temp = {'frm': item['frm'], 'shop_id': item['shop_id'], 'shop_name': item['shop_name'],
                    'city': item['city'], 'category1': item['category1'],
                    'min_send_price': item['min_send_price'],
                    'brand_name': item['brand_name'], 'score': item['score'],
                    'avg_delivery_time': item['avg_delivery_time'],
                    'lng': item['lng'], 'lat': item['lat'],
                    'sale_num': item['sale_num'],
                    'month_sale_num': item['month_sale_num'],
                    'dt':item['dt'],
            }
            #uidx_frm_city_shopid是个唯一ID
            cur.execute(
                "insert into `o2o`.`t_hh_waimai_shop_info` (`wsi_id`,`frm`,`shop_id`,`shop_name`,`city`,"
                "`category1`,`min_send_price`,`brand_name`,`score`,`avg_delivery_time`,`lng`,`lat`,"
                "`sale_num`,`month_sale_num`,`dt`) "
                "VALUES (NULL,'%(frm)s','%(shop_id)s','%(shop_name)s','%(city)s','%(category1)s',"
                "'%(min_send_price)s','%(brand_name)s','%(score)s','%(avg_delivery_time)s',"
                "'%(lng)s','%(lat)s','%(sale_num)s','%(month_sale_num)s','%(dt)s');"
                % temp
            )
            conn.commit()
            cur.close()
            conn.close()
        return item

    
    
    
    
    
    
    
    
    
    
    
    
    