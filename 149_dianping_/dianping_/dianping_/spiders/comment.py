# -*- coding: utf-8 -*-
import sys
import time
import scrapy
from scrapy.selector import Selector
import random
import re
import urlparse
import web
from ..items import CommentItem
# from fake_useragent import UserAgent
reload(sys)
sys.setdefaultencoding('utf8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


star_dict = {10:'1',20:'2',30:'3',40:'4',50:'5'}

def header():
    #随机ua
    header = {
        'Host':'www.dianping.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1'}
    random_t = random.randint(0,1000)
    # ua = UserAgent()
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 61; Win64; x64) %s AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' % random_t

    # header['User-Agent'] = str(ua.random)
    return header


class CommentSpider(scrapy.Spider):
    name = 'comment'
    start_urls = ['http://www.dianping.com/shop/21889860/review_all']
    def __init__(self,*args,**kwargs):
        super(CommentSpider,self).__init__(*args,**kwargs)
        self.url = 'http://www.dianping.com/shop/{}/review_all'
    def start_requests(self):
        #sql = 'select shop_id from t_spider_m_dianping_shop limit 100'
        sql = 'select DISTINCT shop_id from t_spider_m_dianping_shop WHERE reviewCount !=0 AND categoryId=181'
        #sql = 'select DISTINCT shop_id from t_spider_m_dianping_shop_jianshen WHERE reviewCount !=0'
        for i in db.query(sql):
            url = self.url.format(i.get('shop_id'))
            yield scrapy.Request(url,headers=header(),dont_filter=True,meta={'url':url,'shop_id':i.get('shop_id'),'tag':0})
    def parse(self, response):
        score1_name = ''
        score1 = ''
        score2_name = ''
        score2 = ''
        score3_name = ''
        score3 = ''
        Per_capita = ''
        if (response.status == 403 or response.status == 404) and response.meta['tag'] < 100:
            response.meta['tag']+=1
            yield scrapy.Request(response.meta['url'],dont_filter=True,callback=self.parse,meta=response.meta,headers=header())
        item = CommentItem()
        html = response.body

        data_info = Selector(text=html).css(".reviews-items > ul > li")
        # data_info = Selector(text=html).css("div.main-review")

        for i in data_info:
            data_user_id = ''.join(i.css(".dper-photo-aside::attr(data-user-id)").extract())
            i = i.css("div.main-review")
            time_s = ' '.join(''.join(i.css(".misc-info.clearfix > span.time::text").extract()).split())
            # data_user_id = ''.join(i.css(".dper-info > a.name::attr(href)").extract()).split('/')
            # if data_user_id:
            #     data_user_id = data_user_id[-1]
            # else:data_user_id=''
            comment_id = ''.join(i.css(".misc-info.clearfix > span.actions > a:nth-child(1)::attr(data-id)").extract())
            name = i.css(".dper-info > .name::text").extract()
            star = ''.join(re.findall('\d+', ''.join(i.css(".review-rank > span:nth-child(1)::attr(class)").extract())))
            serve_info = i.css(".review-rank > span.score")
            if i.css(".main-review > div.review-words.Hide"):
                comment = ''.join(''.join(i.css(".main-review > div.review-words.Hide::text").extract()).split())
            else:
                comment = ''.join(''.join(i.css(".review-words::text").extract()).split())
            info = serve_info.css("span.item::text").extract()

            if info:
                if len(info) == 3:
                    score1_name,score1 = info[0].split()[0].split('：')
                    score2_name,score2 = info[1].split()[0].split('：')
                    score3_name,score3 = info[2].split()[0].split('：')


                elif len(info) ==4:
                    score1_name, score1 = info[0].split()[0].split('：')
                    score2_name, score2 = info[1].split()[0].split('：')
                    score3_name, score3 = info[2].split()[0].split('：')
                    Per_capita = info[3].split()[0].split('：')[1]
                    if  '元' not in Per_capita:
                        Per_capita = ''
            if star:
                for key in star_dict:
                    if key == int(star):
                        star = star_dict.get(key)
                        break

            name = ''.join(name[0].split())
            item['comment_text'] = comment
            item['user_name'] = name
            item['score1_name'] = score1_name
            item['score1'] = score1
            item['score2_name'] = score2_name
            item['score2'] = score2
            item['score3_name'] = score3_name
            item['score3'] = score3
            item['user_contrib_val'] = Per_capita
            item['total_score'] = star
            item['shop_id'] = response.meta['shop_id']
            item['comment_dt'] = time_s
            item['user_id'] = data_user_id
            item['comment_id'] = comment_id
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield item
            # print time_s,data_user_id,comment_id
        NextPage = Selector(text=html).css(".NextPage::attr(href)").extract_first()
        if NextPage:
            shop_id = response.meta['shop_id']
            url =urlparse.urljoin(response.url,NextPage)
            yield scrapy.Request(url,dont_filter=True,headers=header(),meta={'url':url,'shop_id':shop_id,'tag':0},callback=self.parse)



    
    
    
    
    
    
    