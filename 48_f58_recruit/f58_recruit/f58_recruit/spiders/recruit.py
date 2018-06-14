# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector
import re
import math
import json
import web
import datetime
from f58_recruit.items import F58RecruitItem
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
    sql = "select city_name,city_pinyin,city_id,'' as district,'' as district_pinyin,'' as district_id,'' as shangquan,'' as shangquan_pinyin,sub1_name,sub1_list_name,sub2_name,sub2_list_name,link as url from 58_city_page where getdate='2016-08-25' and city_name='上海'"
    res = db.query(sql)
    return res

class RecuitSpider(scrapy.Spider):
    name = "f58_recruit"
    allowed_domains = ["58.com"]

    def __init__(self, *args, **kwargs):
        self.url_info = get_url_list()
        self._dt_str = datetime.date.today().strftime("%Y-%m-%d")
        self._dt = datetime.date.today()
    
    def start_requests(self):
        for row in self.url_info:
            data = {'city_name':row['city_name'], 'city_pinyin':row['city_pinyin'],
                    'city_id':row['city_id'], 'district':row['district'], 'url':row['url'],
                    'district_pinyin':row['district_pinyin'], 'district_id':row['district_id'],
                    'shangquan':row['shangquan'], 'shangquan_pinyin':row['shangquan_pinyin'],
                    'sub1_name':row['sub1_name'], 'sub1_list_name':row['sub1_list_name'],
                    'sub2_name':row['sub2_name'], 'sub2_list_name':row['sub2_list_name'],
                    'count':'0'}
            url = row['url']
            yield scrapy.FormRequest(url,
                            callback = self.parse_item,
                            meta = data,
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
        info_id = response.meta['info_id']     
        salary_url = "http://zp.service.58.com/api/infoPreview?infoid=%s"%info_id
        tmp_headers = _headers
        tmp_headers['Referer'] = item['current_link']
        yield scrapy.FormRequest(salary_url,
            headers = tmp_headers,
            callback = self.parse_salary_item,
            meta = {'item':item},
            dont_filter = True,
            )

    def parse_salary_item(self, response):
        item = response.meta['item']
        try:
            json_salary = json.loads(response.body)
            item['salary'] = json_salary['salary']
            item['graduate'] = json_salary['xueliyaoqiu']
            item['recruit_num'] = json_salary['zhaopinrenshu']
            item['work_experience'] = json_salary['experience']
        except:
            pass
        yield item

    def check_need_retry(self, response):
        if BeautifulSoup(response.body,"lxml").find(text=re.compile(u'请输入验证码')) != None:
            return True
        if response.meta['url'].find('zp.service.58.com')>-1:
            try:
                json_resp = json.loads(response.body)
                print len(json_resp)
                if response.body.find(':') == -1 or len(json_resp) < 5:
                    return True
                else:
                    return False
            except:
                return True
        return False
    def parse_item(self, response):
        if not self.check_need_retry(response):
            p_SEQ = re.compile('post_count[\s\S]*?",')
            html_resp = response.body
            match_SEQ = p_SEQ.search(html_resp)

            if match_SEQ:
                total_count = int(match_SEQ.group().replace('post_count = "','').replace('",','').strip())
            else:
                total_count = 2450
            if total_count > 2450:
                if response.meta['district'] == '' and response.meta['url'].find('/pn') == -1:
                    sel_district = '''select distinct city_name,city_pinyin,city_id,district,district_pinyin,district_id,
                            '' as shangquan,'' as shangquan_pinyin 
                            from 58tongcheng.58_city_district where city_id="'''+response.meta['city_id']+'''"
                            '''
                    results_district = db.query(sel_district)
                    for district_list in results_district:
                        url_district = 'http://'+district_list['city_pinyin']+'.58.com/'+district_list['district_pinyin']+'/'+response.meta['sub2_list_name']+'/'
                        data = {'url': url_district, 'count':'0',
                                'city_name': response.meta['city_name'],
                                'city_pinyin': response.meta['city_pinyin'],
                                'city_id': response.meta['city_id'],
                                'district': district_list['district'],
                                'district_id': district_list['district_id'],
                                'shangquan': '', 
                                'sub1_name': response.meta['sub1_name'],
                                'sub1_list_name': response.meta['sub1_list_name'],
                                'sub2_name': response.meta['sub2_name'],
                                'sub2_list_name': response.meta['sub2_list_name']
                            }
                        yield scrapy.FormRequest(url_district,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )
            
                elif response.meta['shangquan'] == '' and response.meta['district'] != ''  and response.meta['url'].find('/pn') == -1:
                    sel_shangquan = '''select distinct city_name,city_pinyin,city_id,district,district_pinyin,district_id,
                                shangquan,shangquan_pinyin 
                                from 58tongcheng.58_city_district where district_id="'''+response.meta['district_id']+'''"
                                '''
                    results_shangquan = db.query(sel_shangquan)

                    for shangquan_list in results_shangquan:
                        url_shangquan = 'http://'+shangquan_list['city_pinyin']+'.58.com/'+shangquan_list['shangquan_pinyin']+'/'+response.meta['sub2_list_name']+'/'
                        data = {'url': url_shangquan, 'count':'0',
                                'city_name': response.meta['city_name'],
                                'city_pinyin': response.meta['city_pinyin'],
                                'city_id': response.meta['city_id'],
                                'district': shangquan_list['district'],
                                'shangquan': shangquan_list['shangquan'],
                                'sub1_name': response.meta['sub1_name'],
                                'sub1_list_name': response.meta['sub1_list_name'],
                                'sub2_name': response.meta['sub2_name'],
                                'sub2_list_name': response.meta['sub2_list_name']
                                }
                        yield scrapy.FormRequest(url_shangquan,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )
            
                elif response.meta['shangquan'] != ''  and response.meta['url'].find('/pn') == -1:
                    for page_i in range(2,int(math.ceil(total_count/35))+1):
                        url_new = response.meta['url']+'pn'+str(page_i)+'/'
                        data = {'url': url_new, 'count':'0',
                                'city_name': response.meta['city_name'],
                                'city_pinyin': response.meta['city_pinyin'],
                                'city_id': response.meta['city_id'],
                                'district': response.meta['district'],
                                'shangquan': response.meta['shangquan'],
                                'sub1_name': response.meta['sub1_name'],
                                'sub1_list_name': response.meta['sub1_list_name'],
                                'sub2_name': response.meta['sub2_name'],
                                'sub2_list_name': response.meta['sub2_list_name']
                                }
                        yield scrapy.FormRequest(url_new,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )           
            else:
                if response.meta['url'].find('/pn') == -1:
                    for page_i in range(2,int(math.ceil(total_count/35))+1):
                        url_new = response.meta['url']+'pn'+str(page_i)+'/'
                        data = {'url': url_new, 'count':'0',
                                'city_name': response.meta['city_name'],
                                'city_pinyin': response.meta['city_pinyin'],
                                'city_id': response.meta['city_id'],
                                'district': response.meta['district'],
                                'shangquan': response.meta['shangquan'],
                                'sub1_name': response.meta['sub1_name'],
                                'sub1_list_name': response.meta['sub1_list_name'],
                                'sub2_name': response.meta['sub2_name'],
                                'sub2_list_name': response.meta['sub2_list_name']
                                }
                        yield scrapy.FormRequest(url_new,
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )
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
                    if up_time == u'今天' or up_time == u'精准' or up_time == u'置顶' or up_time == u'高级置顶':
                        real_up_date = self._dt_str
                    elif up_time.find(u'分前')>-1:
                        real_up_date = self._dt_str
                    elif str(up_time).find(u'小时')>-1:
                        real_hour = datetime.timedelta(hours=int(up_time.replace(u'小时前','')))    
                        real_up_date = (self._dt-real_hour).strftime('%Y-%m-%d')
                    elif str(up_time).find(u'天前')>-1:
                        real_day = datetime.timedelta(days=int(up_time.replace(u'天前','')))
                        real_up_date = (self._dt-real_day).strftime('%Y-%m-%d')

                    elif up_time.find('-')>-1:
                        if len(up_time) == 5:
                            real_up_date = '2017-'+str(up_time)
                        else:
                            real_up_date = up_time
                    else:
                        real_up_date = ''

                    if item_list.xpath('dd[@class="w96"]/text()'):
                        location = item_list.xpath('dd[@class="w96"]/text()').extract()[0]
                    else:
                        location = ''
                    if item_list.css('a[class="famousCompanyIcon listPageIcon"]'):
                        valid_type  = 'famousCompany'
                    else:
                        valid_type = ''
                    company_link = item_list.css('a[class=fl]::attr(href)').extract()[0]
                    uid = item_list.css('input[name=uid]::attr(uid)').extract()[0]
                
                    company_id = ''
                    wlt = ''
                    salary = ''
                    graduate = ''
                    recruit_num = ''
                    work_experience = ''
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
                        'valid_type': valid_type,
                        'salary': salary,
                        'graduate': graduate,
                        'work_experience': work_experience,
                        'recruit_num': recruit_num,
                        'city_name': response.meta['city_name'],
                        'district': response.meta['district'],
                        'shangquan': response.meta['shangquan'],
                        'sub1_name': response.meta['sub1_name'],
                        'sub2_name': response.meta['sub2_name'],
                        'current_link': response.meta['url'],
                        'wlt': wlt,
                        'total_count': total_count,
                        'real_up_date': real_up_date,
                        'getdate': self._dt_str,
                        }
                    if uid == '0_0':
                        if company_link.find('jump')>-1:
                            company_temp = item_list.xpath('@logr').extract()[0].split('_')
                            company_id = company_temp[2]
                        elif company_link.find('mq')>-1:
                            company_id = company_link.replace('http://qy.58.com/mq/','').replace('/','')
                        else:
                            company_id = company_link.replace('http://qy.58.com/','').replace('/','')
                        item['company_id'] = company_id
                        tmp_headers = _headers
                        tmp_headers['Referer'] = item['current_link']
                        salary_url = "http://zp.service.58.com/api/infoPreview?infoid="+item_list.css('i::attr(infoid)').extract()[0]
                        yield scrapy.FormRequest(salary_url,
                            headers = tmp_headers,
                            callback = self.parse_salary_item,
                            meta = {'item':item},
                            dont_filter = True,
                            )
                    else:
                        p_SEQ = re.compile('.*?_')
                        match_SEQ = p_SEQ.search(uid)
                        if match_SEQ:
                            company_id = match_SEQ.group().replace('_','')
                        else:
                            company_id = ''
                        item['company_id'] = company_id
                        info_id = item_list.css('i::attr(infoid)').extract()[0]
                        wlt_url = 'http://zp.service.58.com/api/wltStatss?param='+uid
                        yield scrapy.FormRequest(wlt_url,
                            callback = self.parse_wlt_item,
                            meta = {'item':item, 'info_id':info_id},
                            dont_filter = True,
                            )
        else:
            if int(response.meta['count']) > 10:
                print "****************endend:%s"%response.meta['count']
                pass
            else:
                count = str(int(response.meta['count']) + 1)
                print "************count:%s"%count
                response.meta['count'] = count
                data = response.meta
                yield scrapy.FormRequest(response.meta['url'],
                            callback = self.parse_item,
                            meta = data,
                            dont_filter = True,
                            )