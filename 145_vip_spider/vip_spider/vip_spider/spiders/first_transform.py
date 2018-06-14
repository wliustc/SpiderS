# -*- coding: utf-8 -*-
import scrapy
import re
from vip_spider.items import VipSpiderItem
import datetime
import time
import json
import web

# http://compass.vis.vip.com/homepage/metric/queryAllMetric?callback=jQuery321028968414347674765_1515059790241&brandStoreName=%E4%BB%96%E5%A5%B9TATA&dateType=D&detailType=D&beginDate=2017-12-05&endDate=2018-01-03&contrastBeginDate=2017-11-05&contrastEndDate=2017-12-04&_=1515059790263

cookie = {'mars_cid': '1512731528747_bc146d76e1fa27e06737a68ddf2b6ea4', 'user_type': '1', 'shop_id': '16769',
          'PHPSESSID': '7m8dn0b01si9s8asf1drqppj23', 'codes': '603480', 'user_id': '66734',
          'token': 'eyJ0b2tlbiI6ImE4MWZiMjIxMmY4OTIxYjU1ZWIxNGI1MDlhMDQwNGJiIiwidG9rZW4xIjoiZWI5MjcxMzYxZTcyODA4MjM5MmI0NWQ3ZGQxYTVmZjAiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJ3Z3VhbkBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjY3MzQiLCJ2aXNTZXNzaW9uSWQiOiI3bThkbjBiMDFzaTlzOGFzZjFkcnFwcGoyMyIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D',
          'compassV': '1.3.1', 'mars_pid': '0',
          'vc_token': 'eyJ0b2tlbiI6ImE4MWZiMjIxMmY4OTIxYjU1ZWIxNGI1MDlhMDQwNGJiIiwidG9rZW4xIjoiZWI5MjcxMzYxZTcyODA4MjM5MmI0NWQ3ZGQxYTVmZjAiLCJ2ZW5kb3JJZCI6IjE2NzY5IiwidXNlck5hbWUiOiJ3Z3VhbkBoaWxsaW5zaWdodC5jb20iLCJ2ZW5kb3JDb2RlIjoiNjAzNDgwIiwidXNlcklkIjoiNjY3MzQiLCJ2aXNTZXNzaW9uSWQiOiI3bThkbjBiMDFzaTlzOGFzZjFkcnFwcGoyMyIsImFwcE5hbWUiOiJ2aXNQQyIsInZpc2l0RnJvbSI6InZjIn0%3D',
          'permission': '_5_6_32_33_34_36_37_38_39_40_41_42_43_44_45_95_96_97_98_99_100_101_105_106_107_108_111_112_114_115_116_117_118_119_121_122_123_126_127_129_130_137_140_142_144_145_147_148_149_150_151_152_153_154_155_156_157_158_178_179_186_187_188_189_190_191_192_193_196_197_200_201_203_204_205_206_207_208_209_210_211_212_213_214_215_217_218_221_222_229_233_234_235_236_242_243_244_245_246_247_248_249_250_251_252_253_254_255_259_260_261_266_277_279_280_282_283_284_288_289_290_293_296_297_302_304_309_310_313_315_316_317_318_319_321_322_323_324_325_333_338_339_340_341_342_343_344_345_356_357_360_363_364_365_366_367_368_369_370_371_372_373_374_375_376_377_378_379_380_381_382_383_387_388_389_392_393_394_407_408_409_414_415_418_419_420_421_422_426_427_428_429_430_431_432_435_436_437_438_439_440_442_449_450_451_452_453_482_491_492_493_494_495_496_504_505_511_512_519_521_522_523_524_525_526_527_528_529_530_531_534_536_541_542_543_544_554_555_556_557_558_559_560_572_575_581_582_586_587_588_590_591_592_594_595_596_600_601_602_605_606_607_608_609_610_614_615_616_619_621_624_625_626_627_628_629_630_631_632_633_634_635_636_637_638_639_641_645_646_648_649_650_651_652_653_654_658_659_660_661_662_663_664_665_666_667_668_674_675_676_677_678_679_680_681_682_683_684_685_686_687_688_689_690_691_692_693_694_695_696_697_698_699_700_701_702_703_704_705_712_714_715_716_717_728_730_731_732_733_734_735_736_737_738_739_740_741_742_743_744_745_746_747_748_749_750_751_752_753_754_755_756_757_758_759_760_761_762_763_764_765_766_767_768_769_770_771_772_773_774_777_778_779_780_783_784_785_786_806_807_808_809_810_811_812_813_814_815_816_817_818_819_820_828_829_',
          'vendor_id': '603480', '_ga': 'GA1.2.1825428114.1512731485',
          'axdata': 'MDkxZmUyNmI2NzgzNjA4NDM2MWVkYTM4OGU3YjYzYzQwYjg4NmQzMjliMTVmNWQ3NGQzOWE0ZDc2YjBmMmQ5Nw%3D%3D',
          'vendor_code': '603480', 'visadminvipvipcom': '7m8dn0b01si9s8asf1drqppj23', 'expire': '1512742788',
          'user': 'wguan%40hillinsight.com', 'nickname': '%E5%85%B3%E7%8E%AE',
          'visit_id': '9C44399271CB4EEB22D632D5528EE510', 'mars_sid': '356f111e78f48d00c57e91d31e110e95',
          '_gid': 'GA1.2.723306915.1512731485', 'shops': '16769', 'jobnumber': '1111'}
