# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import traceback
from daily_taobao.items import DailyTaobaoItem
import time

reload(sys)
sys.setdefaultencoding('utf8')
shop_levels = ['tmall', 'taobao']
citys = ['北京', '天津', '上海', '重庆', '呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布 ', '霍林郭勒市', '满洲里市',
         '牙克石市', '扎兰屯市', '根河市', '额尔古纳市', '丰镇市', '锡林浩特市', '二连浩特市', '乌兰浩特市', '阿尔山市 ', '南宁', '柳州', '桂林', '梧州', '北海',
         '崇左', '来宾', '贺州', '玉林', '百色', '河池', '钦州', '防城港', '贵港 ', '岑溪', '凭祥', '合山', '北流', '宜州', '东兴', '桂平 ', '哈尔滨',
         '大庆', '齐齐哈尔', '佳木斯', '鸡西', '鹤岗', '双鸭山', '牡丹江', '伊春', '七台河', '黑河', '绥化 加格达奇', '五常', '双城', '尚志', '纳河', '虎林',
         '密山', '铁力', '同江', '富锦', '绥芬河', '海林', '宁安', '穆林', '北安', '五大连池', '肇东', '海伦', '安达 ', '长春', '吉林', '四平', '辽源',
         '通化', '白山', '松原', '白城 ', '九台市', '榆树市', '德惠市', '舒兰市', '桦甸市', '蛟河市', '磐石市', '公主岭市', '双辽市', '梅河口市', '集安市',
         '临江市', '大安市', '洮南市', '延吉市', '图们市', '敦化市', '龙井市', '珲春市', '和龙市 ', '沈阳', '大连', '金州', '鞍山', '抚顺', '本溪', '丹东',
         '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛 ', '新民', '瓦房店', '普兰', '庄河', '海城', '东港', '凤城', '凌海', '北镇',
         '大石桥', '盖州', '灯塔', '调兵山', '开原', '凌源', '北票', '兴城 ', '石家庄', '唐山', '邯郸', '秦皇岛', '保定', '张家口', '承德', '廊坊', '沧州',
         '衡水', '邢台 ', '辛集市', '藁城市', '晋州市', '新乐市', '鹿泉市', '遵化市', '迁安市', '武安市', '南宫市', '沙河市', '涿州市', '固安..定州市', '安国市',
         '高碑店市', '泊头市', '任丘市', '黄骅市', '河间市', '霸州市', '三河市', '冀州市', '深州市 .', '济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊',
         '济宁', '泰安', '威海', '日照', '莱芜', '临', '沂', '德州', '聊城', '菏泽', '滨州 ', '章丘', '胶南', '胶州', '平度', '莱西', '即墨', '滕州',
         '龙口', '莱阳', '莱州', '招远', '蓬莱', '栖霞', '海阳', '青州', '诸城', '安丘', '高密', '昌邑', '兖州', '曲阜', '邹城', '乳山', '文登', '荣成',
         '乐陵', '临清', '禹城', '南京', '镇江', '常州', '无锡', '苏州', '徐州', '连云港', '淮安', '盐城', '扬州', '泰州', '南通', '宿迁 ', '江阴市',
         '宜兴市', '邳州市', '新沂市', '金坛市', '溧阳市', '常熟市', '张家港市', '太仓市', '昆山市', '吴江市', '如皋市', '通州市', '海门市', '启东市', '东台市',
         '大丰市', '高邮市', '江都市', '仪征市', '丹阳市', '扬中市', '句容市', '泰兴市', '姜堰市', '靖江市', '兴化市 ', '合肥', '蚌埠', '芜湖', '淮南', '亳州',
         '阜阳', '淮北', '宿州', '滁州', '安庆', '巢湖', '马鞍山', '宣城', '黄山', '池州', '铜陵 ', '界首', '天长', '明光', '桐城', '宁国 ', '杭州',
         '嘉兴', '湖州', '宁波', '金华', '温州', '丽水', '绍兴', '衢州', '舟山', '台州 ', '建德市', '富阳市', '临安市', '余姚市', '慈溪市', '奉化市',
         '瑞安市', '乐清市', '海宁市', '平湖市', '桐乡市', '诸暨市', '上虞市', '嵊州市', '兰溪市', '义乌市', '东阳市', '永康市', '江山市', '临海市', '温岭市',
         '龙泉市 ', '福州', '厦门', '泉州', '三明', '南平', '漳州', '莆田', '宁德', '龙岩 ', '福清市', '长乐市', '永安市', '石狮市', '晋江市', '南安市',
         '龙海市', '邵武市', '武夷山', '建瓯市', '建阳市', '漳平市', '福安市', '福鼎市 ', '广州', '深圳', '汕头', '惠州', '珠海', '揭阳', '佛山', '河源',
         '阳江', '茂名', '湛江', '梅州', '肇庆', '韶关', '潮州', '东莞', '中山', '清远', '江门', '汕尾', '云浮 ', '增城市', '从化市', '乐昌市', '南雄市',
         '台山市', '开平市', '鹤山市', '恩平市', '廉江市', '雷州市 吴川市', '高州市', '化州市', '高要市', '四会市', '兴宁市', '陆丰市', '阳春市', '英德市',
         '连州市', '普宁市', '罗定市 ', '海口', '三亚 ', '琼海', '文昌', '万宁', '五指山', '儋州', '东方 ', '昆明', '曲靖', '玉溪', '保山', '昭通',
         '丽江', '普洱', '临沧 ', '安宁市', '宣威市', '个旧市', '开远市', '景洪市', '楚雄市', '大理市', '潞西市', '瑞丽市 ', '4地级市-贵阳', '六盘水', '遵义',
         '安顺 ', '清镇市', '赤水市', '仁怀市', '铜仁市', '毕节市', '兴义市', '凯里市', '都匀市', '福泉市 ', '成都', '绵阳', '德阳', '广元', '自贡', '攀枝花',
         '乐山', '南充', '内江', '遂宁', '广安', '泸州', '达州', '眉山', '宜宾', '雅安', '资阳 ', '都江堰市', '彭州市', '邛崃市', '崇州市', '广汉市',
         '什邡市', '绵竹市', '江油市', '峨眉山市', '阆中市', '华蓥市', '万源市', '简阳市', '西昌市 ', '13地级市-长沙', '株洲', '湘潭', '衡阳', '岳阳', '郴州',
         '永州', '邵阳', '怀化', '常德', '益阳', '张家界', '娄底 ', '浏阳市', '醴陵市', '湘乡市', '韶山市', '耒阳市', '常宁市', '武冈市', '临湘市', '汨罗市',
         '津市市', '沅江市', '资兴市', '洪江市', '冷水江市', '涟源市', '吉首市 ', '武汉', '襄樊', '宜昌', '黄石', '鄂州', '随州', '荆州', '荆门', '十堰',
         '孝感', '黄冈', '咸宁 ', '大冶市', '丹江口市', '洪湖市', '石首市', '松滋市', '宜都市', '当阳市', '枝江市', '老河口市', '枣阳市', '宜城市', '钟祥市',
         '应城市', '安陆市', '汉川市', '麻城市', '武穴市', '赤壁市', '广水市', '仙桃市', '天门市', '潜江市', '恩施市', '利川市 ', '郑州', '洛阳', '开封',
         '漯河', '安阳', '新乡', '周口', '三门峡', '焦作', '平顶山', '信阳', '南阳', '鹤壁', '濮阳', '许昌', '商丘', '驻马店 ', '巩义市', '新郑市',
         '新密市', '登封市', '荥阳市', '偃师市', '汝州市', '舞钢市', '林州市', '卫辉市', '辉县市', '沁阳市', '孟州市', '禹州市', '长葛市', '义马市', '灵宝市',
         '邓州市', '永城市', '项城市', '济源市 ', '太原', '大同', '忻州', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '临汾', '吕梁 ', '古交', '潞城',
         '高平', '介休', '永济', '河津', '原平', '侯马', '霍州', '孝义', '汾阳 ', '西安', '咸阳', '铜川', '延安', '宝鸡', '渭南', '汉中', '安康',
         '商洛', '榆林 ', '兴平市', '韩城市', '华阴市 ', '兰州', '天水', '平凉', '酒泉', '嘉峪关', '金昌', '白银', '武威', '张掖', '庆阳', '定西',
         '陇南 ', '玉门市', '敦煌市', '临夏市', '合作市 ', '西宁 ', '格尔木', '德令哈 ', '南昌', '九江', '赣州', '吉安', '鹰潭', '上饶', '萍乡', '景德镇',
         '新余', '宜春', '抚州 ', '乐平市', '瑞昌市', '贵溪市', '瑞金市', '南康市', '井冈山市', '丰城市', '樟树市', '高安市', '德兴市 ', '台北', '台中',
         '基隆', '高雄', '台南', '新竹', '嘉义 ', '板桥市', '宜兰市', '竹北市', '桃园市', '苗栗市', '丰原市', '彰化市', '南投市', '太保市', '斗六市', '新营市',
         '凤山市', '屏东市', '台东市', '花莲市', '马公市 ', '中西区', '东区', '九龙城区', '观塘区', '南区', '深水埗区', '黄大仙区', '湾仔区', '油尖旺区', '离岛区',
         '葵青区', '北区', '西贡区', '沙田区', '屯门区', '大埔区', '荃湾区', '元朗区']

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

