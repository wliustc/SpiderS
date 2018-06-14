# -*- coding: utf-8 -*-
'''女鞋-唯品会-档期-档期分析-流量分析-档期流量入口分布-本档期'''
import scrapy
import datetime
import json
import urllib
import re
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


cookie = {'mars_cid': '1528247823194_33dd74571b8e3803f235d8b5bb8f0363', 'user_type': '1', 'shop_id': '16769', 'PHPSESSID': '6lr3bnv2i3q3lhccnlicrra790', 'codes': '603480', 'user_id': '77419', 'mars_sid': 'd0b63f96ade34c340623cae9fc289145', 'compassV': '2.4', 'guideV': '2.3', 'mars_pid': '0', 'vc_token': 'eyJ0b2tlbiI6IjU3MDYxMzBhYTQ3NDA4ODU0MGUxMDVhZjFmZWRhNmIwIiwidG9rZW4xIjoiODY3NGM3YTk0ZDE5NjFlOWU3M2MwYWUyNzkzZTAyNTkiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJzcGlkZXJfbml1QHNpbmEuY29tIiwidmVuZG9yQ29kZSI6IjYwMzQ4MCIsInVzZXJJZCI6Ijc3NDE5IiwidmlzU2Vzc2lvbklkIjoiNmxyM2JudjJpM3EzbGhjY25saWNycmE3OTAiLCJhcHBOYW1lIjoidmlzUEMiLCJ2aXNpdEZyb20iOiJ2YyJ9', 'permission': '_5_6_32_33_34_36_37_38_39_40_41_42_43_44_45_61_63_64_65_66_67_68_69_70_71_72_95_96_97_98_99_100_101_105_106_107_108_111_112_114_115_116_117_118_119_121_122_123_126_127_129_130_137_140_142_144_145_147_148_149_150_151_152_153_154_155_156_157_158_178_179_186_187_188_189_190_191_192_193_194_196_197_200_201_203_204_205_206_207_208_209_210_211_212_213_214_215_216_217_218_219_220_221_222_229_232_233_234_235_236_238_240_241_242_243_244_245_246_247_248_249_250_251_252_253_254_255_259_260_261_266_277_279_280_282_283_284_288_289_290_293_294_295_296_297_298_299_300_301_302_303_304_305_306_309_310_313_315_316_317_318_319_320_321_322_323_324_325_327_328_333_336_337_338_339_340_341_342_343_344_345_348_350_352_354_356_357_358_360_363_364_365_366_367_368_369_370_371_372_373_374_375_376_377_378_379_380_381_382_383_387_388_389_391_392_393_394_407_408_409_414_415_418_419_420_421_422_426_427_428_429_430_431_432_435_436_437_438_439_440_442_449_450_451_452_453_481_482_483_491_492_493_494_495_496_497_498_499_504_505_511_512_513_514_519_521_522_523_525_526_527_528_530_531_534_535_536_541_542_543_544_545_546_547_548_549_550_551_552_553_554_555_556_557_558_559_560_572_581_582_583_584_585_586_587_588_589_590_591_592_594_595_596_600_601_602_605_606_607_608_609_610_613_614_615_616_619_632_633_634_635_636_637_638_639_640_641_645_646_648_649_650_651_652_653_654_658_659_660_661_662_663_664_665_666_667_668_674_675_676_677_678_679_680_681_682_683_684_685_686_687_688_689_690_691_692_693_694_695_696_697_698_699_700_701_702_703_704_705_712_714_715_716_717_728_730_731_732_733_734_735_736_737_738_739_740_741_742_743_744_745_746_747_748_749_750_751_752_753_754_755_756_757_758_759_760_761_762_763_764_765_766_767_768_769_770_771_772_773_774_777_778_779_780_783_784_785_786_790_806_807_808_809_810_811_812_813_814_815_816_817_818_819_820_822_823_824_825_826_827_828_829_830_834_835_836_837_838_839_840_841_842_843_844_845_846_847_848_849_850_851_855_856_857_858_859_860_861_862_863_864_865_866_871_872_875_876_877_878_879_880_881_882_883_886_893_894_895_896_897_898_899_900_901_902_903_904_905_906_907_908_909_910_911_912_913_914_915_916_918_919_920_921_926_927_928_929_', 'vendor_id': '603480', '_ga': 'GA1.2.1789872469.1528247808', 'axdata': 'OTc0MzRjM2FhMmY1MmQ4NDkwYzc2ZjIyMDk2NThlYThhMGUyYTU3MTZjZDIzZDhlNGRjMTc0MGY4YTYxODQ3NQ%3D%3D', 'vendor_code': '603480', 'visadminvipvipcom': '6lr3bnv2i3q3lhccnlicrra790', 'expire': '1528269422', 'user': 'spider_niu%40sina.com', 'nickname': '%E7%8E%8B%E5%BE%8B%E6%99%8B', 'visit_id': 'BE55F5B081165B09D1B028D9A48E54B1', 'token': 'eyJ0b2tlbiI6IjU3MDYxMzBhYTQ3NDA4ODU0MGUxMDVhZjFmZWRhNmIwIiwidG9rZW4xIjoiODY3NGM3YTk0ZDE5NjFlOWU3M2MwYWUyNzkzZTAyNTkiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJzcGlkZXJfbml1QHNpbmEuY29tIiwidmVuZG9yQ29kZSI6IjYwMzQ4MCIsInVzZXJJZCI6Ijc3NDE5IiwidmlzU2Vzc2lvbklkIjoiNmxyM2JudjJpM3EzbGhjY25saWNycmE3OTAiLCJhcHBOYW1lIjoidmlzUEMiLCJ2aXNpdEZyb20iOiJ2YyJ9', 'tipInfoV': '2.3', '_gid': 'GA1.2.1557292532.1528247808', 'shops': '16769', 'jobnumber': '0'}

dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class WeipinHistorySpider(scrapy.Spider):
    name = 'dangqi_dangqifenxi_liuliang'
    allowed_domains = ['vis.vip.com']

    def start_requests(self):
        brand_list = [
            #'Bata',
            '他她TATA', '天美意teenmix', '暇步士Hush Puppies', '百丽BeLLE',
            '伐拓F.A.T.O.', '思加图STACCATO', '百思图BASTO', "妙丽Millie's",
            '森达SENDA', 'CAT', 'Bevivo', '真美诗Joy&Peace', 'Istbelle', 'Bata','15MINS'
        ]
        for brand in brand_list:
            print brand
            url = 'http://compass.vis.vip.com/dangqi/evaluation/queryTimeLineEvaluation?brandStoreName='+urllib.quote(brand)
            yield scrapy.Request(url, callback=self.parse, headers=header, meta={'brand': brand},
                                    cookies=cookie)

    def parse(self, response):
        try:
            brand = response.meta.get('brand')
            content_json = json.loads(response.body)
            singleResult = content_json.get('singleResult')
            if singleResult:
                contrastBrandList = singleResult[1]
                contrastBrandName = contrastBrandList['brandName']
                contrastBrandName = contrastBrandName.encode('utf-8')
                print contrastBrandName
                for i in singleResult:
                    brandName = i.get('brandName')
                    brandName = brandName.encode('utf-8')
                    brandType = i.get("brandType")
                    brandType = brandType.encode('utf-8')
                    firstSellDay = i.get('firstSellDay')
                    lastSellDay = i.get('lastSellDay')
                    brandSellDay = i.get('brandSellDay')
                    url = 'http://compass.vis.vip.com/dangqi/traffic/queryTrafficEntrance?brandStoreName=' + \
                            urllib.quote(brand) + '&brandName=' + urllib.quote(brandName) + \
                            '&contrastType=0&contrastBrandName=' + \
                            urllib.quote(contrastBrandName)
                    print url
                    yield scrapy.Request(url, callback=self.parse_content, headers=header,
                                         meta={'brand': brand, 'dt': dt,
                                               'updateTime':updateTime,'firstSellDay':firstSellDay,
                                               'lastSellDay':lastSellDay,'brandType':brandType,'brandName':brandName
                                               },
                                         cookies=cookie)
        except:
            pass

    def parse_content(self,response):
        try:
            content_json = json.loads(response.body)
            singleResult = content_json.get('singleResult')
            if singleResult:
                chart = singleResult.get('chart')
                if chart:
                    data = chart.get('data')
                    if data:
                        flowUv = data.get('flowUv')
                        if flowUv:
                            item = WeipinItem()
                            item['content'] = response.body
                            item['meta'] = response.meta
                            yield item

        except:
            pass


    