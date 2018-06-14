# -*- coding: utf-8 -*-
import scrapy
import json
import time
from weixinsmall.items import WeixinsmallItem
import urllib
class XiangwushuoSpider(scrapy.Spider):
    name = "xiangwushuo_all_list"
    allowed_domains = ["39916353.share1diantong.com"]
    start_urls = ['http://39916353.share1diantong.com/']

    def start_requests(self):
        headers={
            'Accept-Encoding': 'gzip',
            'Referer': 'https://servicewechat.com/wxa344448166586158/144/page-frame.html',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044022 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN',
            'Host': '39916353.share1diantong.com',
            'Connection': 'Keep-Alive',
            'charset':'UTF-8',
        }
        page_num=1
        user_id='7360244'
        body={
                'pagenum':str(page_num),
                'orderby_index':str(0),
                'cate':'全部',
                'topic_status':'1',
                'topic_is_new':'0',
                '&topic_is_local':'0',
                'version':'2',
                'uuid':'93ee2efc2097038470af46c982303304',
                'release_version':'20180223',
                'AppID':'wxa344448166586158'
              }
        yield scrapy.FormRequest('https://39916353.share1diantong.com/index/topiclst_v2/',method='POST',
                             headers=headers,
                            formdata=body
                             ,meta={'item':{'page_num':page_num,'user_id':user_id}})

    def parse(self, response):
        print('******************page_num:%s********************' %response.meta['item']['page_num'])
        temp=json.loads(response.body.decode())
        next_page=temp['next_page']
        datas=temp['col_one']
        print(temp['pagenum'],temp['login_user_id'],temp['data'])
        for data in datas.keys():
            item=WeixinsmallItem()
            try:
                item['topic_view_count']=datas[data]['topic_view_count']#主题浏览人数,目前未看见在APP显示
                item['topic_title']=datas[data]['topic_title']#主题标题
                item['topic_abstract'] = datas[data]['topic_abstract']#主题摘要
                item['topic_ctime_standard'] = datas[data]['topic_ctime_standard']#主题创建标准时间
                item['userName'] = datas[data]['userName']#创建主题的用户
                item['topic_id'] = datas[data]['topic_id']#主题的id
                item['homecity'] = datas[data]['homecity']#用户所在城市
                item['topic_like_count'] = datas[data]['topic_like_count']#喜欢这个主题的人数
                item['amount'] = datas[data]['amount']#商品数
                item['topic_address'] = datas[data]['topic_address']#用户地址
                item['market_price'] = datas[data]['market_price']#市场价
                item['topic_collect_count'] = datas[data]['topic_collect_count']#主题收藏人数
                item['pricetype'] = datas[data]['pricetype']#
                item['pricetypename'] = datas[data]['pricetypename']#
                item['topic_status'] = datas[data]['topic_status']
                item['last_bid_price'] = datas[data]['last_bid_price']#上次成交价
                item['topic_user_id'] = datas[data]['topic_user_id']#用户ID
                item['topic_url'] = datas[data]['topic_url']
                item['user_url'] = datas[data]['user_url']
                item['topic_tags'] = datas[data]['topic_tags']#主题的分类
                item['user_cell'] = datas[data]['user_cell']#用户电话
                item['user_realname'] = datas[data]['user_realname']#用户真名
                item['dt']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                yield item
            except Exception as e:
                self.logger.error(datas[data])
        if next_page:
            page_num = response.meta['item']['page_num']+1
            user_id = response.meta['item']['user_id']
            headers = {
                'Accept-Encoding': 'gzip',
                'referer': 'https://servicewechat.com/wxa344448166586158/144/page-frame.html',
                'content-type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044022 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN MicroMessenger/6.6.6.1300(0x26060634) NetType/WIFI Language/zh_CN',
                'Host': '39916353.share1diantong.com',
                'Connection': 'Keep-Alive',
            }
            body = {
                'pagenum': str(page_num),
                'orderby_index': str(0),
                'cate': '全部',
                'topic_status': '1',
                'topic_is_new': '0',
                '&topic_is_local': '0',
                'version': '2',
                'uuid': '93ee2efc2097038470af46c982303304',
                'release_version': '20180223',
                'AppID': 'wxa344448166586158'
            }
            yield scrapy.FormRequest('https://39916353.share1diantong.com/index/topiclst_v2/', method='POST',
                                     headers=headers,
                                     formdata=body
                                     , meta={'item': {'page_num': page_num, 'user_id': user_id}})
        else:
            self.logger.error('************pagenum:%s*******************' %response.meta['item']['page_num'])


    