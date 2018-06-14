# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import RealTimeItem
import datetime
import time
import json
import web
# http://compass.vis.vip.com/newRealTime/situation/overview?callback=jQuery331037277410744833206_1521016821249&brandStoreName=他她TATA&_=1521016821252

cookie = {'mars_cid': '527524167752_067b876843a64520469300ec561eecd1', 'user_type': '1', 'shop_id': '16769',
          #'PHPSESSID': '4a7kciqthgmbhal7ijs4916dk1',
          'codes': '603480', 'user_id': '77419',
          #'token': 'eyJ0b2tlbiI6ImM2OTg5YzAwY2Q3NjUxMzRiYWFkN2Q0YTcxYWI5YTdjIiwidG9rZW4xIjoiNGZlZGY2MzQ5ZDcyNjIxMGI0YjJjNGZiOTM1ZWFlMDEiLCJ2ZW5kb3JJZCI6IjE4ODk0IiwidXNlck5hbWUiOiJ5bGluQGhpbGxpbnNpZ2h0LmNvbSIsInZlbmRvckNvZGUiOiI2MDU1OTkiLCJ1c2VySWQiOiI2ODM4NCIsInZpc1Nlc3Npb25JZCI6IjRhN2tjaXF0aGdtYmhhbDdpanM0OTE2ZGsxIiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D',
          'compassV': '2.2', 'mars_pid': '0',
          'vc_token': 'eyJ0b2tlbiI6IjU3MDYxMzBhYTQ3NDA4ODU0MGUxMDVhZjFmZWRhNmIwIiwidG9rZW4xIjoiODY3NGM3YTk0ZDE5NjFlOWU3M2MwYWUyNzkzZTAyNTkiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJzcGlkZXJfbml1QHNpbmEuY29tIiwidmVuZG9yQ29kZSI6IjYwMzQ4MCIsInVzZXJJZCI6Ijc3NDE5IiwidmlzU2Vzc2lvbklkIjoicHFoanVqMGExcXU1ZmgwYW9oZ2I1bTJqajAiLCJhcHBOYW1lIjoidmlzUEMiLCJ2aXNpdEZyb20iOiJ2YyJ9',
          'permission': '_5_6_32_33_34_36_37_38_39_40_41_42_43_44_45_61_63_64_65_66_67_68_69_70_71_72_95_96_97_98_99_100_101_105_106_107_108_111_112_114_115_116_117_118_119_121_122_123_126_127_129_130_137_140_142_144_145_147_148_149_150_151_152_153_154_155_156_157_158_178_179_186_187_188_189_190_191_192_193_194_196_197_200_201_203_204_205_206_207_208_209_210_211_212_213_214_215_216_217_218_219_220_221_222_229_232_233_234_235_236_238_240_241_242_243_244_245_246_247_248_249_250_251_252_253_254_255_259_260_261_266_277_279_280_282_283_284_288_289_290_293_294_295_296_297_298_299_300_301_302_303_304_305_306_309_310_313_315_316_317_318_319_320_321_322_323_324_325_327_328_333_336_337_338_339_340_341_342_343_344_345_348_350_352_354_356_357_358_360_363_364_365_366_367_368_369_370_371_372_373_374_375_376_377_378_379_380_381_382_383_387_388_389_391_392_393_394_407_408_409_414_415_418_419_420_421_422_426_427_428_429_430_431_432_435_436_437_438_439_440_442_449_450_451_452_453_481_482_483_491_492_493_494_495_496_497_498_499_504_505_511_512_513_514_519_521_522_523_525_526_527_528_530_531_534_535_536_541_542_543_544_545_546_547_548_549_550_551_552_553_554_555_556_557_558_559_560_572_581_582_583_584_585_586_587_588_589_590_591_592_594_595_596_600_601_602_605_606_607_608_609_610_613_614_615_616_619_621_624_625_626_627_628_629_630_631_632_633_634_635_636_637_638_639_640_641_645_646_648_649_650_651_652_653_654_658_659_660_661_662_663_664_665_666_667_668_674_675_676_677_678_679_680_681_682_683_684_685_686_687_688_689_690_691_692_693_694_695_696_697_698_699_700_701_702_703_704_705_712_714_715_716_717_728_730_731_732_733_734_735_736_737_738_739_740_741_742_743_744_745_746_747_748_749_750_751_752_753_754_755_756_757_758_759_760_761_762_763_764_765_766_767_768_769_770_771_772_773_774_777_778_779_780_783_784_785_786_790_806_807_808_809_810_811_812_813_814_815_816_817_818_819_820_822_823_824_825_826_827_828_829_830_834_835_836_837_838_839_840_841_842_843_844_845_846_847_848_849_850_851_855_856_857_858_859_860_861_862_863_864_865_866_871_872_875_876_877_878_879_880_881_882_883_886_893_894_895_896_897_898_899_900_901_902_903_904_905_906_907_908_909_910_911_912_913_914_915_916_918_919_920_921_926_927_',
          'vendor_id': '603480', '_ga': 'GA1.2.433714787.1527524150', 'vendor_code': '603480',
          'axdata': 'OTc0MzRjM2FhMmY1MmQ4NDkwYzc2ZjIyMDk2NThlYTg3NTlhODQ5NTk1OGVjYTk3OTkxYTVkMGEzZDc4NzcxMw%3D%3D',
          'visadminvipvipcom': 'pqhjuj0a1qu5fh0aohgb5m2jj0', 'expire': '1527750966', 'user': 'spider_niu%40sina.com',
          'nickname': '%8E%8B%E5%BE%8B%E6%99%8B',  'visit_id': '0188977194411527142F63F128A1B36',
          'mars_sid': '36b107b8084788bb212428454e29e1ec', '_gid': 'GA1.2.1155273203.1527524150', 'shops': '16769',
          'jobnumber': '0'}
