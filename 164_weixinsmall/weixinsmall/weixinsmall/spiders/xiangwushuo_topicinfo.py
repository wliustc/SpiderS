# -*- coding: utf-8 -*-
import scrapy
import json
from weixinsmall.items import WeixinsmallTopicInfoItem
from weixinsmall.items import WeixinsmallTopicUserInfoItem
from weixinsmall.items import WeixinsmallbidslstItem
from weixinsmall.items import WeixinsmallSponsorItem
import MySQLdb
class XiangwushuoTopicinfoSpider(scrapy.Spider):
    name = "xiangwushuo_topicinfo"
    allowed_domains = ["39916353.share1diantong.com"]
    start_urls = ['http://39916353.share1diantong.com/']

    def start_requests(self):
        conn = MySQLdb.connect(host='10.15.1.24', user='writer',port=3306, passwd='hh$writer', db='hillinsight', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()

        cur.execute('select distinct topic_id from t_spider_xiangwushuo_list where `dt`=date(now());')
        temps=cur.fetchall()
        cur.close()
        conn.close()
        headers={
            'Accept-Encoding': 'gzip',
            'referer': 'https://servicewechat.com/wxa344448166586158/144/page-frame.html',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044022 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN',
            'Host': '39916353.share1diantong.com',
            'Connection': 'Keep-Alive',
        }
        for temp in temps:
            topic_id=temp['topic_id']
            user_id='7361266'
            yield scrapy.Request('https://39916353.share1diantong.com/topic/topicinfo',method='POST',headers=headers,
                                 body='topic_id=%s&uuid=93ee2efc2097038470af46c982303304&'
                                      'session_login_user_id=%s&release_version=20180223&'
                                      'AppID=wxa344448166586158'
                                      %(topic_id,user_id),meta={'item':{'topic_id':topic_id,'user_id':user_id}})
    def parse(self, response):
        temp=json.loads(response.body.decode())
        topicInfo=temp['topicInfo']
        if not temp['success'] and temp['data']=='请求过于频繁，请重试！':
            yield response.request
            return
        try:
            topic_userInfo=temp['topic_userInfo']
        except Exception as e:
            topic_userInfo=None
        try:
            bidslst=temp['bidslst']
        except Exception as e:
            bidslst=None
        try:
                sponsor_lst=temp['sponsor_lst']
        except Exception as e:
            sponsor_lst=None

        try:
            item_topicInfo=WeixinsmallTopicInfoItem()
            item_topicInfo['topic_id']=topicInfo['topic_id']
            item_topicInfo['topic_user_id'] = topicInfo['topic_user_id']
            item_topicInfo['topic_order'] = topicInfo['topic_order']
            item_topicInfo['topic_view_count'] = topicInfo['topic_view_count']
            item_topicInfo['topic_comment_count'] = topicInfo['topic_comment_count']
            item_topicInfo['topic_like_count']=topicInfo['topic_like_count']
            item_topicInfo['topic_collect_count'] = topicInfo['topic_collect_count']
            item_topicInfo['topic_sponsor_count'] = topicInfo['topic_sponsor_count']
            item_topicInfo['topic_title'] = topicInfo['topic_title']
            item_topicInfo['topic_comment_count'] = topicInfo['topic_comment_count']
            item_topicInfo['topic_abstract']=topicInfo['topic_abstract']
            item_topicInfo['allowcommenting'] = topicInfo['allowcommenting']
            item_topicInfo['group_members'] = topicInfo['group_members']
            item_topicInfo['price'] = topicInfo['price']
            item_topicInfo['market_price'] = topicInfo['market_price']
            item_topicInfo['amount'] = topicInfo['amount']
            item_topicInfo['topic_bid_hours']=topicInfo['topic_bid_hours']
            item_topicInfo['topic_address'] = topicInfo['topic_address']
            item_topicInfo['topic_tags'] = topicInfo['topic_tags']
            item_topicInfo['price'] = topicInfo['price']
            item_topicInfo['topic_limited_buying'] = topicInfo['topic_limited_buying']
            item_topicInfo['topic_sold_amout'] = topicInfo['topic_sold_amout']
            item_topicInfo['topic_order_price'] = topicInfo['topic_order_price']
            item_topicInfo['scope_level'] = topicInfo['scope_level']
            item_topicInfo['pic_count'] = topicInfo['pic_count']
            item_topicInfo['status'] = topicInfo['status']
            item_topicInfo['sponsor_count'] = topicInfo['sponsor_count']
            item_topicInfo['btn_pricetypename'] = topicInfo['btn_pricetypename']
            yield item_topicInfo
        except Exception as e:
            self.logger.error('%s,,,,,%s'%(response.meta['item']['topic_id'],temp))
            pass
        if topic_userInfo:
            item_topic_userInfo=WeixinsmallTopicUserInfoItem()
            item_topic_userInfo['topic_id'] = response.meta['item']['topic_id']
            item_topic_userInfo['user_id'] = topic_userInfo['user_id']
            item_topic_userInfo['user_status'] = topic_userInfo['user_status']
            item_topic_userInfo['user_cell'] = topic_userInfo['user_cell']
            item_topic_userInfo['user_wechat_id'] = topic_userInfo['user_wechat_id']
            item_topic_userInfo['user_realname'] = topic_userInfo['user_realname']
            item_topic_userInfo['user_address'] = topic_userInfo['user_address']
            item_topic_userInfo['user_email'] = topic_userInfo['user_email']
            item_topic_userInfo['user_ctime'] = topic_userInfo['user_ctime']
            item_topic_userInfo['user_level'] = topic_userInfo['user_level']
            item_topic_userInfo['user_name'] = topic_userInfo['user_name']
            item_topic_userInfo['user_alias'] = topic_userInfo['user_alias']
            item_topic_userInfo['user_title'] = topic_userInfo['user_title']
            item_topic_userInfo['user_follow_count'] = topic_userInfo['user_follow_count']
            item_topic_userInfo['user_follower_count'] = topic_userInfo['user_follower_count']
            item_topic_userInfo['user_survey_score'] = topic_userInfo['user_survey_score']
            item_topic_userInfo['user_relation_count'] = topic_userInfo['user_relation_count']
            item_topic_userInfo['user_topic_count'] = topic_userInfo['user_topic_count']
            item_topic_userInfo['user_homecity'] = topic_userInfo['user_homecity']
            item_topic_userInfo['userGender'] = topic_userInfo['userGender']
            item_topic_userInfo['userRegfrom'] = topic_userInfo['userRegfrom']
            item_topic_userInfo['userType'] = topic_userInfo['userType']
            item_topic_userInfo['sceneId'] = topic_userInfo['sceneId']
            item_topic_userInfo['credit'] = topic_userInfo['credit']
            item_topic_userInfo['userName'] = topic_userInfo['userName']
            item_topic_userInfo['user_quotas'] = topic_userInfo['user_quotas']
            item_topic_userInfo['homecity'] = topic_userInfo['homecity']
            item_topic_userInfo['btnfollow'] = topic_userInfo['btnfollow']
            yield item_topic_userInfo
        if bidslst:
            for data in bidslst.keys():
                item_bidslst = WeixinsmallbidslstItem()
                item_bidslst['userName']=bidslst[data]['userName']
                item_bidslst['user_id'] = bidslst[data]['user_id']
                item_bidslst['topic_id'] = bidslst[data]['topic_id']
                item_bidslst['homecity'] = bidslst[data]['homecity']
                item_bidslst['bid_price'] = bidslst[data]['bid_price']
                item_bidslst['bid_ctime'] = bidslst[data]['bid_ctime']
                item_bidslst['bid_status'] = bidslst[data]['bid_status']
                item_bidslst['bid_statusname'] = bidslst[data]['bid_statusname']
                item_bidslst['id'] = bidslst[data]['id']
                yield item_bidslst
        if sponsor_lst:
            for data in sponsor_lst.keys():
                item_sponsor_lst = WeixinsmallSponsorItem()
                item_sponsor_lst['topic_id'] = response.meta['item']['topic_id']
                item_sponsor_lst['user_id']=sponsor_lst[data]['user_id']
                item_sponsor_lst['user_status'] = sponsor_lst[data]['user_status']
                item_sponsor_lst['user_cell'] = sponsor_lst[data]['user_cell']
                item_sponsor_lst['user_wechat_id'] = sponsor_lst[data]['user_wechat_id']
                item_sponsor_lst['user_realname'] = sponsor_lst[data]['user_realname']
                item_sponsor_lst['user_address'] = sponsor_lst[data]['user_address']
                item_sponsor_lst['user_email'] = sponsor_lst[data]['user_email']
                item_sponsor_lst['user_secret'] = sponsor_lst[data]['user_secret']
                item_sponsor_lst['user_ctime'] = sponsor_lst[data]['user_ctime']
                item_sponsor_lst['user_alias']=sponsor_lst[data]['user_alias']
                item_sponsor_lst['user_title'] = sponsor_lst[data]['user_title']
                item_sponsor_lst['user_follow_count'] = sponsor_lst[data]['user_follow_count']
                item_sponsor_lst['user_follower_count'] = sponsor_lst[data]['user_follower_count']
                item_sponsor_lst['user_survey_score'] = sponsor_lst[data]['user_survey_score']
                item_sponsor_lst['user_relation_count'] = sponsor_lst[data]['user_relation_count']
                item_sponsor_lst['user_topic_count'] = sponsor_lst[data]['user_topic_count']
                item_sponsor_lst['user_comment_count'] = sponsor_lst[data]['user_comment_count']
                item_sponsor_lst['user_homecity'] = sponsor_lst[data]['user_homecity']
                item_sponsor_lst['userGender'] = sponsor_lst[data]['userGender']
                item_sponsor_lst['userType'] = sponsor_lst[data]['userType']
                item_sponsor_lst['credit'] = sponsor_lst[data]['credit']
                item_sponsor_lst['user_help_flowers'] = sponsor_lst[data]['user_help_flowers']
                item_sponsor_lst['userName'] = sponsor_lst[data]['userName']
                item_sponsor_lst['user_quotas'] = sponsor_lst[data]['user_quotas']
                yield item_sponsor_lst

    
    
    
    
    
    
    
    
    
    
    
    
    
    