# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Selector
import json
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

headers = {
'Connection':'keep-alive',
'Host':'rms.shop.jd.com',
'Referer':'https://mall.jd.com/index-33132.html',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

class JdB2cSpider(scrapy.Spider):
    name = 'JD_b2c'
    allowed_domains = []
    start_urls = []
    def __init__(self,*args,**kwargs):
        super(JdB2cSpider,self).__init__(*args,**kwargs)
        self.b2c_url = 'https://mall.jd.com/index-33132.html'
    def start_requests(self):
        url = self.b2c_url
        yield scrapy.Request(url,dont_filter=True)
    def parse(self, response):
        html = response.body
        title = Selector(text=html).xpath('//*[@class="sub-menu-wrap"]/dl/dt/a/text()').extract()
        qt = 1
        list_= []
        for i in title:
            sd = []
            xp_href = '//*[@class="sub-menu-wrap"]/dl['+str(qt)+ ']/dd/ul/li/a/@href'
            xp_title = '//*[@class="sub-menu-wrap"]/dl['+str(qt)+']/dd/ul/li/a/text()'
            qt+=1
            href = Selector(text=html).xpath(xp_href).extract()
            title_ = Selector(text=html).xpath(xp_title).extract()
            sd.append(href)
            sd.append(title_)
            sd.append(i)
            list_.append(sd)
        for td in list_:
            for x in zip(td[0],td[1]):
                url = 'http:'+ x[0]
                yield scrapy.Request(url,meta={'title':td[2],'type_title':x[1],'href':url},dont_filter=True,callback=self.type_data)


    def type_data(self,response):
        html = response.body
        title = response.meta.get('title')
        type_title = response.meta.get('type_title')
        href = response.meta.get('href')
        html = html.replace(r'\t','').replace(r'\n','').replace(' ','').replace(r'||','')
        code = json.loads(''.join(re.findall('varparams=(.*?){}', html)))
        code_1 =re.findall('m_render_pageInstance_id="(.*?)"m_render_app_id="(.*?)".*?m_render_prototype_id="(.*?)"m_render_template_id="(.*?)"m_render_instance_id="(.*?)"m_render_is_search="true"',html)[-1]
        code_2 = re.findall('type=1&shopId=(.*?)&id=(.*?)"type="text', html)[0]
        url = 'https://module-jshop.jd.com/module/getModuleHtml.html?appId={appId}&orderBy={orderBy}&pageNo={pageNo}&direction={direction}&categoryId={categoryId}&pageSize={pageSize}&pagePrototypeId={pagePrototypeId}&pageInstanceId={pageInstanceId}&moduleInstanceId={moduleInstanceId}&prototypeId={prototypeId}&templateId={templateId}&layoutInstanceId={layoutInstanceId}&origin=0&shopId={shopId}&venderId={venderId}&callback=jshop_module_render_callback&_={times}'
        appid = code.get('appId')
        orderBy= code.get('orderBy')
        pageNo = code.get('pageNo')
        direction = code.get('direction')
        categoryId = code.get('categoryId')
        pageSize = code.get('pageSize')
        pagePrototypeId = code.get('pagePrototypeId')
        pageInstanceId = code_1[0]
        moduleInstanceId = code_1[-1]
        prototypeId = code_1[2]
        templateId = code_1[3]
        layoutInstanceId = code_1[-1]
        venderId = code_2[1]
        shopId = code_2[0]
        times = int(time.time())
        url = url.format(appId=appid,orderBy=orderBy,pageNo=pageNo,direction=direction,categoryId=categoryId,pageSize=pageSize,pagePrototypeId=pagePrototypeId,pageInstanceId=pageInstanceId,moduleInstanceId=moduleInstanceId,prototypeId=prototypeId,templateId=templateId,layoutInstanceId=layoutInstanceId,shopId=shopId,venderId=venderId,times=times)
        yield scrapy.Request(url,dont_filter=True,callback=self.goods_info,meta={'title':title,'type_title':type_title,'href':href})

    def goods_info(self, response):
        html = response.body
        title = response.meta.get('title')
        type_title = response.meta.get('type_title')
        href = response.meta.get('href')
        html = html.replace(r'\t','').replace(r'\r\n','').replace('\\','').decode('utf8')
        name = Selector(text=html).xpath('/html/body/div/div/div/div[2]/ul/li/div/div[3]/div[2]/a/text()').extract()
        brand = Selector(text=html).xpath('/html/body/div/div/div/div[2]/ul/li/div/div[3]/div[2]/a/@href').extract()

        if len(name) > 0:
            comments_int = 0
            info_list = []
            for i in zip(name,brand):
                info_date = []
                comments_int += 1
                goods_type_xpath = '/html/body/div/div/div/div[2]/ul/li[' + str(comments_int) + ']/div/div[2]/div/ul/li/a/@title'
                comments_xpath = '/html/body/div/div/div/div[2]/ul/li[' + str(comments_int) + ']/div/div[3]/div[4]/a/em/text()'
                sid_xpath = '/html/body/div/div/div/div[2]/ul/li[' + str(comments_int) + ']/div/div[2]/div/ul/li/@sid'
                comments = ''.join(Selector(text=html).xpath(comments_xpath).extract())
                goods_type = Selector(text=html).xpath(goods_type_xpath).extract()
                sid = Selector(text=html).xpath(sid_xpath).extract()
                info_date.append(i)
                info_date.append(comments)
                info_date.append(goods_type)
                info_date.append(sid)
                info_list.append(info_date)
                url = 'https:'+i[1]
                yield scrapy.Request(url,meta={'title':title,'type_title':type_title,'href':href,'url':url,'info':info_list},dont_filter=True,callback=self.brand)
                info_list=[]
    def brand(self,response):
        html = response.body.decode('gb18030').encode('utf8')
        bd =''.join(Selector(text=html).xpath('//*[@id="parameter-brand"]/li/a/text()').extract())
        response.meta['brand'] = bd
        info_list = response.meta.get('info')
        print info_list
        seiji = random.randint(600000,9999999)
        for x in info_list:
            skuids = ''
            # url ='https://p.3.cn/prices/mgets?callback=jQuery{seiji}&skuids={skuids}'+'&_={time}'
            url = 'https://p.3.cn/prices/mgets?callback=jQuery{seiji}&type=1&area=1&pdtk=&pduid={uid}&pdpin=&pin=null&pdbp=0&skuIds={skuids}&ext=11000000&source=item-pc'
            for i in x[3]:
                    skuids+='J_'+i+'%2C'
            price = url.format(skuids=skuids, seiji=seiji,uid=seiji)
            response.meta['info'] = x
            response.meta['url_price'] = price
            yield scrapy.Request(price,meta=response.meta,dont_filter=True,callback=self.price_xml)



    def price_xml(self,response):
        item = {}
        html = response.body
        p = html.split('[')[1][0:-4]
        title = response.meta.get('title')
        type_title = response.meta.get('type_title')
        info = response.meta.get('info')
        date_new = []
        for i in p.split('},'):
            if i[-1] != '}':
                i = i + '}'
            date_new.append(i)
        for info_new in zip(info[2],info[3],date_new):
            item['menu'] = title
            item['sub_title'] = type_title
            item['b2c_name'] = info[0][0]
            item['b2c_type'] = info_new[0]
            item['comments'] = info[1]
            item['code'] = info_new[1]
            item['price'] = json.loads(info_new[2]).get('p')
            item['brand'] = response.meta.get('brand')
            item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
            item['tag'] = u'京东'
            yield item

    