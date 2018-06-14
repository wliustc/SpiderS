# -*- coding: utf-8 -*-
import scrapy
import time
import re
import sys
from lxml import etree
from epet_sku.items import EpetJdSkuItem
import json
reload(sys)
sys.setdefaultencoding('utf-8')
def get_time():
    return int(time.time() * 1000)
class JdEpetSpider(scrapy.Spider):
    name = "jd_epet"
    allowed_domains = ["mall.jd.cocd m"]

    # 访问店铺主页
    def start_requests(self):
        yield scrapy.Request('https://mall.jd.com/index-123607.html',headers={
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.8',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        },dont_filter=True)

    # 访问所有分类栏
    def parse(self, response):
        tables_level1=response.css('div[class="sub-menu-wrap"] dl[class="sub-pannel"]')
        for level1 in tables_level1:
            level_1=level1.css('dt a::text').extract()[0].strip(' >')
            for level2 in level1.css('dd li a'):
                url = level2.xpath("@href").extract()[0]
                url ='https:'+url
                level2=level2.css("::text").extract()[0]
                yield scrapy.Request(url,callback=self.parse_page,
                                     headers={
                                     'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                      'accept-encoding':'gzip, deflate, br',
                                      'accept-language':'zh-CN,zh;q=0.8',
                                      'cache-control':'max-age=0',
                                      'referer':'https://mall.jd.com/index-123607.html',
                                      'upgrade-insecure-requests':'1',
                                      'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                            },
                    meta={'item':{'level1':level_1,'level2':level2},'category_url':url},dont_filter=True)


    def parse_page(self,response):
        temps=response.css('.m_render_structure')[7]
        temp={}
        get_url=response.url.split('.html')[0]
        temp['appId']=get_url.split('-')[1]
        temp['orderBy'] =get_url.split('-')[3]
        temp['pageNo'] =get_url.split('-')[6]
        temp['direction'] =get_url.split('-')[4]
        temp['categoryId'] = get_url.split('-')[2]
        temp['pageSize'] =get_url.split('-')[5]
        temp['pagePrototypeId'] = 8
        temp['pageInstanceId'] = temps.xpath('@m_render_pageInstance_id'.lower()).extract()[0]
        temp['moduleInstanceId'] = temps.xpath('@m_render_instance_id'.lower()).extract()[0]
        temp['prototypeId'] = temps.xpath('@m_render_prototype_id'.lower()).extract()[0]
        temp['templateId'] =temps.xpath('@m_render_template_id'.lower()).extract()[0]
        temp['layoutInstanceId'] =temps.xpath('@m_render_layout_instance_id'.lower()).extract()[0]
        temp['origin'] =temps.xpath('@m_render_origin'.lower()).extract()[0]
        temp['shopId'] ='123607'
        temp['venderId'] ='127169'
        temp['callback'] ='jshop_module_render_callback'
        temp['_'] = get_time()
        url='https://module-jshop.jd.com/module/getModuleHtml.html?' \
            'appId=%(appId)s&orderBy=%(orderBy)s&pageNo=%(pageNo)s&direction=%(direction)s&' \
            'categoryId=%(categoryId)s&pageSize=%(pageSize)s&' \
            'pagePrototypeId=%(pagePrototypeId)s&pageInstanceId=%(pageInstanceId)s&' \
            'moduleInstanceId=%(moduleInstanceId)s&' \
            'prototypeId=%(prototypeId)s&' \
            'templateId=%(templateId)s&layoutInstanceId=%(layoutInstanceId)s&origin=%(origin)s&' \
            'shopId=%(shopId)s&venderId=%(venderId)s&' \
            'callback=%(callback)s&_=%(_)s' %temp
        headers = {
                      'Host':'module-jshop.jd.com',
                      'Accept': '*/*',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Referer': response.url,
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }
        yield scrapy.Request(url,callback=self.get_item,
                            headers=headers,
                             meta={'item':{'level1':response.meta['item']['level1'],
                                           'level2':response.meta['item']['level2']},
                                            'page':int(get_url.split('-')[6]),
                                            'category_url': response.meta['category_url'],
                                            'source_url':response.url,
                                   },
                             dont_filter=True)

    def get_item(self,response):
        body=response.body.decode()
        data=re.search(r'"moduleText":(?P<content>.+),"moduleInstanceId"',body).group('content')
        data=re.sub('\\\\"','"',data)
        html=etree.HTML(data)
        lis=html.xpath('//div[@class="user_prolist"]/ul/li')
        tmp={}
        for li in lis:
            name=li.xpath('./table/tr[2]/td/a/text()')[0]
            num = re.sub('[^0-9]','',li.xpath('./table/tr[4]/td/span/text()')[0])
            sku = li.xpath('./table/tr[2]/td/a/@href')[0].split('/')[3].split('.')[0]
            tmp[sku]={'name':name,'num':num,'sku':sku}

        url=''
        for temp in tmp.keys():
            url+='J_'+temp+','
        url='https://p.3.cn/prices/mgets?callback=jQuery8432529&skuids='+url+'&_=%s' %get_time()
        yield scrapy.Request(url,callback=self.get_price,
                             headers={
                             'Accept':'*/*',
                             'Accept-Encoding':'gzip, deflate, br',
                             'Accept-Language':'zh-CN,zh;q=0.8',
                             'Connection':'keep-alive',
                             'Host':'p.3.cn',
                            'Referer':response.meta['source_url'],
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                             },
                             meta={'item':tmp,'category':response.meta['item']},dont_filter=True)
        if response.meta['page']==1:
            page_num=int(re.sub('[^0-9]','',html.xpath('//div[@class="jPage"]/em/text()')[0]))
            print(html.xpath('//div[@class="jPage"]/em/text()')[0])
            page_num = (page_num-1)//24+1
            for i in range(2,page_num+1):
                url=response.meta['category_url'].split('.html')[0][0:-1]+str(i)+'.html'
                yield scrapy.Request(url,callback=self.parse_page,
                                     headers={
                                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                         'accept-encoding': 'gzip, deflate, br',
                                         'accept-language': 'zh-CN,zh;q=0.8',
                                         'cache-control': 'max-age=0',
                                         'referer': response.meta['source_url'],
                                         'upgrade-insecure-requests': '1',
                                         'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                                     },
                                     meta={'item':{'level1':response.meta['item']['level1'],
                                                   'level2':response.meta['item']['level2']},'category_url':url},dont_filter=True)


    def get_price(self,response):
        items=response.meta['item']
        data=response.body.decode()
        datas=json.loads(re.search('jQuery8432529\((?P<content>.+)\);',data).group('content'))
        for data in datas:
            sku=data['id'].split('_')[1]
            price=data['p']
            items[sku]['price']=price
            items[sku]['level1']=response.meta['category']['level1']
            items[sku]['level2'] = response.meta['category']['level2']
            items[sku]['dt']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        for temp in items.keys():
            item = EpetJdSkuItem()
            item['sku']=items[temp]['sku']
            item['list_1'] = items[temp]['level1']
            item['list_2'] = items[temp]['level2']
            item['good_name']=items[temp]['name']
            item['price'] = items[temp]['price']
            item['comment_num'] = items[temp]['num']
            item['dt'] = items[temp]['dt']
            yield item

    
    
    