cate_list = ['50468018',  '54176002',  '50466013',  '50480016',  '50029587',  '54186001',  '50038571',  '50464021',
             '50476014',  '50023636',  '50038718',  '50071817',  '50474022',  '54168001',  '54168002',  '50458014',
             '50484019',  '50484020',  '54204001',  '50470025',  '50470026', '50334022', '50334023', '50346028',
             '55812024', '50356016', '50342020', '55876020', '50354024', '50340023', '55822030', '55938014',
             '55848034', '55844029']



class All_cate_list(scrapy.Spider):

    name = 'allcate_spider'

    def __init__(self, file_path='', *args, **kwargs):
        super(All_cate_list, self).__init__(*args, **kwargs)
        self.file_path = file_path

    def start_requests(self):
        # with open(self.file_path, 'rb') as f:
        #     lines = f.readlines()
        for line in cate_list:
            for level in shop_levels:
                for city in citys:
                    baseurl = 'https://s.taobao.com/list?imgfile=&js=1&stats_click=search_radio_all%3A1&initiati' \
                              've_id=staobaoz_20161213&ie=utf8&sort=sale-desc&cps=yes&bcoffset=0&data_value=60&' \
                              'ajax=true&cat={}&seller_type={}&loc={}'.format(line, level, city)
                    baseurl = baseurl.strip()
                    yield scrapy.Request(baseurl, headers=header, callback=self.parse_json1, dont_filter=True, meta=
                    {'fg_category_id': line, 'level': level, 'city': city})
                yield scrapy.Request('https://s.taobao.com/list?imgfile=&js=1&stats_click=search_radio_all%3A1&init'
                                     'iative_id=staobaoz_20161213&ie=utf8&sort=sale-desc&cps=yes&bcoffset=0&data_v'
                                     'alue=60&ajax=true&cat={}&seller_type={}'.format(line, level), headers=header,
                                     callback=self.parse_json2, dont_filter=True, meta={'fg_category_id': line, 'level': level})

    def parse_json1(self, response):
        jstr = json.loads(response.body.replace("'", '"'))
        fg_category_id = response.meta['fg_category_id']
        level = response.meta['level']
        city = response.meta['city']
        if 'login' in response.url:
            baseurl = 'https://s.taobao.com/list?imgfile=&js=1&stats_click=search_radio_all%3A1&initiati' \
                      've_id=staobaoz_20161213&ie=utf8&sort=sale-desc&cps=yes&bcoffset=0&data_value=60&' \
                      'ajax=true&cat={}&seller_type={}&loc={}'.format(fg_category_id, level, city)
            baseurl = baseurl.strip()
            yield scrapy.Request(baseurl, headers=header, callback=self.parse_json1, dont_filter=True, meta=
            {'fg_category_id': fg_category_id, 'level': level, 'city': city})
        else:
            try:
                # 根据count 提取，生成分页url
                total = jstr['mods']['sortbar']['data']['pager']['totalCount']
                total = 10200 if total > 10200 else total
                for page in range(60, total, 60):
                    baseurl2 = response.url + '&s={}'.format(page)
                    yield scrapy.Request(baseurl2, callback=self.parse2, dont_filter=True, meta={'fg_category_id':
                                                                                                     fg_category_id})

            except:
                traceback.print_exc()

    def parse_json2(self, response):
        jstr = json.loads(response.body.replace("'", '"'))
        fg_category_id = response.meta['fg_category_id']
        level = response.meta['level']
        if 'login' in response.url:
            yield scrapy.Request('https://s.taobao.com/list?imgfile=&js=1&stats_click=search_radio_all%3A1&init'
                                 'iative_id=staobaoz_20161213&ie=utf8&sort=sale-desc&cps=yes&bcoffset=0&data_v'
                                 'alue=60&ajax=true&cat={}&seller_type={}'.format(fg_category_id, level), headers=header,
                                 callback=self.parse_json2, dont_filter=True,
                                 meta={'fg_category_id': fg_category_id, 'level': level})
        else:
            try:
                # 根据count 提取，生成分页url
                total = jstr['mods']['sortbar']['data']['pager']['totalCount']
                total = 10200 if total > 10200 else total
                for page in range(60, total, 60):
                    baseurl2 = response.url + '&s={}'.format(page)
                    yield scrapy.Request(baseurl2, callback=self.parse2, dont_filter=True, meta={'fg_category_id':
                                                                                                     fg_category_id})

            except:
                traceback.print_exc()

    def parse2(self, response):
        items = DailyTaobaoItem()
        jstr = json.loads(response.body.replace("'", '"'))
        fg_category_id = response.meta['fg_category_id']
        try:
            goods_list = jstr['mods']['itemlist']['data']['auctions']
            for goods_info in goods_list:
                goods_id = goods_info['nid']
                shop_url = goods_info['shopLink']
                category_id = goods_info['category']
                user_id = goods_info['user_id']
                shop_name = goods_info['nick']
                dt = time.strftime('%Y-%m-%d', time.localtime())
                items['goods_id'] = goods_id
                items['shop_url'] = shop_url
                items['category_id'] = category_id
                items['fg_category_id'] = fg_category_id.strip()
                items['user_id'] = user_id
                items['shop_name'] = shop_name
                items['dt'] = dt

                yield items
        except:
            traceback.print_exc()