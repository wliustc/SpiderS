# -*- coding: utf-8 -*-
import scrapy
import json
import re
import web
from dianping_food.items import DianpingFoodItem

city_list = ['北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '重庆', '南京', '天津', '苏州', '西安', '长沙', '沈阳',
             '青岛', '郑州', '大连', '东莞', '宁波', '哈尔滨', '太原', '南宁', '海口', '乌鲁木齐', '兰州', '福州', '厦门',
             '合肥', '昆明', '长春', '无锡', '保定', '三亚', '呼和浩特', '株洲', '洛阳', '银川', '包头', '吉林', '岳阳',
             '南宁', '湘潭', '遵义', '焦作', '枣庄', '鄂尔多斯', '常德', '大同', '宜宾', '景德镇']

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_hc.v=e7c8d5f2-8d81-c2d0-f3a2-13ced778e262.1497348948; _lxsdk_cuid=15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8; _lxsdk=15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8; PHOENIX_ID=0a010725-15d2b8b625d-5b17bb6; __mta=45959579.1499674144720.1500895060441.1509449223961.3; aburl=1; __utma=1.413890212.1497348949.1498012348.1509516196.4; __utmc=1; s_ViewType=10; cy=2; cye=beijing; pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTI1MzE1NTA3NjI4XV9b; m_flash2=1; cityid=2; switchcityflashtoast=1; source=m_browser_test_33; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; msource=default; logan_session_token=fdlgel6g6b899y2x49sr; _lxsdk_s=1632546c61b-06a-2d8-9be%7C%7C18',
    'Host': 'mapi.dianping.com',
    'Upgrade-Insecure-Requests': '1',
}

header2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
# 'Cookie': '_hc.v=e7c8d5f2-8d81-c2d0-f3a2-13ced778e262.1497348948; _lxsdk_cuid=15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8; _lxsdk=15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8; PHOENIX_ID=0a010725-15d2b8b625d-5b17bb6; __mta=45959579.1499674144720.1500895060441.1509449223961.3; aburl=1; __utma=1.413890212.1497348949.1498012348.1509516196.4; __utmc=1; s_ViewType=10; cy=2; cye=beijing; pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTI1MzE1NTA3NjI4XV9b; m_flash2=1; cityid=2; switchcityflashtoast=1; source=m_browser_test_33; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; msource=default; logan_session_token=fdlgel6g6b899y2x49sr; _lxsdk_s=1632546c61b-06a-2d8-9be%7C%7C18',
'Host': 'm.dianping.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

# header = {
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#                 'Accept-Encoding': 'gzip, deflate, br',
#                 'Accept-Language': 'zh-CN,zh;q=0.8',
#                 'Cache-Control': 'max-age=0',
#                 'Host': 'mapi.dianping.com',
#                 'Upgrade-Insecure-Requests': '1',
#                 'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
#             }

db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
cookies = {'_hc.v': 'e7c8d5f2-8d81-c2d0-f3a2-13ced778e262.1497348948',
'_lxsdk_cuid': '15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8',
'_lxsdk': '15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8',
'PHOENIX_ID': '0a010725-15d2b8b625d-5b17bb6',
'__mta': '45959579.1499674144720.1500895060441.1509449223961.3',
'aburl': '1',
'__utma': '1.413890212.1497348949.1498012348.1509516196.4',
'__utmc': '1',
's_ViewType': '10',
'cy': '2',
'cye': 'beijing',
'pvhistory': '6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTI1MzE1NTA3NjI4XV9b',
'm_flash2': '1',
'cityid': '2',
'switchcityflashtoast': '1',
'source': 'm_browser_test_33',
'default_ab': 'citylist%3AA%3A1%7Cshop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1',
'msource': 'default',
'logan_session_token': 'fdlgel6g6b899y2x49sr',
'_lxsdk_s': '1632546c61b-06a-2d8-9be%7C%7C18'
}
cookies2 = {
'_hc.v': 'e7c8d5f2-8d81-c2d0-f3a2-13ced778e262.1497348948',
'_lxsdk_cuid': '15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8',
'_lxsdk': '15d2b82133cc8-0c3a9a64c6ed93-30667808-1aeaa0-15d2b82133cc8',
'PHOENIX_ID': '0a010725-15d2b8b625d-5b17bb6',
'__mta': '45959579.1499674144720.1500895060441.1509449223961.3',
'aburl': '1',
'__utma': '1.413890212.1497348949.1498012348.1509516196.4',
'__utmc': '1',
's_ViewType': '10',
'cy': '2',
'cye': 'beijing',
'pvhistory': '6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTI1MzE1NTA3NjI4XV9b',
'm_flash2': '1',
'cityid': '2',
'switchcityflashtoast': '1',
'source': 'm_browser_test_33',
'default_ab': 'citylist%3AA%3A1%7Cshop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1',
'msource': 'default',
'_lxsdk_s': '1632546c61b-06a-2d8-9be%7C%7C7',
}


