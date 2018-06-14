# -*- coding: utf-8 -*-
import scrapy
import MySQLdb
import time
import json
import re
from waimai.items import WaimaibaiduShoplistItem

class WaimaibaidulistSpider(scrapy.Spider):
    name = "WaimaiBaidulist"
    allowed_domains = ["waimai.baidu.com"]
    EARTHRADIUS = 6370996.81
    MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
    LLBAND = [75, 60, 45, 30, 15, 0]
    MC2LL = [
        [1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
         91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
        [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826,
         -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
        [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
         -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
        [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
         -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
        [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
         -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
        [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
         -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5]
    ]
    LL2MC = [
        [-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880,
         -35149669176653700, 26595700718403920, -10725012454188240, 1800819912950474, 82.5],
        [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142,
         -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5],
        [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455,
         -115964993.2797253, 97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5],
        [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013,
         -1221952.21711287, 1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
        [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378,
         54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
        [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093,
         2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]
    ]

    # 墨卡托坐标转经纬度坐标

    def convertMC2LL(self, x, y):
        cF = None
        x = abs(x)
        y = abs(y)

        for cE in range(0, len(self.MCBAND)):
            if (y >= self.MCBAND[cE]):
                cF = self.MC2LL[cE]
                break

        location = self.converter(x, y, cF)
        location['lng'] = location["x"]
        del location["x"]
        location['lat'] = location["y"]
        del location['y']
        return location

        # 经纬度坐标转墨卡托坐标

    def convertLL2MC(self, lng, lat):
        cE = None
        lng = self.getLoop(lng, -180, 180)
        lat = self.getRange(lat, -74, 74)
        for i in range(0, len(self.LLBAND)):
            if (lat >= self.LLBAND[i]):
                cE = self.LL2MC[i]
                break
        if cE != None:
            for i in range(len(self.LLBAND) - 1, 0 - 1, -1):
                if (lat <= -self.LLBAND[i]):
                    cE = self.LL2MC[i]
                    break
        return self.converter(lng, lat, cE)

    def converter(self, x, y, cE):
        xTemp = cE[0] + cE[1] * abs(x)
        cC = abs(y) / cE[9]
        yTemp = cE[2] + cE[3] * cC + cE[4] * cC * cC + cE[5] * cC * cC * cC + cE[6] * cC * cC * cC * cC + cE[
                                                                                                              7] * cC * cC * cC * cC * cC + \
                cE[8] * cC * cC * cC * cC * cC * cC
        if x < 0:
            xTemp *= -1
        elif x > 0:
            xTemp *= 1

        if y < 0:
            yTemp *= -1
        elif y > 0:
            yTemp *= 1
        location = {}
        location['x'] = xTemp
        location['y'] = yTemp
        return location

    def getLoop(self, lng, min, max):
        while lng > max:
            lng -= max - min
        while lng < min:
            lng += max - min
        return lng

    def getRange(self, lat, min1, max1):
        if (min1 != None):
            lat = max(lat, min1)
        if (max1 != None):
            lat = min(lat, max1)
        return lat

    def start_requests(self):
        conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='o2o', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        sql = '''
                SELECT city, spot_name, lng, lat
                FROM t_hh_gaode_hotspots
                where city in ('北京', '上海') and lng>0 and lat>0
              '''
        cur.execute(sql)
        temps=cur.fetchall()
        for i,temp in enumerate(temps):
            if temp['lng']<temp['lat']:
                a=temp['lng']
                temp['lng']=temp['lat']
                temp['lat']=a
            mercator=self.convertLL2MC(temp['lng'],temp['lat'])
            url='http://waimai.baidu.com/waimai?qt=shoplist&' \
            'lat=%s&lng=%s&' \
            'address=%s' %(mercator['y'],mercator['x'],temp['spot_name'])
            headers={
                'Host': 'waimai.baidu.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8;',
            }
            yield scrapy.Request(url,callback=self.parse_item,dont_filter=True,headers=headers,
                                 meta={'item':{'city':temp['city']}})

    def parse_item(self,response):
        url=response.url+'?display=json&page=1&count=40'
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Host':'waimai.baidu.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        }
        yield scrapy.Request(url,callback=self.get_data_num,dont_filter=True,headers=headers,
                             meta={'item': {'city': response.meta['item']['city']}})

    def get_data_num(self, response):
        temps=json.loads(response.body)
        shop_number=int(temps['result']['total'])
        if shop_number > 0:
            page_number=(shop_number-1)//40+ 1
            for i in range(1,page_number+1):
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Host': 'waimai.baidu.com',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                }
                url=re.sub('page=1','page=%s' %i,response.url)
                yield scrapy.Request(url,callback=self.get_shop_data,dont_filter=True,headers=headers,
                                     meta={'item': {'city': response.meta['item']['city']}})

    def get_shop_data(self, response):
        item=WaimaibaiduShoplistItem()
        temp=json.loads(response.body)
        if temp['error_no']==0:
            shop_infos=temp['result']['shop_info']
            for shop_info in shop_infos:
                (lng, lat) = self.convertMC2LL(float(shop_info['shop_lng']), float(shop_info['shop_lat']))
                item.update({
                    'frm': '百度',
                    'city': response.meta['item']['city'],
                    'shop_id': shop_info['shop_id'],
                    'shop_name': shop_info['shop_name'],
                    'category1': shop_info['category'],
                    'brand_name': shop_info['brand'],
                    'min_send_price': shop_info['takeout_price'],
                    'avg_delivery_time': shop_info['delivery_time'],
                    'score': shop_info['average_score'],
                    'lng': lng,
                    'lat': lat,
                    'sale_num': shop_info['saled'],
                    'month_sale_num': shop_info['saled_month'],
                    'dt':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                })
                yield item



    