brand_list = [
    '他她TATA', '天美意teenmix', '暇步士Hush Puppies', '百丽BeLLE',
    '伐拓F.A.T.O.', '思加图STACCATO', '百思图BASTO', "妙丽Millie's",
    '森达SENDA', 'CAT', 'Bevivo', '真美诗Joy%26Peace', 'Istbelle','Bata'
]
db = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306, host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')


class Realtime_Spider(scrapy.Spider):

    name = 'realtime_spider'
    sum_sales = 0
    brand_num = 0
    total_item = []

    def start_requests(self):
        for brand in brand_list:
            url = 'http://compass.vis.vip.com/newRealTime/situation/overview?callback=jQuery331037277410744833206_1521016821249&brandStoreName={}&_={}'.format(brand, int(time.time()*1000))
            yield scrapy.Request(url, cookies=cookie, callback=self.real_parse, dont_filter=True, meta={'brand': brand})

    def real_parse(self, response):
        content = response.body
        items = RealTimeItem()
        Realtime_Spider.brand_num += 1
        content = re.findall('jQuery331037277410744833206_\d+\(([\s\S]*?)\);', content)[0]
        if '"code":"0"' not in content:
            con_json = json.loads(content)
            if con_json['singleResult']['sum_data']['sales'] != '':
                Realtime_Spider.sum_sales = Realtime_Spider.sum_sales + float(con_json['singleResult']['sum_data']['sales'])
            brand = response.meta['brand']
            if brand == '真美诗Joy%26Peace':
                brand = '真美诗Joy&Peace'
            items['brand'] = brand
            items['the_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            items['sales'] = con_json['singleResult']['sum_data']['sales']
            items['uv'] = con_json['singleResult']['sum_data']['uv']
            items['consumerCount'] = con_json['singleResult']['sum_data']['consumerCount']
            items['conversion'] = con_json['singleResult']['sum_data']['conversion']
            items['unitPrice'] = con_json['singleResult']['sum_data']['unitPrice']
            items['salesAmount'] = con_json['singleResult']['sum_data']['salesAmount']
            items['orderCnt'] = con_json['singleResult']['sum_data']['orderCnt']
            Realtime_Spider.total_item.append(items)
        if Realtime_Spider.brand_num == 14 and Realtime_Spider.sum_sales != 0:
            for item in Realtime_Spider.total_item:
                yield item
    
    
    
    
    
    
    
    