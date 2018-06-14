# coding=utf8

import sys
import json
import time
import web
from lxml import etree
import re

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def parse(line):
    item = {}
    line_json = json.loads(line)
    if line_json.get('meituantype') == 'deal':
        try:
            content = line_json.get('content')
            content = json.loads(content)
            item['mt_deal_id'] = content.get('mtDealGroupId')
            shop = content.get('shop')
            item['mt_shop_id'] = shop.get('poiid')
            item['dp_deal_id'] = content.get('dpDealGroupId')
            frontPoiCates = content.get('frontPoiCates')
            if frontPoiCates:
                item['category'] = frontPoiCates[-1]
            item['title'] = content.get('orderTitle')
            item['old_price'] = content.get('originalPrice')
            item['new_price'] = content.get('price')
            item['sales'] = content.get('solds')
            start = content.get('start')
            end = content.get('end')
            item['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(end, "%b %d, %Y %H:%M:%S %p"))
            item['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(start, "%b %d, %Y %H:%M:%S %p"))
            item['description'] = content.get('coupontitle')
            item['city_id'] = shop.get('cityId')
            item['dp_shop_id'] = shop.get('dpShopId')
            item['dt'] = line_json.get('dt')
            
            db.insert('t_hh_meituan_tuangou_deal_info_tmp',**item)
        except:
            pass
    elif line_json.get('meituantype') == 'shop':
        try:
            content = line_json.get('content')
            item['shop_id'] = ''.join(re.findall('"viewShopId": (\d+),', content))
            item['shop_name'] = ''.join(re.findall('poi_shopname": "(.*?)"', content))
            item['lng'] = ''.join(re.findall('poi_lng": "(.*?)"', content))
            item['lat'] = ''.join(re.findall('poi_lat": "(.*?)"', content))
            item['city_id'] = ''.join(re.findall('poi_city_id":(\d+),', content))
            categorys = re.findall('categoryIds": \[(\d+),(\d+)\],', content)
            if categorys:
                item['category1_id'] = categorys[0][0]
                item['category2_id'] = categorys[0][1]
            item['address'] = ''.join(re.findall('poi-address">(.*?)</div>', content))
            item['avg_price'] = ''.join(re.findall('avg-price">(.*?)</span>', content)).replace('人均：¥', '')
            item['shop_power'] = ''.join(re.findall('<em class="star-text">(.*?)</em></span>', content))
            item['phone_no'] = ''.join(re.findall('data-tele="(.*?)"', content))
            item['dt'] = line_json.get('dt')
            
            db.insert('t_hh_meituan_shop_info_tmp',**item)
        except Exception,e:
            print e
    else:
        content = line_json.get('content')

        shop_id = line_json.get('meituantype')
        # print content
        et = etree.HTML(content)
        # print et
        if len(et):
            feedbackCard_list = et.xpath('//div[@class="feedbackCard"]')
            if feedbackCard_list:
                for feedbackcard in feedbackCard_list:
                    # print feedbackcard
                    try:
                        item_comment = {}
                        item_comment['shop_id'] = shop_id
                        username = ''.join(feedbackcard.xpath('./div[@class="user-wrapper"]/div[@class="user-info-text"]/div/weak[@class="username"]/text()'))
                        score = len(feedbackcard.xpath('./div[@class="user-wrapper"]/div[@class="user-info-text"]/div/span[@class="stars"]/i'))
                        comment_time = ''.join(feedbackcard.xpath('./div[@class="user-wrapper"]/div[@class="user-info-text"]/div/weak[@class="time"]/text()'))
                        comment_content = feedbackcard.xpath('./div[@class="comment"]')
                        if comment_content:
                            comment_content = comment_content[0].xpath('string(.)')
                        else:
                            comment_content = ''
                        comment_content = comment_content.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
                        print username,score,comment_time,comment_content
                        item_comment['user_name'] = username
                        item_comment['total_score'] = score
                        item_comment['comment_text'] = comment_content
                        item_comment['comment_dt'] = comment_time
                        item['dt'] = line_json.get('dt')
                    
                        db.insert('t_hh_meituan_shop_comments_tmp',**item_comment)
                    except:
                        pass


        # content = json.loads(content)
        # comments = content.get('comments')
        # if comments:
        #     for comment in comments:
        #         print comment
        #         item_comment = {}
        #         item_comment['shop_id'] = shop_id
        #         item_comment['comment_id'] = comment.get('reviewId')
        #         item_comment['user_id'] = comment.get('userId')
        #         username = comment.get('userName')
        #         if not username:
        #             username = ''
        #         item_comment['user_name'] = username
        #         item_comment['total_score'] = comment.get('star')
        #         item_comment['comment_text'] = comment.get('comment')
        #         item_comment['comment_dt'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime((int(comment.get('commentTime'))/1000)))
        #         try:
        #             db.insert('t_hh_meituan_shop_comments_tmp',**item_comment)
        #         except:
        #             pass



for line in sys.stdin:
    parse(line)
