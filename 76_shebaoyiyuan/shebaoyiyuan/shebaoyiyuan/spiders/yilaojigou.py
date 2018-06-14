# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import json
import hashlib
from urllib import quote
from urllib import quote_plus
from shebaoyiyuan.items import ShebaoyuyuanItem

class YilaojigouSpider(scrapy.Spider):
    name = "yilaojigou"
    def start_requests(self):
        urls=['http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_01_outline_new.jsp']
        yield scrapy.Request(urls[0],method='POST',body='SearchWord=&sword=&suoshu=00&leibie=00&x=14&y=11',dont_filter=True)

    def parse(self, response):
        item_nums=response.css('body > center > table:nth-child(3)')
        page=int(item_nums.css('table')[1].css('b font::text').extract()[1])
        for i in range(0,page):
            url='http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_01_outline_new.jsp?sno=%s&spage=0&epage=10&leibie=00&suoshu=00&sword=' %(i*20)
            yield scrapy.Request(url,callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        table = response.css('body > center > table:nth-child(3)')
        table = table.css('table')[2]
        trs=table.css('tr')
        for i,tr in enumerate(trs):
            item = ShebaoyuyuanItem()
            if i==0:
                continue
            try:
                item['code']=tr.css('td')[0].css('a::text').extract()[0]
                item['hospital'] = tr.css('td')[1].css('a::text').extract()[0]
                item['county'] = tr.css('td')[2].css('span::text').extract()[0]
                item['kind'] = tr.css('td')[3].css('span::text').extract()[0]
                item['sort'] = tr.css('td')[4].css('span::text').extract()[0]
                item['type'] = '医疗机构'
                item['address']=''
                url='http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/'+tr.css('td')[1].css('a::attr("href")').extract()[0]
                yield scrapy.Request(url,callback=self.get_item_address,meta={'item':item},dont_filter=True)
            except Exception as e:
                pass

    def get_item_address(self,response):
        item=response.meta['item']
        address=response.xpath("/html/body/center/table[2]//tr/td/table//tr[5]/td/font/text()").extract()[0].encode('utf-8')
        item['address']= address
        queryStr = '/geocoder/v2/?address=%s&output=json&ak=Nvku0sAHDiCY1t9lY5q0Lob0IIYUo45t' % address
        encodedStr = quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        rawStr = encodedStr + 'Td8FeTRl5ol0ls7IStQOv9SPer7GujbN'
        sn = hashlib.md5(quote_plus(rawStr).encode()).hexdigest()
        url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=Nvku0sAHDiCY1t9lY5q0Lob0IIYUo45t&sn=%s' % (address,sn)
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Host':'api.map.baidu.com',
            'Upgrade-Insecure-Requests':'1',
            'referer': '',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        yield scrapy.Request(url, callback=self.get_item_address_xy,headers=headers, meta={'item': item}, dont_filter=True)

    def get_item_address_xy(self,response):
        address = response.body
        address = json.loads(address)
        lng=address['result']['location']['lng']
        lat=address['result']['location']['lat']
        item=response.meta['item']
        item['lng'] = lng
        item['lat'] = lat
        yield item

    