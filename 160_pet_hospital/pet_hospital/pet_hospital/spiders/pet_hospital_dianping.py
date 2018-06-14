# -*- coding: utf-8 -*-
import sys
import scrapy
# import pandas
import web
# from scrapy.selector import Selector
import json
import re
import datetime
import time
# import xlrd
from pet_hospital.items import TrafficDataItem, TrafficSourceItem, MerchantPageClickItem

reload(sys)
sys.setdefaultencoding("utf-8")

# task_date = datetime.date.today().strftime("%Y-%m-%d")
# last_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
dtime = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

_header = {
    'Host': 'e.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'Referer': 'https://e.dianping.com/merchant/list',
    # 'Cookie': '_hc.v="\"0f6e7827-bc24-4e37-a02d-22712123f3b9.1487061681\""; cy=8; cye=chengdu; __utma=1.1700841063.1489718969.1489718969.1489718969.1; __utmz=1.1489718969.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a030e37-15aeaa15661-4fb813; JSESSIONID=C0C00713A28664E20CC053D266988F34; cXUbkHsw%2FH0ScasTvo0lz7ujLy9lsf59e9bJyqvLIFw%3D=22656280; JxhdnmlB7e4JEYzOiSirmfHSquMJ3UMcWUKuI92hzyA%3D=6124971; r42gX%2FiLe8PTUEe3O3oF6uSM2hz7K4MaZ3WI87Tcv%2Bc%3D=40126992; _bc_u=JwiC8i3nAVtEb1UDka3BVEWvwhVNf%2F%2BAOD%2BVJXQ6f1xpZ8SsTq9s%2BOWHG6Uxtsw7l9gjFPU8Nu6Y8Ij3ijbinroWRXPFA0dDL%2F%2FCRVMKpg8lo%2FQ5dCQ1cn%2FT%2BQ6MwHeFeGmSSdUwtLiSeYX%2FnOYLlIBpThEWmviLh2WlIvRPGyTDx2%2B6lj9xLKbH%2B0mTHdS7HScQPvHSAdWqjH0%2B9OVxiIGDYP8B79h2g4kuqodQ7pdeF4voMXpaAARedLpPJdm9nkXKyGg2TVq6wpiyIc8ImEqjxxj1IApDEqP5jYAf%2BmvYOPk2z3Y8LR7zzzROiwa3hGya2%2FHi84c9ofcQelU0pSxBhZkSLgjNUxdQP9VnPsGWFbCGL7L%2Fgco7kYIFZ2WIZ2aFlN2gk%2FwTQPEQBkhi34RsS3AkSeixvZhBUqsVeTldh4GZ%2FaP0lggN4B5L7yg3AtH4tBhV0ZVr5xeRIJkWc%2FPKE2cC3jEwSVZhTSUD%2B8R1FMQfmPwycYMdGB7L6nQ%2B4s5WT5KvwRVdrXf%2BhSiFX0TQpL7vbIg7WOpzI7cFdh4%3D; mopay_popup_shown=3; hidesupertipsmerge=1; edper=kSN6wyZrHPKXiSMTPWZto7xccJCRReLs',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

_headers = {
    "Host": "e.dianping.com",
    "Connection": "keep-alive",
    "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Upgrade-Insecure-Requests": 1,
    "Referer": "https://e.dianping.com/data/index"
}

_cookie = {
    "MerchantDataCurrentShopId": "19156641",
    "lastInputAccount": "AnanpetMarketing",
    "JSESSIONID": "5E0ADD283838E26CE750CFDAAE6728F5",
    "cye": "beijing",
    "PHOENIX_ID": "0a030e37-158f60136a1-1a8b69d",
    "__utmz": "1.1481596018.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "edper": "fbe78a9a8f9fc3a684704cc09b8f8536bf2b7d7a212a51c12fdf88d46db875c46f7ed7bb1696277efbb6217b2cec87e2"
}

_shop_info = {
    "AnanpetMarketing": {"shop_id": "19156641", "pw": "Ananpet@2017"},
    "ananpet": {"shop_id": "67980409", "pw": "Ananpet2017"},
    "sycysdwyy": {"shop_id": "23618362", "pw": "Cexingpet2018"},
    "myfamily": {"shop_id": "77333775", "pw": "walkrock10"},
    "tjchongyishenggg": {"shop_id": "91020075", "pw": "qwe123456"},
    "a13827223014": {"shop_id": "93513002", "pw": "Cexingpet2"},
}

_method = "POST"


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today - oneday


class PetHospitalSpider(scrapy.Spider):
    name = "pet_hospital_dianping"
    allowed_domains = ["e.dianping.com", 'meituan.com']

    def __init__(self, account='AnanpetMarketing', *args, **kwargs):
        super(PetHospitalSpider, self).__init__(*args, **kwargs)
        self.file_path = "./data/"
        self.platform_type_dict = {"0": "全部平台", "1": "大众点评", "2": "美团"}
        # self.less_shop = "ananpet"
        # self.much_shop = "AnanpetMarketing"
        self.account_name = account
        if account in _shop_info:
            self.account_info = _shop_info[account]
        # else:
        #     self.account_name = None
        self.__click_table = "t_spiderman_pet_hospital_merchantpage_click_info"
        self.__traffic_data_table = "t_spiderman_pet_hospital_traffic_data"
        self.__search_table = "t_spiderman_pet_hospital_traffic_data_source"
        self.cookie = _cookie
        # self.dt = dt

    def start_requests(self):
        db = web.database(dbn='mysql', db='pet_cloud', user='work', pw='phkAmwrF', port=3306, host='10.15.1.14')
        data = db.query(
            '''select dianping_pwd,dianping_id from hospital_base_information where dianping_account='%s';''' % self.account_name)
        if data:
            d = data[0]
            dianping_pwd = d.get('dianping_pwd')
            self.account_info = {}
            # print d.get('dianping_pwd')
            self.account_info['shop_id'] = d.get('dianping_id')
        else:
            if self.account_info:
                dianping_pwd = self.account_info['pw']
            else:
                dianping_pwd = ''
        if dianping_pwd:
            url = 'https://epassport.meituan.com/api/account/login?service=dpmerchantlogin&bg_source=2&loginContinue=https:%2F%2Fe.dianping.com%2Fshopaccount%2Flogin%2Fsetedper%3FtargetUrl%3Dhttps%253A%252F%252Fe.dianping.com%252Fshopportal%252Fpc%252Fnewindex'
            header = {
                'Host': 'epassport.meituan.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Accept': 'application/json',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive'
            }
            body = {"login": self.account_name, "password": dianping_pwd, "part_key": "", "captcha_code": "",
                    "captcha_v_token": ""
                , "sms_verify": 0, "sms_code": ""}
            body = json.dumps(body)
            yield scrapy.Request(url=url, body=body,
                                 method=_method, callback=self.parse_bsid, headers=header, dont_filter=True)

    def parse_bsid(self, response):
        print response.body
        response_json = json.loads(response.body)
        bsid = response_json.get('bsid')
        if bsid:
            print bsid
            header = {
                'Host': 'e.dianping.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://epassport.meituan.com/account/unitivelogin?bg_source=2&service=dpmerchantlogin&feconfig=dpmerchantlogin&continue=https%3A%2F%2Fe.dianping.com%2Fshopaccount%2Flogin%2Fsetedper%3FtargetUrl%3Dhttps%253A%252F%252Fe.dianping.com%252Fshopportal%252Fpc%252Fnewindex',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            url = 'https://e.dianping.com/shopaccount/login/setedper?targetUrl=https%3A%2F%2Fe.dianping.com%2Fshopportal%2Fpc%2Fnewindex&BSID=' + bsid
            # data = requests.get(url, headers=header)
            # print data.content
            yield scrapy.Request(url, headers=header, callback=self.make_requests_from_url, dont_filter=True)

    def make_requests_from_url(self, response):
        if '账号登录中......' in response.body:
            print '登录成功'
            Cookiett = response.headers.getlist('Set-Cookie')
            print Cookiett
            self.cookie['PHOENIX_ID'] = ''.join(re.findall('PHOENIX_ID=(.*?);', ''.join(Cookiett)))
            self.cookie['edper'] = ''.join(re.findall('edper=(.*?);', ''.join(Cookiett)))
            tmp_header = _header
            # url = 'https://e.dianping.com/merchant/load/dealgroup/list?status=1&pageIndex=1'
            url = 'https://e.dianping.com/merchant/load/search/allShops'
            # refer = 'https://e.dianping.com/merchant/list'
            refer = 'https://e.dianping.com/merchant/deallist'
            # refer = 'https://e.dianping.com/mda/web/overview'
            # tmp_header = _header
            tmp_header['Referer'] = refer
            tuandan_count = 0
            return scrapy.Request(url, callback=self.parse, dont_filter=True, headers=tmp_header, cookies=self.cookie,
                                  meta={'tuandan_count': tuandan_count})
        else:
            print '登录失败'

    def parse(self, response):
        phonex_id = ""
        edper = ""
        try:
            # json_obj = json.loads(response.body)
            # if not json_obj['success']:
            # return
            tmp_header = str(response.headers)
            rp = re.compile("PHOENIX_ID=|; Domain")
            phonex_info = rp.split(tmp_header)
            if len(phonex_info) > 1:
                phonex_id = phonex_info[1]
            rp = re.compile("edper=|; Domain")
            edper_info = rp.split(tmp_header)
            if len(edper_info) > 2:
                edper = edper_info[2]
        except:
            print "*******login error :%s" % response.body
            return
        tmp_cookie = _cookie
        if edper != "":
            tmp_cookie['edper'] = edper
        if phonex_id != "":
            tmp_cookie['PHOENIX_ID'] = phonex_id
        # url = "https://e.dianping.com/data/getCityInfo"
        tmp_cookie['MerchantDataCurrentShopId'] = self.account_info['shop_id']
        tmp_cookie['lastInputAccount'] = self.account_name
        json_obj = response.body
        json_data = json.loads((json_obj))
        data = json_data.get('data')
        if data:
            shops = data.get('shops')
            if shops:
                for shop in shops:
                    shop_id = shop.get('shopId')
                    showName = shop.get('showName')
                    for plat_type in self.platform_type_dict.keys():
                        # tmp_data = {"shopId": shop_id, "dateType": "0", "platformType": plat_type,
                        #     "sourceId": "1", "startDate": self.dt, "endDate": self.dt}
                        tmp_data = {'platformType': plat_type, 'dateType': '1', 'source': '1',
                                    'shopId': str(shop_id), 'tab': '0', 'device': '1'}
                        meta_info = {"shop_id": shop_id, "shop_name": showName,
                                     'cookie_info': tmp_cookie, 'platformType': plat_type,
                                     "plat": self.platform_type_dict[plat_type]}
                        # 数据规模
                        url = 'https://e.dianping.com/mda/v2/traffic/scale'

                        yield scrapy.FormRequest(url,
                                                 cookies=tmp_cookie,
                                                 headers=_headers,
                                                 formdata=tmp_data,
                                                 method=_method,
                                                 meta=meta_info,
                                                 callback=self.parse_info,
                                                 dont_filter=True,
                                                 )
                        # 数据来源
                        url = 'https://e.dianping.com/mda/v2/traffic/source'
                        tmp_data = {"platformType": plat_type, "dateType": "1", "shopId": str(shop_id), 'tab': '2',
                                    'device': '1', 'source': '1'}
                        yield scrapy.FormRequest(url,
                                                 cookies=tmp_cookie,
                                                 headers=_headers,
                                                 formdata=tmp_data,
                                                 method=_method,
                                                 meta=meta_info,
                                                 callback=self.parse_info_source,
                                                 dont_filter=True,
                                                 )
                        #  流量去向
                        url = "https://e.dianping.com/mda/v2/traffic/destination"
                        tmp_data = {"platformType": plat_type, "dateType": "1", 'source': '1', "shopId": str(shop_id),
                                    "tab": "3", "device": "1"}
                        yield scrapy.FormRequest(url,
                                                 cookies=tmp_cookie,
                                                 headers=_headers,
                                                 formdata=tmp_data,
                                                 method=_method,
                                                 meta=meta_info,
                                                 callback=self.parse_info_click,
                                                 dont_filter=True,
                                                 )

    def parse_info(self, response):
        meta_info = response.meta
        pvs = list()
        uvs = list()
        try:
            json_obj = json.loads(response.body)
            json_data = json_obj["data"]
            if json_data:
                moduleList = json_data.get('moduleList')
                if moduleList:
                    for li in moduleList:
                        title = li.get('title')
                        if '浏览量' == title:
                            graphics = li.get('graphics')
                            if graphics:
                                detail = graphics.get('detail')
                                if detail:
                                    values = detail[0].get('value')
                                    if values:
                                        for value in values:
                                            pvs.append(value)
                        elif '访客数' == title:
                            graphics = li.get('graphics')
                            if graphics:
                                detail = graphics.get('detail')
                                if detail:
                                    values = detail[0].get('value')
                                    if values:
                                        for value in values:
                                            uvs.append(value)
                    meta_info['pvs'] = pvs
                    meta_info['uvs'] = uvs
            plat_type = meta_info['platformType']
            shop_id = meta_info['shop_id']
            url = 'https://e.dianping.com/mda/v2/traffic/quality'
            tmp_data = {'platformType': str(plat_type), 'dateType': '1', 'source': '1', 'shopId': str(shop_id),
                        'tab': '1', 'device': '1'}
            # meta_info['plat'] = self.platform_type_dict[plat_type]
            yield scrapy.FormRequest(url,
                                     cookies=response.meta['cookie_info'],
                                     headers=_headers,
                                     formdata=tmp_data,
                                     method=_method,
                                     meta=meta_info,
                                     callback=self.parse_summary,
                                     dont_filter=True,
                                     )

        except Exception, e:
            print e
            print "*******response:%s,%s" % (response.body, response.meta)
            return

    def parse_summary(self, response):
        times = list()
        rates = list()
        dts = list()
        try:
            json_obj = json.loads(response.body)
            json_data = json_obj.get('data')
            if json_data:
                moduleList = json_data.get('moduleList')
                if moduleList:
                    for li in moduleList:
                        title = li.get('title')
                        if '平均停留时长' == title:

                            graphics = li.get('graphics')
                            if graphics:
                                dates = graphics.get('dates')
                                detail = graphics.get('detail')
                                if detail:
                                    values = detail[0].get('value')
                                    if values:
                                        for value in values:
                                            times.append(value)
                                    if dates:
                                        for date in dates:
                                            dts.append(date)
                                            # item['dt'] = dt
                                            # item['avg_view_time'] = avg_view_time
                        elif '跳失率' == title:
                            graphics = li.get('graphics')
                            if graphics:
                                detail = graphics.get('detail')
                                if detail:
                                    values = detail[0].get('value')
                                    if values:
                                        for value in values:
                                            rates.append(value)
                                            # item['loss_rate'] = loss_rate
            pvs = response.meta['pvs']
            uvs = response.meta['uvs']
            if str(yesterday) in dts:
                for pv, uv, dt, avg_view_time, loss_rate in zip(pvs, uvs, dts, times, rates):
                    item = TrafficDataItem()
                    item['dt'] = dt
                    item['uv'] = uv
                    item['pv'] = pv
                    item['loss_rate'] = loss_rate
                    item['avg_view_time'] = avg_view_time
                    item['loss_num'] = int(round(int(item['uv']) * float(item['loss_rate']) / 100))
                    item['total_view_time'] = round(int(item['uv']) * float(item['avg_view_time']), 2)
                    item['shop_id'] = response.meta['shop_id']
                    item['hospital_name'] = response.meta['shop_name']
                    item['plat'] = response.meta['plat']
                    item['created_time'] = int(time.time())
                    # item['_target_table'] = self.__traffic_data_table
                    yield item
            else:
                yield

        except Exception, e:
            print e
            print "*******response:%s,%s" % (response.body, response.meta)
            return

    def parse_info_click(self, response):
        try:
            json_obj = json.loads(response.body)
            json_data = json_obj["data"]
            if json_data:
                tableModules = json_data.get('tableModules')
                if tableModules:
                    for modules in tableModules:
                        if modules:
                            rows = modules.get('rows')
                            if rows:
                                for row in rows:
                                    if str(yesterday) == dtime:
                                        item = MerchantPageClickItem()
                                        item['shop_id'] = response.meta['shop_id']
                                        item['hospital_name'] = response.meta['shop_name']
                                        item['plat'] = response.meta['plat']
                                        item['dt'] = dtime
                                        item['created_time'] = int(time.time())
                                        item['click_module'] = row[0]
                                        item['click_count'] = row[1]
                                        item['click_ratio'] = row[2]
                                        item['industry_avg_ratio'] = row[3]
                                        item['circle_ratio'] = row[4]
                                        #   item['_target_table'] = self.__click_table
                                        yield item
                                    else:
                                        yield
        except Exception, e:
            print e
            print "*******response:%s,%s" % (response.body, response.meta)
            return

    def parse_info_source(self, response):
        try:
            json_obj = json.loads(response.body)
            json_data = json_obj.get("data")
            if json_data:
                tableModules = json_data.get('tableModules')
                if tableModules:
                    for modules in tableModules:
                        rows = modules.get('rows')
                        if rows:
                            for row in rows:
                                if str(yesterday) == dtime:
                                    item = TrafficSourceItem()
                                    item['shop_id'] = response.meta['shop_id']
                                    item['hospital_name'] = response.meta['shop_name']
                                    item['plat'] = response.meta['plat']
                                    item['dt'] = dtime
                                    item['created_time'] = int(time.time())
                                    item['source_name'] = row[0]
                                    item['search_count'] = row[1]
                                    item['source_ratio'] = row[2]
                                    item['industry_avg_ratio'] = row[3]
                                    item['circle_ratio'] = row[4]
                                    #    item['_target_table'] = self.__search_table
                                    yield item
                                else:
                                    yield
        except Exception, e:
            print e
            print "*******response:%s,%s" % (response.body, response.meta)
            return