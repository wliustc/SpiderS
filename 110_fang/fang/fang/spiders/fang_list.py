# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import FangItem
import web
import hashlib
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0;+http://www.baidu.com/search/spider.html)",
    "referer": 'https://www.baidu.com'
}
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dbo2o = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



class Fang_List_Spider(scrapy.Spider):

    name = 'fang_list_spider'

    def start_requests(self):
        sql = "select city, city_link from t_hh_fang_city_list"
        results = db.query(sql)
        for r in results:
            # r['init'] = 1
            city_code = r['city_link'].split('.')[0]
            url = 'http://fangjia.fang.com/pghouse-c0%s/j3100/' % (city_code)
            # r.pop('city_link')
            yield scrapy.Request(url, headers=headers, callback=self.area_parse, meta={'city': r['city'], 'city_code':
                                 city_code}, dont_filter=True)

    def area_parse(self, response):
        if response.url != 'http://fangjia.fang.com':
            # print response.url
            # raw_input('enter')
            content = response.body.decode('gb18030').encode('utf-8')
            city = response.meta['city']
            city_code = response.meta['city_code']
            # page_reg = re.search('</strong>/(\d+)<', content)
            # page_total = page_reg.group(1)
            # page_total = '20'
            pattern = re.search('id="dl_quxian">([\s\S]*?)</dd>', content)
            if pattern:
                area_con = pattern.group(1)
                pattern1 = re.compile('</a><a href=".*?/a(\d+)')
                area_code = re.findall(pattern1, area_con)
                for code in area_code:
                    page = '1'
                    retry_time = 1
                    url = 'http://fangjia.fang.com/pghouse-c0%s/a%s-i3%s-j3100/' % (city_code, code, page)
                    yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={'city': city, 'city_code':
                                                                                               city_code, 'code': code,
                                                                                               'page': page, 'retry_time': retry_time},
                                         dont_filter=True)

    def list_parse(self, response):
        content = response.body.decode('gb18030').encode('utf-8')
        city = response.meta['city']
        city_code = response.meta['city_code']
        code = response.meta['code']
        # page_total = response.meta['page_total']
        page = response.meta['page']
        url = response.url
        retry_time = response.meta['retry_time']
        # if 'class="list-none mt10' in content and retry_time < 20:
        #     # print url
        #     # raw_input('enter')
        #     retry_time += 1
        #     yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={'city': city, 'city_code':
        #         city_code, 'code': code, 'page': page}, dont_filter=True)
        page_reg = re.search('</strong>/(.*?)<', content)
        if not page_reg and retry_time < 50:
            retry_time += 1
            yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={'city': city, 'city_code':
                city_code, 'code': code, 'page': page, 'retry_time': retry_time}, dont_filter=True)
            # print url
            # raw_input('enter')
        else:
            page_total = page_reg.group(1)
            retry_time = 1
            pattern = re.compile('<div class="house">([\s\S]*?)class="clear"')
            info_list = re.findall(pattern, content)
            for info in info_list:
                items = FangItem()
                items['city'] = city
                items['frm'] = '搜房'
                pattern1 = re.search('class="housetitle"><[\s\S]*?>([\s\S]*?)<', info)
                items['title'] = pattern1.group(1).strip()
                pattern2 = re.search('class="housetitle"><.*?href="(.*?)"', info)
                href = pattern2.group(1)
                uid_re = re.search('.*/(\d+).*', href)
                if uid_re:
                    items['src_uid'] = uid_re.group(1)
                if href.startswith('http://'):
                    items['link'] = href
                    md5 = hashlib.md5()
                    md5.update(href)
                    items['src_uid'] = md5.hexdigest()
                else:
                    items['link'] = 'http://fangjia.fang.com' + href
                pattern3 = re.search('<span class="price">([\s\S]*?)<', info)
                if pattern3:
                    avg_price = pattern3.group(1).strip()
                    if avg_price.isdigit():
                        items['avg_price'] = avg_price
                pattern4 = re.search('二手房：<.*?>(\d+).*', info)
                if pattern4:
                    items['sale_houses'] = pattern4.group(1)
                pattern5 = re.search('租房：<.*?>(\d+).*', info)
                if pattern5:
                    items['rental_houses'] = pattern5.group(1)
                # key_str = ','.join('`%s`' % k for k in items.keys())
                # value_str = ','.join(
                #     'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v) for v in
                #     items.values())
                # kv_str = ','.join(
                #     "`%s`=%s" % (k, 'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v))
                #     for (k, v)
                #     in items.items())
                # sql = "INSERT INTO t_hh_community_source_info(%s) VALUES(%s)" % (key_str, value_str)
                # sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
                # print sql
                # raw_input('enter')
                # dbo2o.query(sql)

                # if city == '上海':
                #     print response.url
                #     raw_input('enter')

                yield items
            if int(page) < int(page_total):
                page = int(page) + 1
                url = 'http://fangjia.fang.com/pghouse-c0%s/a%s-i3%s-j3100/' % (city_code, code, page)
                yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={'city': city, 'city_code':
                    city_code, 'code': code,
                                                                                           'page_total': page_total,
                                                                                           'page': page, 'retry_time': retry_time},
                                     dont_filter=True)