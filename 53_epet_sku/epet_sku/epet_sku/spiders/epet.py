# -*- coding: utf-8 -*-
import time
import scrapy
from epet_sku.items import EpetSkuItem
import re
class EpetSpider(scrapy.Spider):
    name = "epet"
    allowed_domains = ["*"]
    page=0
    start_urls = (
        'http://www.epet.com/',     #狗狗
        'http://cat.epet.com/',     #猫
    )

    def parse(self, response):          #第一步获得一级列表
        task_day=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        list0=response.url.split('.')[0].split('/')[-1]
        if list0=='www':
            list_0='狗狗'
        elif list0=='cat':
            list_0='猫猫'
        data_list_tags = response.css('.catelist .dogType')
        data_list_tags=data_list_tags.css('li')
        temp=[]
        for datas in data_list_tags:
            langs = datas.css('::attr("lang")').extract()[0].split(',')
            for i,data in enumerate(datas.css('a')):
                temp.append({"lang" : langs[i],
                             "list_one":data.css("::text").extract()[0],
                             "list_0": list_0})
        yield scrapy.Request('http://www.epet.com/share/run.html?act=allcates&inajax=1',meta={'item':temp,'task_day':task_day},
                             callback=self.parse_list2,dont_filter=True)

    def parse_list2(self, response):    #找到了二级列表
        data_list_tags = response.css('.cate_l')
        list_1s=response.meta['item']
        task_day=response.meta['task_day']
        temp=[]
        for list_1 in list_1s:
            list2s=data_list_tags.css(".ct_%s" % list_1['lang'])
            for list2 in list2s:
                title=list2.css('.ctitle a::text').extract()[0]
                tmp = {'list_0':list_1['list_0'],"list_1": title,'list_2':[]}
                for data in list2.css('.mid_head'):
                    tmp['list_2'].append({
                                            'name': data.css("a::text").extract()[0],
                                            'url':data.css('a::attr("href")').extract()[0],
                                          })
                temp.append(tmp)
        for tmp in temp:
            for data in tmp['list_2']:
                url=data['url']
                yield scrapy.Request(url,meta={'item':{'list_1':tmp['list_1'],'list_2':data['name'],'list_0':tmp['list_0']},
                                               'task_day':task_day},
                                     callback=self.parse_list3,
                                dont_filter=True )

    def parse_list3(self,response):     #第三级分类，抓tr2
        data_list_tags = response.css('.filter_box')
        task_day=response.meta['task_day']
        data_list_tags=data_list_tags.css(".filter_box  tr:nth-child(2)")
        list3s=data_list_tags.css('td a')
        temp=[]
        if list3s.css("::text").extract():
            datas=list3s.css('a')
            for data in datas:
                url=data.css('::attr("href")').extract()[0]
                name=data.css('::text').extract()[0]
                if (len(datas) > 1) and (name=='全部'):
                    continue
                tmp={}
                tmp.update(response.meta['item'])
                tmp['list_3']=name
                tmp['url']=url
                temp.append(tmp)
        else:
            tmp={}
            tmp.update(response.meta['item'])
            tmp['list_3']="全部"
            tmp['url']=response.url
            temp.append(tmp)
        for tmp in temp:
            yield scrapy.Request(tmp['url'],meta={'item':tmp,'task_day':task_day},callback=self.parse_list4,
                                 dont_filter=True)

    def parse_list4(self, response):#得到总页数
        goods_num = int(response.css(".lis_plr .cred::text").extract()[0])
        page_nums= goods_num//60
        if goods_num%60:
            page_nums+=1

        for i in range(1,page_nums+1):  #生成每页的url
            url=str(response.url)
            yield scrapy.Request(url.split('.html')[0]+'f%s' %i+'.html',meta=response.meta,callback=self.parse_list5,
                                 dont_filter=True)

    def parse_list5(self,response):      #爬取sku列表
        good_lists=response.css('.list_box-li')
        temp=[]
        task_day = response.meta['task_day']
        for good_list in good_lists:
            sku=good_list.css('::attr("data-gid")').extract()[0]
            url=good_list.css('.gd-photo::attr("href")').extract()[0]
            tmp={'list_1':response.meta['item']['list_1'],'list_2':response.meta['item']['list_2'],
                 'list_0':response.meta['item']['list_0'],
                 'list_3':response.meta['item']['list_3'],'sku':sku,'url':url,'last_url':response.url
                 }
            temp.append(tmp)
        for tmp in temp:
            yield scrapy.Request(tmp['url'],meta={'item':tmp,'task_day':task_day},callback=self.parse_list6,
                                 dont_filter=True)

    def parse_list6(self,response):     #抓详情页
        item=EpetSkuItem()
        # 商品名称 品牌 市场价 E宠价 累计销量（已售数量） 评价数量  url(筛选页面错误)
        good_name=self.get_goodname(response)
        goodbrand=self.get_goodbrand(response)
        eprice=self.get_eprice(response)
        sprice=self.get_sprice(response)
        countnum=self.get_countnum(response)
        xiaoliang=self.get_xiaoliang(response)
        item['sku']=response.meta['item']['sku']
        item['good_name']=good_name
        item['list_0']=response.meta['item']['list_0']
        item['list_1']=response.meta['item']['list_1']
        item['list_2'] = response.meta['item']['list_2']
        item['list_3'] = response.meta['item']['list_3']
        item['goodbrand'] = goodbrand
        item['eprice'] = eprice
        item['sprice'] = sprice
        item['countnum'] = countnum
        item['xiaoliang'] = xiaoliang
        item['url']=response.url
        item['last_url']=response.meta['item']['last_url']
        item['task_day']=response.meta['task_day']
        yield item

    def get_goodname(self,response):
        i=0
        while True:
            if i==0:
                name=response.css('.gdtitle::text').extract()
            elif i==1:
                name = response.css('.xq-title h1::text').extract()
            else:
                name=''
                break
            if not name:
                i+=1
            else:
                break
        if not name:
            name=''
        else:
            name=name[0]
        name=name.strip()
        return name

    def get_goodbrand(self,response):
        brand=response.css('.brands-home div[data-name=brand-info] span:nth-child(1)::text').extract()
        if not brand:
            brand=''
        else:
            brand=brand[0]
        return brand

    def get_eprice(self,response):
        eprice = response.css('#goods-sale-price::text').extract()
        if not eprice:
            eprice=''
        else:
            eprice=eprice[0]
        return eprice

    def get_sprice(self, response):
        i=0
        while True:
            if i==0:
                sprice = response.css('.epet-pprice del::text').extract()
            elif i==1:
                sprice = response.css('.this-price em::text').extract()
            else:
                sprice=''
                break
            if not sprice:
                i+=1
            else:
                break
        if not sprice:
            sprice=''
        else:
            if sprice:
                sprice = re.findall("[.0-9]+", sprice[0])[0]
        return sprice

    def get_countnum(self, response):
        '.had-buy li:nth-child(1) span::text'
        i=0
        while True:
            if i==0:
                countnum = response.css('.gdtable .ats-style:nth-child(2) .ce54649::text').extract()
                if countnum:
                    countnum=countnum[0]
            elif i==1:
                countnum = response.css('.had-buy li:nth-child(2) span::text').extract()
                print(countnum)
                if countnum:
                    countnum=re.findall("\([0-9]+",countnum[0])[0]
            else:
                countnum=''
                break
            if not countnum:
                i+=1
            else:
                break
        if not countnum:
            countnum=''
        countnum=countnum.strip('()')
        return countnum

    def get_xiaoliang(self,response):
        i=0
        while True:
            if i==0:
                xiaoliang = response.css('.gdtable .ats-style:nth-child(1) .ce54649::text').extract()
                if xiaoliang:
                    xiaoliang=xiaoliang[0]
            elif i==1:
                xiaoliang = response.css('.had-buy li:nth-child(1) span::text').extract()
                if xiaoliang:
                    xiaoliang=re.findall("[0-9]+",xiaoliang[0])[0]
            else:
                xiaoliang=''
                break
            if not xiaoliang:
                i+=1
            else:
                break
        if not xiaoliang:
            xiaoliang=''
        return xiaoliang
    