# -*- coding: utf-8 -*-
import scrapy
import re
from fang_shop.items import FangShopItem
import web
import urlparse
import hashlib
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/59.0.3071.115 Safari/537.36'
}
dbo2o = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')



class Fang_Shop_Spider(scrapy.Spider):

    name = 'fang_shop_spider'

    def start_requests(self):
        sql = '''select city,city_link,province from t_hh_fang_city_list'''
        results = db.query(sql)
        for result in results:
            if result['city'] == '北京':
                url = 'http://shop.fang.com/loupan/house/'
                yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={
                    'city': result['city'], 'province': result['province']
                }, dont_filter=True)
            else:
                pattern = re.search('(.*?)\.fang', result['city_link'])
                city_code = pattern.group(1)
                url = 'http://shop.%s.fang.com/loupan/house/' % city_code
                yield scrapy.Request(url, headers=headers, callback=self.list_parse, meta={
                    'city': result['city'], 'province': result['province']
                }, dont_filter=True)

    def list_parse(self, response):
        content = str(response.body).decode('gb18030').encode('utf-8')
        pattern = re.compile('class="title"><a target="_blank" href="(.*?)"')
        city = response.meta['city']
        province = response.meta['province']
        url_list = re.findall(pattern, content)
        for url in url_list:
            url = re.sub('/esf/', '/', url)
            url_new = url + 'xiangqing/'
            yield scrapy.Request(url_new, headers=headers, callback=self.detail_parse, meta={
                'city': city, 'province': province
            }, dont_filter=True)
        pattern_next = re.search('id="PageControl1_hlk_next" href="(.*?)"', content)
        url_domain = urlparse.urlparse(response.url).netloc
        if pattern_next:
            url_next = 'http://' + url_domain + pattern_next.group(1)
            yield scrapy.Request(url_next, headers=headers, callback=self.list_parse, meta={
                'city': city, 'province': province
            }, dont_filter=True)

    def detail_parse(self, response):
        content = str(response.body).decode('gb18030').encode('utf-8')
        city = response.meta['city']
        province = response.meta['province']
        items = FangShopItem()
        base_info = {}
        pattern1 = re.search('所属区域：([\s\S]*?)<', content)
        base_info['所属区域'] = pattern1.group(1)
        pattern2 = re.search('楼盘地址：<span title="([\s\S]*?)"', content)
        base_info['楼盘地址'] = pattern2.group(1)
        pattern3 = re.search('环线位置：([\s\S]*?)<', content)
        base_info['环线位置'] = pattern3.group(1)
        pattern4 = re.search('物业类别：([\s\S]*?)<', content)
        base_info['物业类别'] = pattern4.group(1)
        pattern5 = re.search('建筑类别：([\s\S]*?)<', content)
        base_info['建筑类别'] = pattern5.group(1)
        pattern6 = re.search('总 层 数：([\s\S]*?)<', content)
        base_info['总层数'] = pattern6.group(1)
        pattern7 = re.search('开 发 商：([\s\S]*?)<', content)
        base_info['开发商'] = pattern7.group(1)
        pattern8 = re.search('竣工时间：([\s\S]*?)<', content)
        base_info['竣工时间'] = pattern8.group(1)
        pattern9 = re.search('物 业 费：([\s\S]*?)<', content)
        base_info['物业费'] = pattern9.group(1)
        pattern10 = re.search('物业公司：([\s\S]*?)<', content)
        base_info['物业公司'] = pattern10.group(1)
        pattern11 = re.search('占地面积：([\s\S]*?)<', content)
        base_info['占地面积'] = pattern11.group(1)
        pattern12 = re.search('建筑面积：([\s\S]*?)<', content)
        base_info['建筑面积'] = pattern12.group(1)
        pattern13 = re.search('开间面积：([\s\S]*?)<', content)
        base_info['开间面积'] = pattern13.group(1)
        pattern14 = re.search('是否可分割：([\s\S]*?)<', content)
        base_info['是否可分割'] = pattern14.group(1)
        pattern15 = re.search('电梯数量：([\s\S]*?)<', content)
        base_info['电梯数量'] = pattern15.group(1)
        pattern16 = re.search('空    调：([\s\S]*?)<', content)
        base_info['空调'] = pattern16.group(1)
        pattern17 = re.search('装修状况：([\s\S]*?)<', content)
        base_info['装修状况'] = pattern17.group(1)
        pattern18 = re.search('停 车 位：([\s\S]*?)<', content)
        base_info['停车位'] = pattern18.group(1)
        base_info = json.dumps(base_info, ensure_ascii=False, encoding='utf-8')
        items['base_info'] = base_info
        pattern19 = re.search('交通状况</dt>[\s\S]*?<dl class="xiangqing">([\s\S]*?)</div>', content)
        traffic_con = pattern19.group(1)
        if '暂无资料' in traffic_con:
            items['traffic_info'] = '暂无资料'
            # print traffic_con
            # raw_input('enter')
        else:
            traffic_info = {}
            pattern19_1 = re.search('公交：([\s\S]*?)<', traffic_con)
            if pattern19_1:
                traffic_info['公交'] = pattern19_1.group(1)
            pattern19_2 = re.search('地铁：([\s\S]*?)<', traffic_con)
            if pattern19_2:
                traffic_info['地铁'] = pattern19_2.group(1)
            traffic_info = json.dumps(traffic_info, ensure_ascii=False, encoding='utf-8')
            items['traffic_info'] = traffic_info
        pattern20 = re.search('周边信息</dt>[\s\S]*?<dl class="xiangqing">([\s\S]*?)</div>', content)
        around_con = pattern20.group(1)
        if '暂无资料' in around_con:
            items['around_info'] = '暂无资料'
        else:
            around_info = {}
            pattern20_1 = re.search('商场：([\s\S]*?)<', around_con)
            if pattern20_1:
                around_info['商场'] = pattern20_1.group(1)
            pattern20_2 = re.search('医院：([\s\S]*?)<', around_con)
            if pattern20_2:
                around_info['医院'] = pattern20_2.group(1)
            pattern20_3 = re.search('邮局：([\s\S]*?)<', around_con)
            if pattern20_3:
                around_info['邮局'] = pattern20_3.group(1)
            pattern20_4 = re.search('银行：([\s\S]*?)<', around_con)
            if pattern20_4:
                around_info['银行'] = pattern20_4.group(1)
            pattern20_5 = re.search('餐饮：([\s\S]*?)<', around_con)
            if pattern20_5:
                around_info['餐饮'] = pattern20_5.group(1)
            around_info = json.dumps(around_info, ensure_ascii=False, encoding='utf-8')
            items['around_info'] = around_info
        pattern21 = re.search('class="biaoti">([\s\S]*?)<', content)
        pattern22 = re.search('newcode=(\d+)"', content)
        items['shop_name'] = pattern21.group(1)
        if pattern22:
            items['src_uid'] = pattern22.group(1)
        else:
            md5 = hashlib.md5()
            md5.update(response.url)
            items['src_uid'] = md5.hexdigest()
        items['city'] = city
        items['province'] = province
        items['url'] = response.url
        yield items
