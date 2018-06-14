# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import time
import re
from weather.items import Weatherhttp2Item
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class TianqihoubaoSpider(scrapy.Spider):
    name = "tianqihoubao"
    allowed_domains = ["www.tianqihoubao.com/lishi/"]

    def start_requests(self):
        data = ['北京', '上海', '内江', '广安', '三亚', '阿坝', '安顺', '鞍山', '巴中', '白城', '白山', '白银', '包头', '宝鸡', '滨州', '长治', '沧州',
                '昌吉', '常州', '潮州', '池州', '崇左', '滁州',
                '达州', '大庆', '德宏', '德阳', '德州', '东莞', '东营', '鄂尔多斯', '鄂州', '防城港', '佛山', '抚顺', '抚州', '阜新', '阜阳', '固原', '广元',
                '贵港', '海东', '海西', '邯郸', '菏泽',
                '贺州', '鹤壁', '鹤岗', '衡水', '衡阳', '红河', '葫芦岛', '湖州', '怀化', '淮安', '淮北', '淮南', '黄冈', '黄石', '惠州', '吉林', '佳木斯',
                '嘉兴', '嘉峪关', '江门', '焦作', '揭阳',
                '金昌', '金华', '晋城', '晋中', '荆门', '荆州', '九江', '开封', '来宾', '莱芜', '廊坊', '乐山', '丽江', '连云港', '凉山', '辽阳', '辽源',
                '聊城', '临汾', '临夏', '临沂', '六安',
                '龙岩', '娄底', '泸州', '洛阳', '漯河', '吕梁', '马鞍山', '茂名', '眉山', '梅州', '南通', '宁波', '宁德', '怒江', '攀枝花', '盘锦', '平顶山',
                '萍乡', '莆田', '濮阳', '普洱', '七台河',
                '钦州', '秦皇岛', '庆阳', '衢州', '曲靖', '泉州', '三门峡', '三明', '商丘', '上饶', '绍兴', '十堰', '石嘴山', '双鸭山', '朔州', '松原',
                '苏州', '绥化', '随州', '遂宁', '塔城', '台州',
                '泰安', '泰州', '天水', '通化', '铜陵', '铜仁', '威海', '渭南', '温州', '文山', '乌海', '无锡', '吴忠', '武威', '咸宁', '咸阳', '湘潭',
                '湘西', '襄阳', '孝感', '忻州', '新乡', '新余',
                '宿迁', '宿州', '许昌', '宣城', '烟台', '盐城', '扬州', '阳江', '阳泉', '益阳', '鹰潭', '永州', '玉林', '玉溪', '云浮', '枣庄', '张家界',
                '漳州', '肇庆', '镇江', '中山', '中卫',
                '舟山', '周口', '珠海', '株洲', '资阳', '淄博', '自贡', '遵义', '阿克苏', '阿勒泰', '安康', '安庆', '安阳', '百色', '蚌埠', '保定', '保山',
                '北海', '本溪', '毕节', '亳州', '长春',
                '长沙', '常德', '朝阳', '郴州', '成都', '承德', '赤峰', '楚雄', '大理', '大连', '大同', '丹东', '儋州', '恩施', '福州', '甘孜', '赣州',
                '广州', '贵阳', '桂林', '哈尔滨', '哈密', '海口',
                '杭州', '合肥', '和田', '河池', '河源', '呼和浩特', '黄山', '鸡西', '吉安', '济南', '济宁', '锦州', '景德镇', '酒泉', '喀什', '克拉玛依',
                '昆明', '兰州', '丽水', '临沧', '柳州',
                '绵阳', '牡丹江', '南昌', '南充', '南京', '南宁', '南平', '南阳', '内江', '平凉', '齐齐哈尔', '青岛', '清远', '日照', '厦门', '汕头', '汕尾',
                '韶关', '深圳', '沈阳', '石家庄', '四平',
                '太原', '唐山', '通辽', '吐鲁番', '潍坊', '乌鲁木齐', '芜湖', '梧州', '武汉', '西安', '西宁', '信阳', '邢台', '徐州', '雅安', '延安', '伊春',
                '宜宾', '宜昌', '宜春', '银川', '营口',
                '榆林', '岳阳', '运城', '湛江', '张家口', '张掖', '昭通', '郑州', '驻马店']

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.tianqihoubao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        yield scrapy.Request('http://www.tianqihoubao.com/lishi/', dont_filter=True, callback=self.get_city_list,
                             headers=header, meta={'item': data})

    def get_city_list(self, response):
        response = response.replace(encoding='gbk')
        datas = map(lambda x: {x.css('::text').extract()[0].strip():
                                   'http://www.tianqihoubao.com' + x.css('::attr("href")').extract()[0]},
                    response.css('.citychk dd a'))

        datas = list(datas)
        datas = filter(lambda x: True if list(x.keys())[0] in response.meta['item'] else False, datas)
        datas = list(datas)
        for i, data in enumerate(datas):
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.tianqihoubao.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            city = list(data.keys())[0]
            url = data[city]
            yield scrapy.Request(url, dont_filter=True, callback=self.getinto_city,
                                 headers=header, meta={'item': {'city': city}})

    def getinto_city(self, response):
        urls = response.css('#content div a')
        for url in urls:
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.tianqihoubao.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            temp = url.css('a::attr("href")').extract()[0]
            year=temp.split('/')[-1].split('.')[0][:4]
            month=temp.split('/')[-1].split('.')[0][4:]
            if year!='2016' or not (month in ['08','12']):
                continue
            if year == '2016' and (month in ['08', '12']):
                temp='/lishi/'+temp
            if temp[0] != '/':
                temp = '/' + temp
            url = 'http://www.tianqihoubao.com' + temp
            yield scrapy.Request(url, dont_filter=True, callback=self.get_weather,
                                 headers=header, meta={'item': {'city': response.meta['item']['city']}})

    def get_weather(self, response):
        table_trs = response.css('table tr')
        for i, tr in enumerate(table_trs):
            if i == 0:
                continue
            item = Weatherhttp2Item()
            item['date'] = tr.xpath('./td[1]/a/text()').extract()[0].strip()
            item['statics'] = re.sub('\s+', '', tr.xpath('./td[2]//text()').extract()[0])
            item['temp'] = re.sub('\s+', '', tr.xpath('./td[3]//text()').extract()[0])
            item['wind'] = re.sub('\s+', '', tr.xpath('./td[4]//text()').extract()[0])
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            item['city'] = response.meta['item']['city']
            yield item
    