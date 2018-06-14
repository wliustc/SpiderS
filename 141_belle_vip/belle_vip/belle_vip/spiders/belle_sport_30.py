# -*- coding: utf-8 -*-
import datetime
import json
import urllib

import scrapy
import time
import ast
import web

from belle_vip.items import BelleVipItem

header = {
    'Host': 'compass.vis.vip.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    # 'Cookie': 'visadminvipvipcom=7m8dn0b01si9s8asf1drqppj23; _ga=GA1.2.1825428114.1512731485; _gid=GA1.2.723306915.1512731485; mars_pid=0; mars_cid=1512731528747_bc146d76e1fa27e06737a68ddf2b6ea4; mars_sid=356f111e78f48d00c57e91d31e110e95; PHPSESSID=7m8dn0b01si9s8asf1drqppj23; user=wguan%40hillinsight.com; jobnumber=1111; nickname=%E5%85%B3%E7%8E%AE; shop_id=16769; expire=1512742788; vendor_code=603480; vendor_id=603480; user_id=66734; user_type=1; shops=16769; codes=603480; token=eyJ0b2tlbiI6ImE4MWZiMjIxMmY4OTIxYjU1ZWIxNGI1MDlhMDQwNGJiIiwidG9rZW4xIjoiZWI5MjcxMzYxZTcyODA4MjM5MmI0NWQ3ZGQxYTVmZjAiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJ3Z3VhbkBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjY3MzQiLCJ2aXNTZXNzaW9uSWQiOiI3bThkbjBiMDFzaTlzOGFzZjFkcnFwcGoyMyIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D; vc_token=eyJ0b2tlbiI6ImE4MWZiMjIxMmY4OTIxYjU1ZWIxNGI1MDlhMDQwNGJiIiwidG9rZW4xIjoiZWI5MjcxMzYxZTcyODA4MjM5MmI0NWQ3ZGQxYTVmZjAiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJ3Z3VhbkBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjY3MzQiLCJ2aXNTZXNzaW9uSWQiOiI3bThkbjBiMDFzaTlzOGFzZjFkcnFwcGoyMyIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D; permission=_5_6_32_33_34_36_37_38_39_40_41_42_43_44_45_95_96_97_98_99_100_101_105_106_107_108_111_112_114_115_116_117_118_119_121_122_123_126_127_129_130_137_140_142_144_145_147_148_149_150_151_152_153_154_155_156_157_158_178_179_186_187_188_189_190_191_192_193_196_197_200_201_203_204_205_206_207_208_209_210_211_212_213_214_215_217_218_221_222_229_233_234_235_236_242_243_244_245_246_247_248_249_250_251_252_253_254_255_259_260_261_266_277_279_280_282_283_284_288_289_290_293_296_297_302_304_309_310_313_315_316_317_318_319_321_322_323_324_325_333_338_339_340_341_342_343_344_345_356_357_360_363_364_365_366_367_368_369_370_371_372_373_374_375_376_377_378_379_380_381_382_383_387_388_389_392_393_394_407_408_409_414_415_418_419_420_421_422_426_427_428_429_430_431_432_435_436_437_438_439_440_442_449_450_451_452_453_482_491_492_493_494_495_496_504_505_511_512_519_521_522_523_524_525_526_527_528_529_530_531_534_536_541_542_543_544_554_555_556_557_558_559_560_572_575_581_582_586_587_588_590_591_592_594_595_596_600_601_602_605_606_607_608_609_610_614_615_616_619_621_624_625_626_627_628_629_630_631_632_633_634_635_636_637_638_639_641_645_646_648_649_650_651_652_653_654_658_659_660_661_662_663_664_665_666_667_668_674_675_676_677_678_679_680_681_682_683_684_685_686_687_688_689_690_691_692_693_694_695_696_697_698_699_700_701_702_703_704_705_712_714_715_716_717_728_730_731_732_733_734_735_736_737_738_739_740_741_742_743_744_745_746_747_748_749_750_751_752_753_754_755_756_757_758_759_760_761_762_763_764_765_766_767_768_769_770_771_772_773_774_777_778_779_780_783_784_785_786_806_807_808_809_810_811_812_813_814_815_816_817_818_819_820_828_829_; axdata=MDkxZmUyNmI2NzgzNjA4NDM2MWVkYTM4OGU3YjYzYzQwYjg4NmQzMjliMTVmNWQ3NGQzOWE0ZDc2YjBmMmQ5Nw%3D%3D; visit_id=9C44399271CB4EEB22D632D5528EE510; compassV=1.3.1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

#cookie = {'mars_cid': '1528766753669_0d083089f28b88516648bce0d44c058d', 'user_type': '1', 'shop_id': '18894', 'PHPSESSID': 'rivopo3oa0q10t9k5n3r95tdb6', 'codes': '605599', 'user_id': '68384', 'mars_sid': '04eb5468bafed786bc410f4e429bd224', 'compassV': '2.4', 'guideV': '2.3', 'mars_pid': '0', 'vc_token': 'eyJ0b2tlbiI6ImM2OTg5YzAwY2Q3NjUxMzRiYWFkN2Q0YTcxYWI5YTdjIiwidG9rZW4xIjoiNGZlZGY2MzQ5ZDcyNjIxMGI0YjJjNGZiOTM1ZWFlMDEiLCJ2ZW5kb3JJZCI6IjE4ODk0IiwidXNlck5hbWUiOiJ5bGluQGhpbGxpbnNpZ2h0LmNvbSIsInZlbmRvckNvZGUiOiI2MDU1OTkiLCJ1c2VySWQiOiI2ODM4NCIsInZpc1Nlc3Npb25JZCI6InJpdm9wbzNvYTBxMTB0OWs1bjNyOTV0ZGI2IiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D', 'permission': '_95_96_105_106_107_112_114_116_117_119_121_123_129_130_137_140_149_150_152_196_197_200_201_203_206_207_208_209_210_211_212_213_214_229_242_243_244_245_259_260_261_279_288_289_290_293_304_315_316_317_338_340_342_360_389_394_408_414_415_427_428_429_435_442_528_530_572_834_', 'vendor_id': '605599', '_ga': 'GA1.2.1007065487.1528766737', 'vendor_code': '605599', 'axdata': 'ZWYwZjQ5ZGU2ZGMyMzlkYzY1YTM1OTM5YmZkOWYyNjQ3MGIyY2YzZjJlODY3ZWZhOGJjMDkxMjI2OThmZDU3ZQ%3D%3D', 'visadminvipvipcom': 'rivopo3oa0q10t9k5n3r95tdb6', 'expire': '1528774007', 'user': 'ylin%40hillinsight.com', 'nickname': '%E6%9E%97%E9%98%B3', 'visit_id': 'D61502A3B26BBE788CC1891701A2C315', 'token': 'eyJ0b2tlbiI6ImM2OTg5YzAwY2Q3NjUxMzRiYWFkN2Q0YTcxYWI5YTdjIiwidG9rZW4xIjoiNGZlZGY2MzQ5ZDcyNjIxMGI0YjJjNGZiOTM1ZWFlMDEiLCJ2ZW5kb3JJZCI6IjE4ODk0IiwidXNlck5hbWUiOiJ5bGluQGhpbGxpbnNpZ2h0LmNvbSIsInZlbmRvckNvZGUiOiI2MDU1OTkiLCJ1c2VySWQiOiI2ODM4NCIsInZpc1Nlc3Npb25JZCI6InJpdm9wbzNvYTBxMTB0OWs1bjNyOTV0ZGI2IiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D', 'tipInfoV': '2.3', '_gid': 'GA1.2.1647209744.1528766737', 'shops': '18894', 'jobnumber': '20180105'}


dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                  host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')


class BelleSpider(scrapy.Spider):
    name = "belle_sport_30"
    allowed_domains = ["vis.vip.com"]

    # start_urls = ['http://vis.vip.com/']
    def __init__(self, select_date='yesterday', *args, **kwargs):
        super(BelleSpider, self).__init__(*args, **kwargs)
        if select_date == 'yesterday':
            self.select_date = self.caculate_date()
        else:
            ll = []
            ll.append(select_date)
            self.select_date = ll

    def start_requests(self):
        while True:
            try:
                # db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306,
                #                  host='10.15.1.24')
                # db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                #                   host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')
                data = db.query(
                    'select sign from t_spider_vip_sign where dt="%s" and spider_name="%s"' % (dt, BelleSpider.name))
                break
            except:
                time.sleep(1)
        if data:
            sign = data[0].get('sign')
            if sign:
                pass
        else:
            data2 = db.query('select sign from t_spider_vip_sign_run_sport')
            if data2:
                sign2 = data2[0].get('sign')
                if sign2:
                    pass
            else:
                db.query('insert into t_spider_vip_sign_run_sport values(0,"doing")')
                data = db.query('select cookie from t_spider_vip_sign_cookie_sport;')
                cookie = data[0].get('cookie')
                print cookie
                cookie = ast.literal_eval(cookie)
                brand_list = [
                    '阿迪达斯adidas'
                ]
                for dd in self.getYesterday():
                    dd_ = dd.split(',')
                    print dd_
                    for brand in brand_list:
                        url = 'http://compass.vis.vip.com/newGoods/details/getDetails?callback=&brandStoreName=' + urllib.quote(
                                brand) + '&pageSize=200000&pageNumber=1&sortColumn=goodsAmt&sortType=1&warehouseName=0&optGroup=0&goodsCnt=0&beginDate=' + \
                                  dd_[0] + '&endDate=' + dd_[
                                      1] + '&brandName=&sumType=1&goodsType=0&optGroupFlag=0&warehouseFlag=0&analysisType=0&brandType='
                        yield scrapy.Request(url, callback=self.parse, headers=header, meta={'brand': brand, 'dt': dt, 'cookie':cookie},
                                                 cookies=cookie)

    def parse(self, response):
        try:
            content_json = json.loads(response.body)
            singleResult = content_json.get('singleResult')
            cookie = response.meta['cookie']
            if singleResult:
                list = singleResult.get('list')
                if list:
                    brand_list = [
                        'New Balance',
                        'ASICS',
                        'ONITSUKA TIGER',
                        'UGG',
                        '匡威converse',
                        '彪马PUMA',
                        '耐克Nike',
                        '范斯vans',
                        '锐步Reebok',
                        '阿迪达斯adidas'
                    ]
                    for dd in self.select_date:
                        # for dd in self.get_date():
                        dd_ = dd.split(',')
                        print dd_
                        for brand in brand_list:
                            url = 'http://compass.vis.vip.com/newGoods/details/getDetails?callback=&brandStoreName=' + urllib.quote(
                                brand) + '&pageSize=200000&pageNumber=1&sortColumn=goodsAmt&sortType=1&warehouseName=0&optGroup=0&goodsCnt=0&beginDate=' + \
                                  dd_[0] + '&endDate=' + dd_[
                                      1] + '&brandName=&sumType=1&goodsType=0&optGroupFlag=0&warehouseFlag=0&analysisType=0&brandType='
                            yield scrapy.Request(url, callback=self.parse_all, headers=header,
                                                 meta={'brand': brand, 'dt': dt},
                                                 cookies=cookie)
                else:
                    db.query('delete from t_spider_vip_sign_run_sport')

            else:
                db.query('delete from t_spider_vip_sign_run_sport')

        except:
            pass

    def parse_all(self, response):
        item = BelleVipItem()
        item['content'] = response.body
        item['meta'] = response.meta
        yield item

    def get_date1(self):
        import calendar as cal
        list_ = []
        year = 2016
        for m in range(8, 13):
            d = cal.monthrange(year, m)
            list_.append('2016-%s-01,2016-%s-%s' % (str(m).zfill(2), str(m).zfill(2), d[1]))
        # print '--------'
        year = 2017
        for m in range(1, 12):
            d = cal.monthrange(year, m)
            list_.append('2017-%s-01,2017-%s-%s' % (str(m).zfill(2), str(m).zfill(2), d[1]))
        return list_

    def get_date(self):
        import calendar as cal
        list_ = []
        year = 2017
        for m in range(5, 11):
            d = cal.monthrange(year, m)
            list_.append('2017-%s-01,2017-%s-%s' % (str(m).zfill(2), str(m).zfill(2), d[1]))
        return list_

    def get_week(self):
        d = datetime.datetime.now()
        dayscount = datetime.timedelta(days=d.isoweekday())
        dayto = d - dayscount
        sixdays = datetime.timedelta(days=6)
        dayfrom = dayto - sixdays
        date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day)
        date_to = datetime.datetime(dayto.year, dayto.month, dayto.day)
        return date_from.strftime('%Y-%m-%d'), date_to.strftime('%Y-%m-%d')

    def getYesterday(self):
        ll = []
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        yesterday_list = '%s,%s' % (yesterday.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))
        ll.append(yesterday_list)
        return ll

    def caculate_date(self, day_num=31):
        date_list = []
        the_date = datetime.datetime.now()
        # date_fmt = datetime.datetime.strptime('日期', '%Y-%m-%d') # 输入日期计算
        yesterday = (the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        before = (the_date - datetime.timedelta(days=day_num)).strftime('%Y-%m-%d')
        date_set = '%s,%s' % (before, yesterday)
        date_list.append(date_set)
        return date_list

















