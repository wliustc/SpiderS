# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import re
import sys
import citylist
reload(sys)
sys.setdefaultencoding('utf-8')

_filter_cookies = {
    "_hc.v":"da06573c-a571-76ac-447b-dbe520c62b07.1489977857",
    "s_ViewType":"10",
    "JSESSIONID":"B24945CA2233848C3B57DEC476FD5C3A",
    "aburl":"1",
    "PHOENIX_ID":"0a01677b-15ba82b90d5-e507bea",
}
_list_cookies = {
    "_hc.v":"da06573c-a571-76ac-447b-dbe520c62b07.1489977857",
    "PHOENIX_ID":"0a01677b-15ba82b90d5-e507bea",
    "s_ViewType":"10",
    "JSESSIONID":"FC021E11F8A824C9FDB3FCE2B62920C6",
    "aburl":"1",
}

_list_post = {
    "cityId":"2",
    "cityEnName":"beijing",
    "promoId":"0",
    "shopType":"0",
    "categoryId":"0",
    "regionId":"0",
    "sortMode":"2",
    "shopSortItem":"1",
    "keyword":"",
    "searchType":"2",
    "branchGroupId":"0",
    "shippingTypeFilterValue":"0",
    "page":"1",
}

_review_post = {
    "shopId":"3007666",
    "cityId":"2",
    "categoryURLName":"shopping",
    "power":"5",
    "cityEnName":"beijing",
    "shopType":"20",
}

_filter_map = re.compile(r'searchmap", config:(.*)}\);')

def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj

def get_end(data):
    result = []
    for item in data:
        if item['value']:
            result.append(item['value'])
        if "children" in item:
            result.extend(get_end(item['children']))
    else:
        return result

class ListSpider(scrapy.Spider):
    name = "list"
    allowed_domains = ["dianping.com"]
    def __init__(self,cy=u"湖北,湖南,江西,四川,广东,江苏,陕西", search=u"良品铺子", *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.filter_url = 'http://www.dianping.com/search/map/keyword/{}/0_{}'
        self.list_url = 'http://www.dianping.com/search/map/ajax/json?{}'
        self.review_url = 'http://www.dianping.com/ajax/json/shopDynamic/allReview?{}'
        self.cy = cy
        self.search = search
        self.cy = []
        for item in cy.split(","):
            if item in citylist.cityname:
                for it in citylist.cityname[item]:
                    if it in citylist.citys:
                        self.cy.append([item,citylist.citys[it]])
        self.start_urls = []

    def start_requests(self):
        for cid in self.cy: 
            url = self.filter_url.format(cid[1],urllib.quote(self.search.encode("utf-8")))
            yield scrapy.Request(url,
                cookies = _filter_cookies,
                dont_filter = True,
                meta = {"city":cid[0]},
                callback = self.parse_dim
            )
            

    def parse_dim(self, response):
        if response.status == 200:
            m = _filter_map.search(response.body)
            city_s = response.meta['city']
            if m:
                filters = m.group(1)
                filters = filters.replace("category:",'"category":').replace("sort:",'"sort":').replace("location:",'"location":').replace(", ],"," ],")
                filters = json.loads(filters)
                cityId = get_json_hierarchy(filters,["filter","cityId"])
                cityEnName = get_json_hierarchy(filters,["filter","cityEnName"])
                end_categorys = get_end(get_json_hierarchy(filters,["menu","location"]))
                for item in end_categorys:
                    posts = dict(_list_post)
                    posts['cityId'] = cityId
                    posts['cityEnName'] = cityEnName
                    posts['regionId'] = item
                    posts['keyword'] = self.search
                    url = self.list_url.format(urllib.urlencode(posts))
                    yield scrapy.Request(url,
                        meta = {"posts":posts,"city":city_s},
                        cookies = _list_cookies,
                        callback = self.parse_list
                    )
            else:
                self.logger.error("dim get error parse error {}".format(response.body))
        else:
            self.logger.error("dim get error {}".format(response.body))

    def parse_list(self, response):
        metas = response.meta['posts']
        if response.status == 200:
            bodys = json.loads(response.body)
            city_s = response.meta['city']
            if bodys['code'] == 200:
                if bodys['pageCount'] > 50:
                    self.logger.error("large than 50 :{} {}".format(response.url,bodys['pageCount']))
                else:
                    for item in bodys['shopRecordBeanList']:
                        tmp = {}
                        tmp['shopName'] = item['shopName']
                        tmp['address'] = item['address']
                        tmp['cityId'] = metas['cityId']
                        tmp['cityEnName'] = metas['cityEnName']
                        tmp['lat'] = item['geoLat']
                        tmp['lng'] = item['geoLng']
                        tmp['shopId'] = item['shopId']
                        tmp['avgPrice'] = item['avgPrice']
                        tmp['voteTotal'] = item['shopRecordBean']['voteTotal']
                        tmp['phoneNo'] = item['phoneNo']
                        tmp['lat'] = item['geoLat']
                        tmp['province'] = city_s
                        tmp['power'] = item['shopRecordBean']['power']
                        tmp['shopType'] = item['shopRecordBean']['shopType']
                        tmp['score1'] = item['shopRecordBean']['score1']
                        tmp['score2'] = item['shopRecordBean']['score2']
                        tmp['score3'] = item['shopRecordBean']['score3']
                        params = dict(_review_post)
                        params['shopId'] = tmp['shopId']
                        params['cityId'] = tmp['cityId']
                        params['power'] = tmp['power']
                        params['cityEnName'] = tmp['cityEnName']
                        params['shopType'] = tmp['shopType']
                        url = self.review_url.format(urllib.urlencode(params))
                        yield scrapy.Request(url,
                            meta = {"data":tmp},
                            dont_filter = True,
                            callback = self.parse_review
                        )
                    page = int(metas['page']) + 1
                    if page <= bodys['pageCount']:
                        params = dict(metas)
                        params['page'] = page
                        url = self.list_url.format(urllib.urlencode(params))
                        yield scrapy.Request(url,
                            meta = {"posts":params,"city":city_s},
                            cookies = _list_cookies,
                            dont_filter = True,
                            callback = self.parse_list
                        )
            else:
                self.logger.error("list code error:{}".format(meta['cityId']))
        else:
            self.logger.error("list status error:{}".format(meta['cityId']))

    def parse_review(self, response):
        metas = response.meta['data']
        if response.status == 200:
            bodys = json.loads(response.body)
            tmp = []
            if "summarys" in bodys and bodys['summarys']:
                for item in bodys['summarys']:
                    tmp.append(item['summaryName']+"({})".format(item['summaryCount']))
            metas['summarys'] = ";".join(tmp)
            yield metas
        else:
            metas['summarys'] = "-1"
            yield metas
    
    
    