# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector
import re
import web
import json
import datetime
from f58_advert.items import F58AdvertItem
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding( "utf-8" )
db = web.database(dbn='mysql', db='58tongcheng', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')

_headers = {
    "Host":"zp.service.58.com",
    "Connection":"keep-alive",
    "Accept":"ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Referer":""
    }

def get_url_list():
    sql = "select city_name,sub1_name,sub2_name,link as url from 58_city_page where getdate='2016-08-25'"
    res = db.query(sql)
    return res

class AdvertSpider(scrapy.Spider):
    name = "f58_advert"
    allowed_domains = ["58.com"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self._dt = datetime.date.today().strftime("%Y-%m-%d")
    
    def start_requests(self):
        for row in self.url_info:
            print row['url']
            url = row['url']
            yield scrapy.FormRequest(url,
                            callback = self.parse_item,
                            meta = {'city_name':row['city_name'], 'sub1_name':row['sub1_name'],
                                    'sub2_name':row['sub2_name'], 'url':url, 'count':'0'},
                            dont_filter = True,
                            )

    def parse_wlt_item(self,  response):
        item = response.meta['item']
        try:
            json_wlt = json.loads(response.body)
            wlt = json_wlt[item['uid']]
        except:
            wlt = ''  
        item['wlt'] = wlt
        yield item

    def check_need_retry(self, response):
        if BeautifulSoup(response.body,"lxml").find(text=re.compile(u'请输入验证码')) != None:
            return True
        if response.meta['url'].find('zp.service.58.com')>-1:
            try:
                json_resp = json.loads(response.body)
                if response.body.find(':') == -1 or len(json_resp) < 5:
                    return True
                else:
                    return False
            except:
                return True
        return False

    def parse_item(self, response):
        if not self.check_need_retry(response):
            html_resp = response.body
            p_SEQ = re.compile('post_count[\s\S]*?",')
            match_SEQ = p_SEQ.search(html_resp)
            if match_SEQ:
                total_count = int(match_SEQ.group().replace('post_count = "','').replace('",','').strip())
            else:
                total_count = 2450

            hxs = Selector(response)
            for item_list in hxs.xpath('//div[@id="infolist"]/dl'):
                if item_list.xpath('//dt[@class="shortMsg"]'):
                    break
                else:
                    if item_list.css('a[class=t]::text'):
                        item_title = "".join(item_list.css('a[class=t]::text').extract())
                    else:
                        item_title = ''
                    if item_list.css('a[class=tuiguang]'):
                        up_time = item_list.css('a[class=tuiguang]::text').extract()[0].replace('\n','').strip()
                    else:
                        up_time = item_list.css('dd[class=w68]::text').extract()[0].replace('\n','').strip()

                    real_up_date = ''
                    if item_list.xpath('dd[@class="w96"]/text()'):
                        location = item_list.xpath('dd[@class="w96"]/text()').extract()[0]
                    else:
                        location = ''
                    company_link = item_list.css('a[class=fl]::attr(href)').extract()[0]
                    uid = item_list.css('input[name=uid]::attr(uid)').extract()[0]
                    company_id = ''
                    if uid == '0_0':
                        if company_link.find('jump')>-1:
                            company_temp = item_list.xpath('@logr').extract()[0].split('_')
                            company_id = company_temp[2]
                    
                        elif company_link.find('mq')>-1:
                            company_id = company_link.replace('http://qy.58.com/mq/','').replace('/','')
                        else:
                            company_id = company_link.replace('http://qy.58.com/','').replace('/','')
                    else:
                        p_SEQ = re.compile('.*?_')
                        match_SEQ = p_SEQ.search(uid)
                        if match_SEQ:
                            company_id = match_SEQ.group().replace('_','')
                    if up_time == u'精准' or up_time == u'置顶' or up_time == u'高级置顶':
                        wlt = ''
                        wlt_url = 'http://zp.service.58.com/api/wltStatss?param='+uid
                        item = F58AdvertItem()
                        item = {'logr': item_list.xpath('@logr').extract()[0],
                            'sortid': item_list.xpath('@sortid').extract()[0],
                            'infoid': item_list.css('i::attr(infoid)').extract()[0],
                            'uid': item_list.css('input[name=uid]::attr(uid)').extract()[0],
                            'company_id': company_id,
                            'item_title': item_title,
                            'job_link': item_list.css('a[class=t]::attr(href)').extract()[0],
                            'urlparams': item_list.css('a[class=t]::attr(urlparams)').extract()[0],
                            'company': item_list.css('a[class=fl]::attr(title)').extract()[0],
                            'company_link': item_list.css('a[class=fl]::attr(href)').extract()[0],
                            'location': location,
                            'up_time': up_time,
                            'wlt': wlt,
                            'city_name': response.meta['city_name'],
                            'district': '',
                            'shangquan': '',
                            'sub1_name': response.meta['sub1_name'],
                            'sub2_name': response.meta['sub2_name'],
                            'current_link': response.meta['url'],
                            'total_count': total_count,
                            'real_up_date': real_up_date,
                            'getdate': self._dt,
                            }
                        tmp_headers = _headers
                        tmp_headers['Referer'] = item['current_link']
                        yield scrapy.FormRequest(wlt_url,
                            headers = tmp_headers,
                            callback = self.parse_wlt_item,
                            meta = {'item':item},
                            dont_filter = True,
                            )
        else:
            if int(response.meta['count']) > 2:
                print "*******overcount:%s"%response.meta['count']
                pass
            else:
                count = str(int(response.meta['count']) + 1)
                print "url:%s count *****:%s"%(response.meta['url'], count)
                yield scrapy.FormRequest(response.meta['url'],
                            callback = self.parse_item,
                            meta = {'city_name':response.meta['city_name'], 'sub1_name':response.meta['sub1_name'],
                                    'sub2_name':response.meta['sub2_name'], 'url':response.meta['url'],'count':count},
                            dont_filter = True,
                            )
    