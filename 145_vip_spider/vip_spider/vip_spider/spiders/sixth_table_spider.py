# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import SixthTableItem
import datetime
import time
import json
import web

#cookie = {'mars_cid': '1512735638623_3a93402dbb3f77596716b5fd1981966b', 'user_type': '1', 'shop_id': '16769', 'PHPSESSID': 'uqndls4tmjtjv1667642ujh126', 'codes': '603480', 'user_id': '68122', 'token': 'eyJ0b2tlbiI6ImRhZDVjZDU0MDEzNzJhZDE5ZDYyNDMxMmM5ZjA1YmQ1IiwidG9rZW4xIjoiMWI4OGMxY2E0NTEzYzcxMDdjZjhhOGE4NjE2OWYxMWQiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJoYm5pdUBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjgxMjIiLCJ2aXNTZXNzaW9uSWQiOiJ1cW5kbHM0dG1qdGp2MTY2NzY0MnVqaDEyNiIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D', 'compassV': '2.4', 'guideV': '2.3', 'mars_pid': '0', 'vc_token': 'eyJ0b2tlbiI6ImRhZDVjZDU0MDEzNzJhZDE5ZDYyNDMxMmM5ZjA1YmQ1IiwidG9rZW4xIjoiMWI4OGMxY2E0NTEzYzcxMDdjZjhhOGE4NjE2OWYxMWQiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJoYm5pdUBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjgxMjIiLCJ2aXNTZXNzaW9uSWQiOiJ1cW5kbHM0dG1qdGp2MTY2NzY0MnVqaDEyNiIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D', 'permission': '_5_6_32_33_34_36_37_38_39_40_41_42_43_44_45_61_63_64_65_66_67_68_69_70_71_72_95_96_97_98_99_100_101_105_106_107_108_111_112_114_115_116_117_118_119_121_122_123_126_127_129_130_137_140_142_144_145_147_148_149_150_151_152_153_154_155_156_157_158_178_179_186_187_188_189_190_191_192_193_194_196_197_200_201_203_204_205_206_207_208_209_210_211_212_213_214_215_216_217_218_219_220_221_222_229_232_233_234_235_236_238_240_241_242_243_244_245_246_247_248_249_250_251_252_253_254_255_259_260_261_266_277_279_280_282_283_284_288_289_290_293_294_295_296_297_298_299_300_301_302_303_304_305_306_309_310_313_315_316_317_318_319_320_321_322_323_324_325_327_328_333_336_337_338_339_340_341_342_343_344_345_348_350_352_354_356_357_358_360_363_364_365_366_367_368_369_370_371_372_373_374_375_376_377_378_379_380_381_382_383_387_388_389_391_392_393_394_407_408_409_414_415_418_420_421_422_426_427_428_429_430_431_432_435_436_437_438_439_440_442_449_450_451_452_453_481_482_483_491_492_493_494_495_496_497_498_499_504_505_511_512_513_514_519_521_522_523_525_526_527_528_530_531_534_535_536_541_542_543_544_545_546_547_548_549_550_551_552_553_554_555_556_557_558_559_560_572_581_582_583_584_585_586_587_588_589_590_591_592_594_596_600_601_602_605_606_607_608_609_610_613_614_615_616_619_632_633_634_635_636_637_638_639_640_641_645_646_648_649_650_651_652_653_654_658_659_660_661_662_663_664_665_666_667_668_674_675_676_677_678_679_680_681_682_683_684_685_686_687_688_689_690_691_692_693_694_695_696_697_698_699_700_701_702_703_704_705_712_714_715_716_717_728_730_731_732_733_734_735_736_737_738_739_740_741_742_743_744_745_746_747_748_749_750_751_752_753_754_755_756_757_758_759_760_761_762_763_764_765_766_767_768_769_770_771_772_773_774_777_778_779_780_783_784_785_786_790_806_807_808_809_810_811_812_813_814_815_816_817_818_819_820_822_823_824_825_826_827_828_829_830_834_835_836_837_838_839_840_841_842_843_844_845_846_847_848_849_850_851_855_856_857_858_859_860_861_862_863_864_865_866_871_872_875_876_877_878_879_880_881_882_883_886_893_894_895_896_897_898_899_900_901_902_903_904_905_906_907_908_909_910_911_912_913_914_915_916_918_919_920_921_926_927_928_929_', 'vendor_id': '603480', '_ga': 'GA1.2.839822030.1512735589', 'vendor_code': '603480', 'axdata': 'YzVmNTI1MzNiZDZjNjA5YThlNDY5YzJkNTVmMWNhOTBhOWNlZWY3OWRkZjI0M2QzOTg4ZDdmOTdlOTM0ZDBkNg%3D%3D', 'visadminvipvipcom': 'uqndls4tmjtjv1667642ujh126', 'expire': '1528863783', 'user': 'hbniu%40hillinsight.com', 'nickname': '%E7%89%9B%E6%B4%AA%E6%96%8C', '_gat': '1', 'visit_id': '4D4E3AB12952D86B681F1B112FB1701B', 'mars_sid': '879b6f4049cb1b91337d84093aa147c5', 'tipInfoV': '2.3', '_gid': 'GA1.2.1855378962.1528770010', 'shops': '16769', 'jobnumber': '0'}
import ast
db2 = web.database(dbn='mysql', db='belle', user='yougou', pw='09E636cd', port=3306,
                  host='rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com')

