# -*- coding: utf-8 -*-
import scrapy
import execjs
import re
from jd_comment.items import JdSkuItem
import time


class SearchListSpider(scrapy.Spider):
    name = "search_list"
    allowed_domains = ["www.jd.com"]
    start_urls = [{'shop_name': '天美意官方旗舰店', 'pinpai': '天美意（TEENMIX）'},
                  {'shop_name': '妙丽官方旗舰店', 'pinpai': '妙丽（Millies）'},
                  {'shop_name': '真美诗官方旗舰店', 'pinpai': '真美诗（Joy&peace）'},
                  {'shop_name': 'CAT官方旗舰店', 'pinpai': 'CAT'},
                  {'shop_name': '百丽官方旗舰店', 'pinpai': 'Istbelle 百丽（Belle） Bevivo'},
                  {'shop_name': '他她官方旗舰店', 'pinpai': '他她（TATA）'},
                  {'shop_name': '思加图官方旗舰店', 'pinpai': '思加图（STACCATO）'},
                  {'shop_name': '百思图官方旗舰店', 'pinpai': '百思图（BASTO）'},
                  {'shop_name': '百丽集团京东自营旗舰店', 'pinpai': '百思图（BASTO） 百丽（BeLLE） 他她（TATA） 天美意（TEENMIX） 真美诗（Joy&peac'},
                  {'shop_name': '森达官方旗舰店', 'pinpai': '森达（SENDA）'},
                  {'shop_name': '暇步士官方旗舰店', 'pinpai': '暇步士（Hush Puppies）'}]

    def start_requests(self):
        for data in self.start_urls:
            url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % data['shop_name']
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'search.jd.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_search_list, meta={'item':{
                               'shop_name':data['shop_name'],'brand':data['pinpai'],'page': 1}})

    def get_search_list(self, response):
        page = response.meta['item']['page']
        if not 'page_num_m' in response.meta['item']:
            page_num_m = int(response.css('#J_topPage .fp-text i::text').extract()[0]) * 2
        else:
            page_num_m = response.meta['item']['page_num_m']
        temps = response.css('.gl-item')
        for temp in temps:
            item = {}
            item['sku'] = temp.css('::attr("data-sku")').extract()[0]
            try:
                item['spu'] = temp.css('::attr("data-spu")').extract()[0]
            except Exception as e:
                item['spu'] = item['sku']
            item['shop_name'] = response.meta['item']['shop_name']
            item['brand'] = response.meta['item']['brand']
            item['title'] = ''.join(temp.css('.p-name em::text').extract()).split(' ')[0]
            header={
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.8',
            'cache-control':'max-age=0',
            'if-modified-since':'Fri, 10 Nov 2017 03:12:30 GMT',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }
            url='https://item.jd.com/'+item['sku']+'.html'
            yield scrapy.Request(url,headers=header,dont_filter=True, callback=self.get_detail_item, meta={'item':item})
        if page == 1:
            a = response.xpath('//div[@id="J_container"]/script[1]/text()').extract()[0]
            data = re.search('LogParm = (?P<name>{([\t\n].+)+)\n};', a)
            data = execjs.eval(data.groupdict()['name'] + '}')
            log_id = data['log_id']
            data = re.search('base_url=.+', a)
            base_url = data.group().strip(';').strip('base_url=').strip("'")
        else:
            log_id = response.meta['item']['log_id']
            base_url = response.meta['item']['base_url']
        if page < page_num_m and len(temps) >= 30:
            page = page + 1
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'search.jd.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            url = "https://search.jd.com/s_new.php?" + base_url + "&page=" + str(page) + "&s=" + str(
                1 + 30 * (page - 1)) + "&scrolling=y&log_id=" + log_id + "&tpl="
            yield scrapy.Request(url, headers=header, dont_filter=True, callback=self.get_search_list, meta={'item':{ 'shop_name':
                                    response.meta['item']['shop_name'],'brand':response.meta['item']['brand'],
                                    'page': page,'page_num_m': page_num_m,'base_url': base_url,'log_id': log_id}})


    def get_detail_item(self,response):
        datas=re.search('colorSize: (?P<name>.+\])',response.body.decode('gbk')).groupdict()['name']
        datas=eval(datas)
        for data in datas:
            item = JdSkuItem()
            item['sku'] = data['skuId']
            item['spu'] = response.meta['item']['spu']
            item['shop_name'] = response.meta['item']['shop_name']
            item['brand'] = response.meta['item']['brand']
            item['title'] = response.meta['item']['title']
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            item['chicun'] = data['尺码']
            try:
                item['yanse'] = data['颜色']
            except Exception as e:
                item['yanse'] = ''
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            yield item
        pass
    
    
    