brand_list = [
    '他她TATA', '天美意teenmix', '暇步士Hush Puppies', '百丽BeLLE',
    '伐拓F.A.T.O.', '思加图STACCATO', '百思图BASTO', "妙丽Millie's",
    '森达SENDA', 'CAT', 'Bevivo', '真美诗Joy&Peace', 'Istbelle'
]
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

now = datetime.datetime.now()
today = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
before = (now - datetime.timedelta(days=102)).strftime('%Y-%m-%d')
con_end = (now - datetime.timedelta(days=103)).strftime('%Y-%m-%d')
con_begin = (now - datetime.timedelta(days=133)).strftime('%Y-%m-%d')


class First_Table_Spider(scrapy.Spider):
    name = 'tt_spider'

    def start_requests(self):
        crawl_day = datetime.datetime.now().strftime('%Y-%m-%d')
        the_signal = ''
        data = db.query("select sign from t_spider_vip_sign where dt='{}' and spider_name='{}'".format(crawl_day,
                                                                                                       'first_table_spider'))
        for t in data:
            the_signal = t.sign
        if the_signal == '1':
            pass
        else:
            for brand in brand_list:
                url = 'http://compass.vis.vip.com/homepage/metric/queryAllMetric?callback=jQuery3210289684143476747' \
                      '65_{}&brandStoreName={}&dateType=D&detailType=D&beginDate={}&endDate={}&contrastBeginDate={}&co' \
                      'ntrastEndDate={}&_={}'.format(int(time.time() * 1000), brand, before, today,
                                                     con_begin, con_end, int(time.time() * 1000))
                yield scrapy.Request(url, cookies=cookie, callback=self.first_parse, dont_filter=True,
                                     meta={'brand': brand})

    def first_parse(self, response):
        items = VipSpiderItem()
        content = response.body
        content = re.findall('jQuery321028968414347674765_\d+\(([\s\S]*?)\);', content)[0]
        if '"code":"0"' not in content:
            con_json = json.loads(content)
            brand = response.meta['brand']
            # print con_json
            # raw_input("enter")
            sales_list = con_json['singleResult']['chart']['data']['sales'][0]
            cutGoodsMoney_list = con_json['singleResult']['chart']['data']['cutGoodsMoney'][0]
            rejectedPct_list = con_json['singleResult']['chart']['data']['rejectedPct'][0]
            flowUv_list = con_json['singleResult']['chart']['data']['flowUv'][0]
            flowConversion_list = con_json['singleResult']['chart']['data']['flowConversion'][0]
            orderCnt_list = con_json['singleResult']['chart']['data']['orderCnt'][0]
            consumerCount_list = con_json['singleResult']['chart']['data']['consumerCount'][0]
            avgUserSalesAmount_list = con_json['singleResult']['chart']['data']['avgUserSalesAmount'][0]
            avgOrderSalesAmount_list = con_json['singleResult']['chart']['data']['avgOrderSalesAmount'][0]
            stockAmtOnline_list = con_json['singleResult']['chart']['data']['stockAmtOnline'][0]
            stockCntOnline_list = con_json['singleResult']['chart']['data']['stockCntOnline'][0]
            saleStockAmt_list = con_json['singleResult']['chart']['data']['saleStockAmt'][0]
            for i in range(len(sales_list)):
                items['the_date'] = sales_list[i]['x']
                items['brand'] = brand
                items['sales'] = sales_list[i]['y']
                items['cutGoodsMoney'] = cutGoodsMoney_list[i]['y']
                items['rejectedPct'] = rejectedPct_list[i]['y']
                items['flowUv'] = flowUv_list[i]['y']
                items['flowConversion'] = flowConversion_list[i]['y']
                items['orderCnt'] = orderCnt_list[i]['y']
                items['consumerCount'] = consumerCount_list[i]['y']
                items['avgUserSalesAmount'] = avgUserSalesAmount_list[i]['y']
                items['avgOrderSalesAmount'] = avgOrderSalesAmount_list[i]['y']
                items['stockAmtOnline'] = stockAmtOnline_list[i]['y']
                items['stockCntOnline'] = stockCntOnline_list[i]['y']
                items['saleStockAmt'] = saleStockAmt_list[i]['y']

                yield items


