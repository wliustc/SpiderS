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
db = web.database(dbn='mysql', db='o2o', user='reader', pw='hh$reader', port=3306, host='10.15.1.25')
header2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Origin': 'http://www.dianping.com',
            # 'Cache-Control': 'max-age=0',
            'Host': 'www.dianping.com',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }


class ShopTime_Spider(scrapy.Spider):

    name = 'shoptime_spider'

    def start_requests(self):
        url = 'https://m.dianping.com/citylist'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'm.dianping.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        yield scrapy.Request(url, headers=header, callback=self.parse_cityEN, dont_filter=True)

    def parse_cityEN(self, response):
        content = response.body
        for city in city_list:
            reg = '"cityName":"{}".*?"cityEnName":"(.*?)"'.format(city)
            pattern = re.search(reg, content)
            cityEnName = pattern.group(1)
            # print cityEnName
            data = db.query("select city_name,city_id from t_hh_dianping_business_area "
                            "WHERE city_name='{}' group by city_name,city_id".format(city))
            for item in data:
                for cate in ['112', '116']:
                    num = 1
                    city_id = item.city_id
                    post_data = {'cityId': str(city_id),
                                 'cityEnName': cityEnName,
                                 'promoId': '0',
                                 'shopType': '10',
                                 'categoryId': cate,
                                 'regionId': '0',
                                 'sortMode': '2',
                                 'shopSortItem': '0',
                                 'keyword': '',
                                 'searchType': '1',
                                 'branchGroupId': '0',
                                 'aroundShopId': '0',
                                 'shippingTypeFilterValue': '0',
                                 'page': str(num)}
                    url = 'http://www.dianping.com/search/map/ajax/json'
                    yield scrapy.FormRequest(url, headers=header2, formdata=post_data, method='POST', callback=
                    self.parse_detail, dont_filter=True, meta={'num': num, 'cate': cate, 'city_id': city_id,
                                                               'cityEnName': cityEnName, 'city': city})

    def parse_detail(self, response):
        content = response.body
        num = response.meta['num']
        city = response.meta['city']
        cate = response.meta['cate']
        city_id = response.meta['city_id']
        cityEnName = response.meta['cityEnName']
        if 'verify.meituan.com' in response.url:
            post_data = {'cityId': str(city_id),
                         'cityEnName': cityEnName,
                         'promoId': '0',
                         'shopType': '10',
                         'categoryId': cate,
                         'regionId': '0',
                         'sortMode': '2',
                         'shopSortItem': '0',
                         'keyword': '',
                         'searchType': '1',
                         'branchGroupId': '0',
                         'aroundShopId': '0',
                         'shippingTypeFilterValue': '0',
                         'page': str(num)}
            url = 'http://www.dianping.com/search/map/ajax/json'
            yield scrapy.FormRequest(url, headers=header2, formdata=post_data, method='POST', callback=
            self.parse_detail, dont_filter=True, meta={'num': num, 'cate': cate, 'city_id': city_id,
                                                       'cityEnName': cityEnName, 'city': city})
        else:
            items = DianpingFoodItem()
            json_con = json.loads(content)
            # print content
            shop_list = json_con['shopRecordBeanList']
            for info in shop_list:
                shop_id = info['shopId']
                # reviewTagDTOList = info['shopRecordBean'].get('reviewTagDTOList')
                # reviewTag = ''
                # if reviewTagDTOList:
                #     for data in reviewTagDTOList:
                #         reviewTag = reviewTag + data['tagName'] + '|'
                addDate = info['addDate']
                address = info['address']
                categoryName = info['shopRecordBean']['categoryName']
                dishtags = info['shopRecordBean']['dishTags']
                shopTags = info['shopRecordBean'].get('shopTags')
                name = info['shopRecordBean']['shopName']
                branchName = info['shopRecordBean']['branchName']
                priceText = info['avgPrice']
                reviewCount = info['shopRecordBean']['voteTotal']
                shopPower = info['shopRecordBean']['shopPower']
                point1 = info['shopRecordBean']['displayScore1']
                point2 = info['shopRecordBean']['displayScore2']
                point3 = info['shopRecordBean']['displayScore3']
                items['city'] = str(city)
                items['categoryName'] = str(categoryName)
                items['dishtags'] = str(dishtags)
                items['shop_name'] = str(name)
                items['branchName'] = str(branchName)
                items['priceText'] = str(priceText)
                items['reviewCount'] = str(reviewCount)
                items['shopPower'] = str(shopPower)
                items['shop_id'] = str(shop_id)
                items['tagList'] = str(shopTags)
                items['origin_data'] = str(info)
                items['point1'] = str(point1)
                items['point2'] = str(point2)
                items['point3'] = str(point3)
                # ---------------------------
                items['addDate'] = str(addDate)
                items['address'] = str(address)

                yield items
            total_page = json_con['pageCount']
            if num < total_page:
                num += 1
                post_data = {'cityId': str(city_id),
                             'cityEnName': cityEnName,
                             'promoId': '0',
                             'shopType': '10',
                             'categoryId': cate,
                             'regionId': '0',
                             'sortMode': '2',
                             'shopSortItem': '0',
                             'keyword': '',
                             'searchType': '1',
                             'branchGroupId': '0',
                             'aroundShopId': '0',
                             'shippingTypeFilterValue': '0',
                             'page': str(num)}
                url = 'http://www.dianping.com/search/map/ajax/json'
                yield scrapy.FormRequest(url, headers=header2, formdata=post_data, method='POST', callback=
                self.parse_detail, dont_filter=True, meta={'num': num, 'cate': cate, 'city_id': city_id,
                                                           'cityEnName': cityEnName, 'city': city})