data = db2.query('select cookie from t_spider_vip_sign_cookie;')
cookie = data[0].get('cookie')
cookie = ast.literal_eval(cookie)
brand_list = [
    '他她TATA', '天美意teenmix', '暇步士Hush Puppies', '百丽BeLLE',
    '伐拓F.A.T.O.', '思加图STACCATO', '百思图BASTO', "妙丽Millie's",
    '森达SENDA', 'CAT', 'Bevivo', '真美诗Joy&Peace', 'Istbelle'
]
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
now = datetime.datetime.now()
today = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
#before = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
before = '2017-10-01'


class Sixth_Table_Spider(scrapy.Spider):

    name = 'sixth_table_spider'

    def start_requests(self):
        crawl_day = datetime.datetime.now().strftime('%Y-%m-%d')
        the_signal = ''
        data = db.query("select sign from t_spider_vip_sign where dt='{}' and spider_name='{}'".format(crawl_day,
                                                                                                       'sixth_table_spider'))
        for t in data:
            the_signal = t.sign
        if the_signal == '1':
            pass
        else:
            for brand in brand_list:
                url = 'http://compass.vis.vip.com/dangqi/reject/getRejectOverview?callback=jQuery32108590923814259758_{}' \
                      '&brandStoreName={}&dateType=D&detailType=D&beginDate={}&endDate={}&_={}'.format\
                    (int(time.time()*1000), brand, before, today, int(time.time()*1000))
                yield scrapy.Request(url, callback=self.json_parse, cookies=cookie, dont_filter=True, meta={'brand': brand})

    def json_parse(self, response):
        content = response.body
        brand = response.meta['brand']
        items = SixthTableItem()
        content = re.findall('jQuery32108590923814259758_\d+\((.*?)\);', content)[0]
        if '"code":"1"' in content:
            json_con = json.loads(content)
            gmv_list = json_con['singleResult']['chart']['data']['sales'][0]
            sales_list = json_con['singleResult']['chart']['data']['salesCnt'][0]
            return_list = json_con['singleResult']['chart']['data']['salesReturnCnt'][0]
            return_gmv_list = json_con['singleResult']['chart']['data']['salesReturnAmt'][0]
            ReturnPercent_list = json_con['singleResult']['chart']['data']['salesReturnPercent'][0]
            reject_list = json_con['singleResult']['chart']['data']['rejectCnt'][0]
            reject_gmv_list = json_con['singleResult']['chart']['data']['rejectAmt'][0]
            rejectPercent_list = json_con['singleResult']['chart']['data']['rejectPercent'][0]
            returnPercent_list2 = json_con['singleResult']['chart']['data']['returnPercent'][0]
            date_list = json_con['singleResult']['chart']['scale']
            for i in range(len(date_list)):
                items['the_date'] = date_list[i]
                items['brand'] = brand
                items['sales'] = gmv_list[i]['y']
                items['salesCnt'] = sales_list[i]['y']
                items['salesReturnCnt'] = return_list[i]['y']
                items['salesReturnAmt'] = return_gmv_list[i]['y']
                items['salesReturnPercent'] = ReturnPercent_list[i]['y']
                items['rejectCnt'] = reject_list[i]['y']
                items['rejectAmt'] = reject_gmv_list[i]['y']
                items['rejectPercent'] = rejectPercent_list[i]['y']
                items['returnPercent'] = returnPercent_list2[i]['y']

                yield items

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    