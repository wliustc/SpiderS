# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import traceback
from daily_taobao.items import DailyTaobaoItem
import time
import re

reload(sys)
sys.setdefaultencoding('utf8')
shop_levels = ['tmall', 'taobao']
citys = ['北京', '上海', '广州', '深圳', '杭州', '海外', '江浙沪', '珠三角', '京津冀', '东三省', '港澳台', '江浙沪皖', '长沙',
         '长春', '成都', '重庆', '大连', '东莞', '佛山', '福州', '贵阳', '合肥', '金华', '济南', '嘉兴', '昆明', '宁波',
         '南昌', '南京', '青岛', '泉州', '沈阳', '苏州', '天津', '温州', '无锡', '武汉', '西安', '厦门', '郑州', '中山',
         '石家庄', '哈尔滨', '安徽', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '湖北', '湖南',
         '江苏', '江西', '吉林', '辽宁', '宁夏', '青海', '山东', '山西', '陕西', '云南', '四川', '西藏', '新疆',
         '浙江', '澳门', '香港', '台湾', '内蒙古', '黑龙江']

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

cate_list = ['50468018',  '54176002',  '50466013',  '50480016',  '50029587',  '54186001',  '50038571',  '50464021',
             '50476014',  '50023636',  '50038718',  '50071817',  '50474022',  '54168001',  '54168002',  '50458014',
             '50484019',  '50484020',  '54204001',  '50470025',  '50470026', '50334022', '50334023', '50346028',
             '55812024', '50356016', '50342020', '55876020', '50354024', '50340023', '55822030', '55938014',
             '55848034', '55844029', '50468016', '50340020']


class Allcates_Spider_Tmp(scrapy.Spider):

    name = 'allcates_spider_tmp'

    def start_requests(self):
        for line in cate_list:
            for level in shop_levels:
                for city in citys:
                    for num in range(0, 4400, 44):
                        retry = 0
                        baseurl = 'https://s.taobao.com/search?initiative_id=staobaoz_20171113&cat={}&p4ppushleft' \
                                  '=%2C44&sort=sale-desc&seller_type={}&loc={}&s={}'.format(line, level, city, num)
                        baseurl = baseurl.strip()
                        yield scrapy.Request(baseurl, headers=header, callback=self.parse_json, dont_filter=True, meta=
                        {'fg_category_id': line, 'level': level, 'city': city, 'retry': retry})
                for num in range(0, 4400, 44):
                    retry = 0
                    yield scrapy.Request('https://s.taobao.com/search?initiative_id=staobaoz_20171113&cat={}&p4ppushleft' \
                                  '=%2C44&sort=sale-desc&seller_type={}&s={}'.format(line, level, num), headers=header,
                                        callback=self.parse_json, dont_filter=True, meta={'fg_category_id': line, 'level': level, 'retry': retry})

    def parse_json(self, response):
        items = DailyTaobaoItem()
        fg_category_id = response.meta['fg_category_id']
        retry = response.meta['retry']
        content = response.body
        pattern = re.search('g_page_config = ([\s\S]*?}});', content)
        if pattern:
            # print 'success'
            json_con = json.loads(pattern.group(1))
            itemlist = json_con['mods']['itemlist']
            if itemlist.get('data'):
                try:
                    goodslist = itemlist['data']['auctions']
                    for goods_info in goodslist:
                        goods_id = goods_info['nid']
                        shop_url = goods_info['shopLink']
                        category_id = goods_info['category']
                        user_id = goods_info['user_id']
                        shop_name = goods_info['nick']
                        dt = time.strftime('%Y-%m-%d', time.localtime())
                        items['goods_id'] = goods_id
                        items['shop_url'] = shop_url
                        items['category_id'] = category_id
                        items['fg_category_id'] = fg_category_id.strip()
                        items['user_id'] = user_id
                        items['shop_name'] = shop_name
                        items['dt'] = dt

                        yield items
                except:
                    traceback.print_exc()
        else:
            if retry < 10:
                retry += 1
                yield scrapy.Request(response.url, callback=self.parse_json, dont_filter=True, meta={
                    'fg_category_id': fg_category_id, 'retry': retry})
            else:
                # print 'fail'
                # raw_input("enter")
                pass