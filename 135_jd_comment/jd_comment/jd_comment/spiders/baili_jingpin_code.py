# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json
from scrapy import Selector
import random
from jd_comment.items import JdSkuItem




class BailiJingpinSpider(scrapy.Spider):
    name = 'baili_jingpin_code'
    allowed_domains = ["jd.com"]
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(BailiJingpinSpider,self).__init__(*args,**kwargs)
        self.dict = {'滔搏运动官方旗舰店':'https://mall.jd.com/view_search-641774-7027639-0-1-24-2.html',
                     '百丽集团男鞋旗舰店':'https://mall.jd.com/view_search-34265-0-99-1-24-1.html',
                     '优购运动旗舰店':'https://yougouyd.jd.com/view_search-62792-0-99-1-24-1.html',
                     '滔搏运动户外专营店':'https://mall.jd.com/view_search-284790-0-99-1-24-1.html'
                     }
        # self.taobo_url = 'https://yougouyd.jd.com/view_search-62792-0-99-1-24-1.html'
    def start_requests(self):
        for i in self.dict:
            url = self.dict.get(i)
            shop_name = i
            yield scrapy.Request(url,dont_filter=True,meta={'shop_name':shop_name})
    def parse(self, response):
        html = response.body
        shop_name = response.meta.get('shop_name')
        html = html.replace(r'\t', '').replace(r'\n', '').replace(' ', '').replace(r'||', '')
        code = json.loads(''.join(re.findall('varparams=(.*?){}', html)))
        code_1 = re.findall(
            'm_render_pageInstance_id="(.*?)"m_render_app_id="(.*?)".*?m_render_prototype_id="(.*?)"m_render_template_id="(.*?)"m_render_instance_id="(.*?)"m_render_is_search="true"',
            html)[-1]
        code_2 = re.findall('type=1&shopId=(.*?)&id=(.*?)"type="text', html)[0]
        url = 'https://module-jshop.jd.com/module/getModuleHtml.html?appId={appId}&orderBy={orderBy}&direction={direction}&categoryId={categoryId}&pageSize={pageSize}&pagePrototypeId={pagePrototypeId}&pageInstanceId={pageInstanceId}&moduleInstanceId={moduleInstanceId}&prototypeId={prototypeId}&templateId={templateId}&layoutInstanceId={layoutInstanceId}&origin=0&shopId={shopId}&venderId={venderId}&callback=jshop_module_render_callback&_={times}&pageNo={pageNo}'
        appid = code.get('appId')
        orderBy = code.get('orderBy')
        pageNo = code.get('pageNo')
        direction = code.get('direction')
        categoryId = code.get('categoryId')
        pageSize = code.get('pageSize')
        pagePrototypeId = code.get('pagePrototypeId')
        venderId = code.get('venderId')
        isGlobalSearch = code.get('isGlobalSearch')
        maxPrice = code.get('maxPrice')
        shopId = code.get('shopId')
        isRedisstore = code.get('isRedisstore')
        minPrice = code.get('minPrice')
        pageInstanceId = code_1[0]
        moduleInstanceId = code_1[-1]
        prototypeId = code_1[2]
        templateId = code_1[3]
        layoutInstanceId = code_1[-1]
        venderId = code_2[1]
        shopId = code_2[0]
        times = int(time.time())

        url = url.format(appId=appid, orderBy=orderBy, pageNo=pageNo, direction=direction, categoryId=categoryId,
                         pageSize=pageSize, pagePrototypeId=pagePrototypeId, pageInstanceId=pageInstanceId,
                         moduleInstanceId=moduleInstanceId, prototypeId=prototypeId, templateId=templateId,
                         layoutInstanceId=layoutInstanceId, shopId=shopId, venderId=venderId, times=times)
        yield scrapy.Request(url,dont_filter=True,callback=self.goods_info,meta={'page_url':url,'shop_name':shop_name})



    def goods_info(self, response):
        html = response.body
        shop_name = response.meta.get('shop_name')
        page_url = response.meta.get('page_url')
        html = html.replace(r'\t','').replace(r'\r\n','').replace('\\','').decode('utf8')
        name = Selector(text=html).xpath('//div[@class="jDesc"]/a/text()').extract()
        brand = Selector(text=html).xpath('//div[@class="jDesc"]/a/@href').extract()
        sid = Selector(text=html).xpath('//div[@class="jPrice"]/span[@class="jdNum"]/@jdprice').extract()
        if len(sid) == 0:
            sid = Selector(text=html).xpath('//div[@class="jdPrice"]/span[@class="jdNum"]/@jdprice').extract()
        if len(name) > 0:
            for i in zip(name,brand,sid):
                url = 'https:'+i[1]
                yield scrapy.Request(url,meta={'name':i[0],'url':url,'code':i[2],'shop_name':shop_name},dont_filter=True,callback=self.brand)
            page_split = page_url.split('pageNo=')
            page = int(page_split[1])+1
            url = page_split[0]+'pageNo='+str(page)
            yield scrapy.Request(url,meta={'page_url':url,'shop_name':shop_name},dont_filter=True,callback=self.goods_info)

    def brand(self,response): #详情页
        item ={}
        html = response.body.decode('gb18030').encode('utf8')
        bd =''.join(Selector(text=html).xpath('//*[@id="parameter-brand"]/li/a/text()').extract())
        item['brand'] = bd
        item['name'] = response.meta.get('name')
        if item['name'] == None:
            item['name'] = ''.join(re.findall('<title>(.*?)</title>',html))
        # item['url'] = response.meta['url']
        item['code'] = response.meta['code']
        # item['Article_number'] = ''.join(re.findall('>货号：(.*?)</li>',html))
        # item['applys'] = ''.join(re.findall('>适用人群：(.*?)</li>',html))
        # item['function'] = ''.join(re.findall('>功能科技：(.*?)</li>',html))
        # item['go_public'] = ''.join(re.findall('>上市时间：(.*?)</li>',html))
        item['the_name'] = response.meta.get('shop_name')
        if item['name']:
            info_list = response.meta.get('code')
            seiji = random.randint(600000,9999999)
            skuids = 'J_' + str(info_list)
            url = 'https://p.3.cn/prices/mgets?callback=jQuery{seiji}&type=1&area=1&pdtk=&pduid={uid}&pdpin=&pin=null&pdbp=0&skuIds={skuids}&ext=11000000&source=item-pc'
            price = url.format(skuids=skuids, seiji=seiji,uid=seiji)
            yield scrapy.Request(price,meta={'item':item},dont_filter=True,callback=self.price_xml)
        else:
            yield scrapy.Request(item['url'],meta=response.meta,dont_filter=True,callback=self.brand)




    def price_xml(self,response): #价格
        item = JdSkuItem()
        # item ={}
        items = response.meta['item']
        html = response.body
        p = html.split('[')[1][0:-4]
        p = json.loads(p)
        item['price'] = p.get('p')
        item['dt'] = time.strftime("%Y-%m-%d", time.localtime())
        item['sku'] = items['code']
        item['brand'] = items['brand']
        item['shop_name'] = items['the_name']
        yield item


    