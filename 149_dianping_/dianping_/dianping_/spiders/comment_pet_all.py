# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
import web
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from scrapy.selector import Selector
from ..items import CommentItem
import re
import copy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from PIL import Image
import random
import web
import traceback
from io import BytesIO
import base64
import hashlib
import time
import urllib
import json

class CommentNotLoginAllSpider(scrapy.Spider):
    name = "CommentNotLoginAll"    
    allowed_domains = ["www.dianping.com"]
    start_urls = ['http://www.dianping.com/']
    handle_httpstatus_list=[302,403]
    user_agent_form = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/63.0.%s Safari/537.36'
    
    def chage_user_agent(self):
        self._user_agent = [self.user_agent_form % (random.random() * 10000), 0]

    @property
    def user_agent(self):
        return self._user_agent[0]

    @user_agent.getter
    def user_agent(self):
        if self._user_agent[1]>=100:
            self._user_agent=[self.user_agent_form %(random.random()*10000),0]
            return self._user_agent[0]
        else:
            self._user_agent[1]+=1
            return self._user_agent[0]

    def start_requests(self):
        self._user_agent=[self.user_agent_form %(random.random()*10000),0]
        self.url = 'http://www.dianping.com/shop/{}/review_all?queryType=sortType&&queryVal=latest'
        self.cookies=''
        yield scrapy.Request('http://www.dianping.com/', meta={'noneeedrequest': 1},
                             dont_filter=True)

    def parse(self, response):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.user_agent
        driver = webdriver.PhantomJS()
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)  # 这两种设置都进行才有效
        driver.get('http://www.dianping.com/')
        driver.implicitly_wait(30)
        driver.set_window_size(1200, 1000)
        time.sleep(5)
        cookies = driver.get_cookies()
        driver.close()
        result = {}
        for i in cookies:
            result[i["name"]] = i["value"]
        self.cookies=result
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Host':'www.dianping.com',
            'Upgrade-Insecure-Requests':'1',
        }
        header['User-Agent']=self.user_agent
        sql = "SELECT * FROM o2o.t_hh_dianping_shop_info WHERE `category2_id`=25147 or `category2_id`=25148;"
        shop_list=[]
        for i in db.query(sql):
            shop_list.append({'shop_id':i.get('shop_id')})

        shop_id=shop_list.pop()['shop_id']
        url = self.url.format(shop_id)
        yield scrapy.Request(url,headers=header,cookies=copy.deepcopy(self.cookies),callback=self.get_item,dont_filter=True,
                             meta={'url':url,'shop_id':shop_id,'tag':0,'shop_data':shop_list,
                                   'lxsdk':copy.deepcopy(self.cookies['_lxsdk'])})

    def get_item(self, response):
        score1_name = ''
        score1 = ''
        score2_name = ''
        score2 = ''
        score3_name = ''
        score3 = ''
        Per_capita = ''
            # return
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Host':'www.dianping.com',
            'Upgrade-Insecure-Requests':'1',
        }
        header['User-Agent'] = self.user_agent
        #if response.status==302:
        #    self.logger.error('302 error many plase check!!!')
        #    response.meta['noneeedrequest']=1
        #    yield scrapy.Request(response.meta['url'], dont_filter=True, callback=self.spiderindefence,
        #                         meta=response.meta, headers=header)
        if (response.status == 403 or response.status == 404 or response.status==302) and response.meta['tag'] < 10:
                response.meta['tag']+=1
                response.meta['noneeedrequest']=1
                if 'reget' in response.meta:
                    reget=response.meta['reget']
                else:
                    reget=0
                response.meta['reget']=reget+1
                yield scrapy.Request(response.meta['url'],dont_filter=True,callback=self.re_get_cookie,
                                     meta=response.meta,headers=header)
                return
        shop_list = response.meta['shop_data']
        if shop_list:
            shop_id = shop_list.pop()['shop_id']
            url = self.url.format(shop_id)
            yield scrapy.Request(url, headers=header, cookies=copy.deepcopy(self.cookies), callback=self.get_item,
                                 dont_filter=True,
                                 meta={'url': url, 'shop_id': shop_id, 'tag': 0, 'shop_data': shop_list,
                                       'lxsdk': copy.deepcopy(self.cookies['_lxsdk'])})
        item = CommentItem()
        html = response.body
        data_info = Selector(text=html).css(".reviews-items > ul > li")

        for i in data_info:
            data_user_id = ''.join(i.css(".dper-photo-aside::attr(data-user-id)").extract())
            i = i.css("div.main-review")
            time_s = ' '.join(''.join(i.css(".misc-info.clearfix > span.time::text").extract()).split())
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


    def re_get_cookie(self,response):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        if response.meta['reget'] > 100:
            self.logger.error('403 error many plase check!!! ')
        elif response.meta['reget'] > 10:
            dcap["phantomjs.page.settings.userAgent"] =self.chage_user_agent()
        else:
            dcap["phantomjs.page.settings.userAgent"] = self.user_agent
        driver = webdriver.PhantomJS()
        # driver=webdriver.Chrome(r'D:\gongju\chromedriver.exe ')
        # driver.set_window_size(1920, 1080)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)  # 这两种设置都进行才有效
        driver.get('http://www.dianping.com/')
        driver.implicitly_wait(30)
        driver.set_window_size(1200, 1000)
        time.sleep(5)
        cookies = driver.get_cookies()
        driver.close()
        result = {}
        shop_data=response.meta['shop_data']
        for i in cookies:
            result[i["name"]] = i["value"]
        self.cookies=result
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Host':'www.dianping.com',
            'Upgrade-Insecure-Requests':'1',
        }
        header['User-Agent'] = self.user_agent
        yield scrapy.Request(response.request.url, headers=header, cookies=copy.deepcopy(self.cookies), callback=self.get_item, dont_filter=True,
                             meta={'url': response.request.url, 'shop_id':response.meta['shop_id'],'shop_data':shop_data,
                                   'tag': response.meta['tag']+1,'lxsdk':copy.deepcopy(self.cookies['_lxsdk']),
                                   'reget':response.meta['reget']+1})

    def spiderindefence(self,response):#反爬虫验证码
        pass    
    
    
    