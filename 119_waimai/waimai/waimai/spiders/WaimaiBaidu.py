# -*- coding: utf-8 -*-
import scrapy
import MySQLdb
import re
from waimai.items import WaimaibaiduItem
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class WaimaibaiduSpider(scrapy.Spider):
    name = "WaimaiBaidu"
    allowed_domains = ["http://waimai.baidu.com"]

    def start_requests(self):
        conn = MySQLdb.connect(host='10.15.1.14', user='work', passwd='phkAmwrF', db='o2o', charset='utf8',
                               connect_timeout=5000)
        cur = conn.cursor()
        cur.execute('select shop_id, concat("http://waimai.baidu.com/waimai/shop/", shop_id) url '
                    'from t_hh_waimai_shop_info '
                    'where frm="百度";')
        temps=cur.fetchall()
        for i,temp in enumerate(temps):
            url=temp[1]
            headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'Host':'waimai.baidu.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            }
            yield scrapy.Request(url,meta={'item':{'shop_id':temp[0]}},dont_filter=False,headers=headers)
            if i>100:
                break

    def parse(self, response):
        item_secs = response.xpath('//section[@class="menu-list"]/div[@class="list-wrap"]')
        for sec in item_secs:
            cate_name = sec.xpath('div[@class="list-status"]/span/text()').extract()[0]
            item_list = sec.xpath('.//li[@class="list-item"]')
            for li in item_list:
                item = WaimaibaiduItem()
                li_data = li.xpath('@data').extract()[0]
                data_parts = li_data.split('$')
                item.update({
                    'frm': 'Baidu',
                    'goods_id': data_parts[0],
                    'goods_name': data_parts[1],
                    'price': data_parts[2],
                    'category': cate_name,
                    'shop_id': response.meta['item']['shop_id'],
                    'month_sales':'',
                    'dt':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                })
                sales_count = li.xpath('.//span[@class="sales-count"]')
                for sc in sales_count:
                    sc_txt = sc.xpath('text()').extract()[0]
                    if sc_txt.startswith('月售'):
                        sc_re = re.search(u'月售(\d+)份', sc_txt)
                        if sc_re:
                            item['month_sales'] = sc_re.group(1)
                yield item
    
    
    
    
    
    
    
    