# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
import sys
import random
import re
import web
from tongcheng.items import TongchengItem
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', host='10.15.1.24', port=3306)
USER_AGENTS = [
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'User-Agent,Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent,Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
]


class ShangpuSpider(scrapy.Spider):
    name = 'shangpu'

    # allowed_domains = ['http://bj.58.com/shangpucz/?PGTID=0d100000-0000-1152-6523-50bde0228f08']
    # start_urls = ['http://http://bj.58.com/shangpucz/?PGTID=0d100000-0000-1152-6523-50bde0228f08/']

    def start_requests(self):
        sql = '''select distinct base_url from t_spider_58tongcheng_shangpu_url_list;'''
        for i in db.query(sql):
            url = i.get('base_url')
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                # 'Host': 'bj.58.com'
            }
            yield Request(url, headers=headers, meta={'url': url}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # http://callback.58.com/firewall/valid/3701644040.do?namespace=fangchan_business_pc&url=bj.58.com%2Fshangpu%2F33550129756868x.shtml
        base_url = response.url
        if 'callback' in str(base_url):
            i = re.search(r'url=(.*)', base_url)
            if i:
                i = i.group(1)
                base_url = urllib.unquote(i)
                url = 'http://' + base_url
                # url = response.url
                headers = {
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                }
                yield scrapy.Request(url, meta={'url': url}, headers=headers, callback=self.parse, dont_filter=True)
        else:
            text = response.xpath('//div[@class="wrap"]/div/h1[@class="item"]/text()').extract()
            if text:
                item = TongchengItem()
                item['url'] = response.url
                item['title'] = ''
                item['name'] = ''
                item['phone'] = ''
                item['publish_time'] = ''
                item['img_src'] = ''
                item['house_description'] = ''
                item['near_description'] = ''
                item['money'] = ''
                item['house_area'] = ''
                item['house_type'] = ''
                item['manager_form'] = ''
                item['country'] = ''
                item["area"] = ''
                # print text
                item['lat'] = ''
                item['addr'] = ''
                item['lon'] = ''
                item['city'] = u'北京'
                yield item
            else:
                title = response.xpath('//div[@class="house-title"]/h1/text()').extract()
                if title:
                    html = response.body
                    item = TongchengItem()
                    item['url'] = response.url
                    if title:
                        title = ''.join(title)
                        item['title'] = title.strip()
                    else:
                        item['title'] = ''
                    name = response.xpath('//p[@class="nav"]/span/text()').extract()  # 联系人名称
                    if name:
                        item['name'] = name
                    else:
                        item['name'] = ''
                    phone = response.xpath('//p[@class="phone-num"]/text()').extract()  # 联系人电话
                    if phone:
                        item['phone'] = ''.join(phone)
                    else:
                        item['phone'] = ''
                    img_src = response.xpath('//ul[@class="general-pic-list"]/li/img/@data-src').extract()  # 图片
                    if img_src:
                        item['img_src'] = img_src
                    else:
                        item['img_src'] = ''
                    publish_time = response.xpath('//div[@class="house-title"]/p/span[1]/text()').extract()  # 发布时间
                    if publish_time:
                        item['publish_time'] = ''.join(publish_time)
                    else:
                        item['publish_time'] = ''
                    # item['publish_time'] = ''.join(publish_time)
                    house_description = response.xpath('//div[@id="generalSound"]/div[@class="general-item-wrap"]')  # 房源描述
                    if house_description:
                        house_description = house_description.xpath('string(.)').extract()
                        item['house_description'] = ''.join(house_description).strip()
                    else:
                        item['house_description'] = ''
                    near_description = response.xpath('//div[@id="generalSound"]/div[@class="general-item-wrap"]')  # 房源描述
                    if near_description:
                        near_description = near_description.xpath('string(.)').extract()
                        item['near_description'] = ''.join(near_description).strip()
                    else:
                        item['near_description'] = ''
                    money = response.xpath(
                        '//p[@class="house_basic_title_money"]/span[@class="house_basic_title_money_num"]/text()').extract()  # 租金
                    if money:
                        item['money'] = ''.join(money)
                    else:
                        item['money'] = ''
                    house_area = response.xpath(
                        '//ul[@class="house_basic_title_content"]/li[1]/span[@class="house_basic_title_content_item2"]/text()').extract()  # 面积
                    if house_area:
                        item['house_area'] = house_area[0]
                    else:
                        item['house_area'] = ''
                    house_type = response.xpath('//ul[@class="house_basic_title_content"]/li[1]/a/text()').extract()
                    if house_type:
                        item['house_type'] = house_type
                    else:
                        item['house_type'] = ''
                    manager_form = response.xpath(
                        '//ul[@class="house_basic_title_content"]/li[2]/span[@class="house_basic_title_content_item3"]/text()').extract()
                    if manager_form:
                        manager_form = ''.join(manager_form)
                        item["manager_form"] = manager_form.strip()
                    else:
                        item['manager_form'] = ''
                    country = response.xpath('//ul[@class="house_basic_title_content"]/li[6]/a[1]/text()').extract()
                    if country:
                        item['country'] = country
                    else:
                        item['country'] = ''
                    area = response.xpath('//ul[@class="house_basic_title_content"]/li[6]/a[2]/text()').extract()
                    if area:
                        item['area'] = area
                    else:
                        item["area"] = ''
                    addr = response.xpath(
                        '//ul[@class="house_basic_title_content"]/li[6]/span[@class="house_basic_title_content_item3 xxdz-des"]/text()').extract()
                    if addr:
                        addr = addr[0]
                        item['addr'] = addr.strip()
                    else:
                        item['addr'] = ''
                    lat = re.findall(r'"baidulat":(.*?),', html, re.S)
                    if lat:
                        item['lat'] = ''.join(lat)
                    else:
                        item['lat'] = ''
                    lon = re.findall(r'"baidulon":(.*?),\"', html, re.S)
                    if lon:
                        item['lon'] = ''.join(lon)
                    else:
                        item['lon'] = ''
                    item['city'] = u'北京'
                    yield item
                else:
                    meta = response.meta
                    url = meta.get('url')
                    if url:
                        headers = {
                            'User-Agent': random.choice(USER_AGENTS),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                            # 'Host': 'bj.58.com'
                        }
                        yield scrapy.Request(url, headers=headers, meta={'url': url}, callback=self.parse, dont_filter=True)

    