class Dianping_Food_Spider(scrapy.Spider):

    name = 'dianping_food_spider'

    def start_requests(self):
        # for city in city_list:
        data = db.query("SELECT city_name,city_id,area1_id FROM  t_hh_dianping_business_area WHERE city_name NOT in"
                        " ('北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '重庆', '南京', '天津', '苏州', '西安', "
                        "'长沙', '沈阳', '青岛', '郑州', '大连', '东莞', '宁波', '哈尔滨', '太原', '南宁', '海口', "
                        "'乌鲁木齐', '兰州', '福州', '厦门', '合肥', '昆明', '长春', '无锡', '保定', '三亚', '呼和浩特', "
                        "'株洲', '洛阳', '银川', '包头', '吉林', '岳阳', '南宁', '湘潭', '遵义', '焦作', '枣庄', "
                        "'鄂尔多斯', '常德', '大同', '宜宾', '景德镇') GROUP BY city_name,city_id,area1_id")
        for item in data:
            for cate in ['112', '116']:
                city = str(item.city_name)
                num = 0
                city_id = str(item.city_id)
                region_id = str(item.area1_id)
                url = 'https://mapi.dianping.com/searchshop.json?start={}&categoryid={}&parentCategoryId=10&locatecityid={}&limit=30&sortid=0&cityid={}&regionid={}&maptype=0'.\
                    format(str(num), cate, city_id, city_id, region_id)
                yield scrapy.Request(url, headers=header, callback=self.parse_list, meta={'num': num, 'city_id': city_id, 'region_id': region_id, 'cate': cate, 'city': city}, dont_filter=True)

    def parse_list(self, response):
        content = response.body
        # print content
        city = response.meta['city']
        num = response.meta['num']
        city_id = response.meta['city_id']
        region_id = response.meta['region_id']
        cate = response.meta['cate']
        # pattern = re.search('jsonp_\d+_\d+\(([\s\S]*?)\)', content)
        # json_con = json.loads(pattern.group(1))
        json_con = json.loads(content)
        shop_list = json_con['list']
        for info in shop_list:
            city = city
            categoryName = info['categoryName']
            dishtags = info.get('dishtags')
            name = info['name']
            branchName = info['branchName']
            priceText = re.findall('\d+', info['priceText'])
            if priceText:
                priceText = priceText[0]
            else:
                priceText = ''
            reviewCount = info['reviewCount']
            shopPower = info['shopPower']
            shop_id = info['id']
            tagList = info['tagList']
            tags = ''
            if tagList:
                for tag in tagList:
                    tags = tags + tag['text'] + '|'
            origin_data = info
            url_point = 'https://m.dianping.com/shop/' + str(shop_id)
            yield scrapy.Request(url_point, headers=header2, callback=self.parse_point, meta=
            {'city': city, 'categoryName': categoryName, 'dishtags': dishtags, 'name': name, 'branchName': branchName
             , 'priceText': priceText, 'reviewCount': reviewCount, 'shopPower': shopPower, 'shop_id': shop_id,
             'tagList': tags, 'origin_data': origin_data}, dont_filter=True)
        is_next = json_con['isEnd']
        if is_next == 'false':
            num += 30
            url = 'https://mapi.dianping.com/searchshop.json?start={}&categoryid={}&parentCategoryId=10&locatecityid={}&limit=30&sortid=0&cityid={}&regionid={}&maptype=0'. \
                format(str(num), cate, city_id, city_id, region_id)
            yield scrapy.Request(url, headers=header, callback=self.parse_list,
                                 meta={'num': num, 'city_id': city_id, 'region_id': region_id, 'cate': cate,
                                       'city': city}, dont_filter=True)

    def parse_point(self, response):
        content = response.body
        # print content
        # raw_input("enter")
        items = DianpingFoodItem()
        city = response.meta['city']
        categoryName = response.meta['categoryName']
        dishtags = response.meta['dishtags']
        name = response.meta['name']
        branchName = response.meta['branchName']
        priceText = response.meta['priceText']
        reviewCount = response.meta['reviewCount']
        shopPower = response.meta['shopPower']
        shop_id = response.meta['shop_id']
        tagList = response.meta['tagList']
        origin_data = response.meta['origin_data']
        # try:
        point_name1 = ''
        point_name2 = ''
        point_name3 = ''
        point1 = ''
        point2 = ''
        point3 = ''
        pattern = re.search('<div class="desc">([\s\S]*?)</div>', content)
        if pattern:
        # print content
        # raw_input('enter')
            point_con = pattern.group(1)
            point_list = re.findall('<span>(.*?):(.*?)</span>', point_con)
            point_name1 = point_list[0][0]
            point_name2 = point_list[1][0]
            point_name3 = point_list[2][0]
            point1 = point_list[0][1]
            point2 = point_list[1][1]
            point3 = point_list[2][1]
        items['city'] = city
        items['categoryName'] = categoryName
        items['dishtags'] = dishtags
        items['shop_name'] = name
        items['branchName'] = branchName
        items['priceText'] = priceText
        items['reviewCount'] = reviewCount
        items['shopPower'] = shopPower
        items['shop_id'] = shop_id
        items['tagList'] = tagList
        items['origin_data'] = origin_data
        items['point_name1'] = point_name1
        items['point_name2'] = point_name2
        items['point_name3'] = point_name3
        items['point1'] = point1
        items['point2'] = point2
        items['point3'] = point3
        yield items
        # except:
        #     print content
        #     raw_input("enter")