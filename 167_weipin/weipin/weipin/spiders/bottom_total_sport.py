# -*- coding: utf-8 -*-
'''运动-唯品会-档期-档期详情-合计查看-全部（增量每30天） 最下边'''
import scrapy
import datetime
import json
import urllib

import time
import web
from weipin.items import WeipinItem

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

cookie = {
    'user_id': '68384',
    'vendor_code': '605599',
}

dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class DangqiHejiSpider(scrapy.Spider):
    name = 'bottom_total_sport'
    allowed_domains = ['vis.vip.com']

    def __init__(self, select_date='yesterday', *args, **kwargs):
        super(DangqiHejiSpider, self).__init__(*args, **kwargs)
        if select_date == 'yesterday':
            self.select_date = self.caculate_date()
        else:
            ll = []
            ll.append(select_date)
            self.select_date = ll

    def start_requests(self):
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
        for brand in brand_list:
            url = 'http://compass.vis.vip.com/dangqi/details/queryTimeLineDetail?brandStoreName=' + urllib.quote(
                brand)
            yield scrapy.Request(url, callback=self.parse, headers=header, meta={'brand': brand,'dt':dt,'updateTime':updateTime},
                                 cookies=cookie)

    def parse(self, response):
        try:
            brand = response.meta.get('brand')
            # print response.body
            content_json = json.loads(response.body)
            singleResult = content_json.get('singleResult')
            if singleResult:
                for i in singleResult:
                    lastSellDay = i.get('lastSellDay')
                    brandType = i.get('brandType')
                    brandType = brandType.encode('utf-8')
                    brandName = i.get('brandName')
                    brandName = brandName.encode('utf-8')
                    for dd in self.getYesterday():
                        dd_ = dd.split(',')
                        #print dd_
                        if lastSellDay >= dd_[0]:
                            for dd2 in self.select_date:
                                dd_2 = dd2.split(',')
                                #print dd_2
                                url = 'http://compass.vis.vip.com/dangqi/details/getDangqiDetails?&brandStoreName=' + urllib.quote(
                                    brand) + '&brandType=' + urllib.quote(brandType) + '&brandName=' + urllib.quote(
                                    brandName) + \
                                      '&mixBrand=0&sortColumn=salesAmount&sortType=1&pageSize=200000&pageNumber=1&sumType=0&lv3CategoryFlag=0&optGroupFlag=0&warehouseFlag=0&analysisType=1&beginDate=' + \
                                      dd_2[0] + '&endDate=' + dd_2[1] + '&queryType=0'
                                print url
                                yield scrapy.Request(url, callback=self.parse_content, headers=header,
                                                     meta={'brand': brand, 'dt': dt,'updateTime':updateTime},
                                                     cookies=cookie)
        except:
            pass

    def parse_content(self, response):
        try:
            content_json = json.loads(response.body)
            singleResult = content_json.get('singleResult')
            if singleResult:
                list = singleResult.get('list')
                if list:
                    item = WeipinItem()
                    item['content'] = response.body
                    item['meta'] = response.meta
                    yield item

                else:
                    pass
        except:
            pass

    # 昨天
    def getYesterday(self):
        ll = []
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        yesterday_list = '%s,%s' % (yesterday.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))
        ll.append(yesterday_list)
        return ll

    # 最近三十天
    def caculate_date(self, day_num=31):
        date_list = []
        the_date = datetime.datetime.now()
        # date_fmt = datetime.datetime.strptime('日期', '%Y-%m-%d') # 输入日期计算
        yesterday = (the_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        before = (the_date - datetime.timedelta(days=day_num)).strftime('%Y-%m-%d')
        date_set = '%s,%s' % (before, yesterday)
        date_list.append(date_set)
        return date_list

    
    