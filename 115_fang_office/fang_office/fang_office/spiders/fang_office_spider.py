# -*- coding: utf-8 -*-
import scrapy
import re
from fang_office.items import FangOfficeItem
import web
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
dbo2o = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0;+http://www.baidu.com/search/spider.html)",
    "referer": 'https://www.baidu.com'
}


class Fang_Office_Spider(scrapy.Spider):

    name = 'fang_office_spider'

    def start_requests(self):
        sql = '''
                select *, concat(fang_link, '/xiangqing/') url from t_hh_community_source_info
                where frm='搜房' and city in ('武汉', '长沙', '南昌', '郑州', '成都', '西安', '重庆', '深圳', '苏州') and 
                fang_link!='' and property_type like '%写字楼%'
        '''
        results = dbo2o.query(sql)
        for r in results:
            r['built_dt'] = "%s" % (r['built_dt'])
            url = re.sub('/esf/', '/', r['url'])
            yield scrapy.Request(url, headers=headers, callback=self.detail_parse, meta={'data': r}, dont_filter=True)

    def detail_parse(self, response):
        content = str(response.body).decode('gb18030').encode('utf-8')
        hxs = Selector(text=content)
        items = FangOfficeItem()
        xiangqing_box = hxs.xpath('//div[@class="lpblbox1 borderb01 mt10"]')
        for box in xiangqing_box:
            box_name = box.xpath('dl[@class="title02"]/dt[@class="name"]/text()').extract()
            if not box_name:
                continue
            if not box_name[0].strip().startswith('基本信息'):
                continue
            xq_items = box.xpath('dl[@class="xiangqing"]/dd')
            for xq in xq_items:
                content = xq.xpath('text()').extract()[0]
                parts = content.split('：')
                if len(parts) < 2:
                    continue
                key = parts[0].strip()
                val = parts[1].strip()
                if val.startswith(u'暂无资料'):
                    continue
                if key.startswith(u'写字楼等级'):
                    items['building_level'] = val
                elif key.startswith(u'物业类别'):
                    items['classes'] = val
                elif key.startswith(u'总 层 数'):
                    val_re = re.search(u'地上(\d+).*地下(\d+)层', val)
                    if val_re:
                        items['floors'] = int(val_re.group(1)) + int(val_re.group(2))
                    else:
                        val_re = re.search('(\d+).*', val)
                        if val_re:
                            items['floors'] = val_re.group(1)
                elif key.startswith(u'得 房 率'):
                    val_re = re.search('([\d\.]+).*', val)
                    if val_re:
                        items['construction_ratio'] = val_re.group(1)
                elif key.startswith(u'占地面积'):
                    val_re = re.search('([\d\.]+).*', val)
                    if val_re:
                        items['floor_space'] = val_re.group(1)
        items['frm'] = '搜房'
        items['city'] = response.meta['data']['city']
        items['district'] = response.meta['data']['district']
        items['biz_area'] = response.meta['data']['position']
        items['src_uid'] = response.meta['data']['src_uid']
        items['building_name'] = response.meta['data']['title']
        items['lng'] = response.meta['data']['longitude']
        items['lat'] = response.meta['data']['latitude']
        items['alias'] = response.meta['data']['nick_name']
        items['address'] = response.meta['data']['address']
        items['sell_price'] = response.meta['data']['avg_price']
        items['rent_price'] = response.meta['data']['rent_price']
        items['built_dt'] = response.meta['data']['built_dt']
        items['developer'] = response.meta['data']['developer']
        items['property_fee'] = response.meta['data']['property_fee']
        items['building_area'] = response.meta['data']['covered_area']
        items['parking_space'] = response.meta['data']['parking_places']
        items['greening_rate'] = response.meta['data']['greening_rate']
        items['volume_rate'] = response.meta['data']['plot_ratio']
        items['fang_link'] = response.meta['data']['fang_link']

        yield items