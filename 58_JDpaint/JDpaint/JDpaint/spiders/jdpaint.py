# -*- coding: utf-8 -*-
import scrapy
import json
import re
import datetime
import copy
from JDpaint.items import JDpaintItem
task_date=datetime.date.today().strftime("%Y-%m-%d")
form_d={
            '_format_':'json',
            'stock':'1',
            'sort':'1',
            'page':'1',
            'categoryId':'9931',
            'c1':'9847',
            'c2':'9860',
            'expressionKey':''
}
class JdpaintSpider(scrapy.Spider):
    name = "JDpaint"
    allowed_domains = ["jd.com"]
    #start_urls = (
    #    'http://www.jd.com/',
    #)
    def __init__(self, *args, **kwargs):
        #https://so.m.jd.com/ware/search.action?keyword=%E7%AB%8B%E9%82%A6      手机APP上的
        self.cUrl = 'https://so.m.jd.com/ware/searchList.action'
        self.stUrl = 'http://item.m.jd.com/product/{}.html'
        self.brandlist=['立邦','多乐士','华润漆','三棵树漆','嘉宝莉']

    def start_requests(self):
        for brand in self.brandlist:
            tmp = form_d
            expressionKey='[{"key":"品牌","value":"'+brand+'"}]'
            tmp['expressionKey']=expressionKey

            yield scrapy.FormRequest(self.cUrl,
                            formdata=copy.deepcopy(form_d),
                            headers={
                                'Host': 'so.m.jd.com',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cache-Control': 'no-cache'
                            },
                            method="POST",
                            meta={'brand':brand,'page':tmp['page']},
                            callback = self.parse
                            )
    def parse(self, response):
        if response:
            items_list=self._parse_list_items(response)
            if items_list:
                for item in items_list:
                    ware_id=item['ware_id']
                    yield scrapy.Request(self.stUrl.format(ware_id),meta={'item':item},callback=self.parse_item)
                brand=response.meta['brand']
                tmp = copy.deepcopy(form_d)
                page = response.meta['page']
                tmp['page']=str(int(page)+1)
                expressionKey='[{"key":"品牌","value":"'+brand+'"}]'
                tmp['expressionKey']=expressionKey
                yield scrapy.FormRequest(self.cUrl,
                            formdata = tmp,
                            meta={'brand':brand,'page':page},
                            callback = self.parse
                            )
            else:
                pass
    	
    def parse_item(self,response):
        item=response.meta['item']
        body =response.body.decode()
        p=re.compile(r'.jpg","shopId":(\d+),"name":"(.*)","score":')
        m=p.search(body)
        if m:
            shop_id=str(m.group(1)).strip()
            shop_name=str(m.group(2)).strip()
            shop_name=shop_name.split('",')[0]#这句是我自己加的因为源程序解出来是个json字符串而且还不完整

        else:
            shop_id=''
            shop_name=''
        if shop_name.find('旗舰店')!=-1:
            shop_type='旗舰店'
        else:
            shop_type='其他'
        
        address_fr=str(response.xpath('//*[@class="serviceFlag"]/p/text()').extract()) if response.xpath('//*[@class="serviceFlag"]/p/text()') is not None and str(response.xpath('//*[@class="serviceFlag"]/p/text()').extract()).strip() else ''
        if address_fr is None or not str(address_fr).strip():
            address=''
        else:

            if '京东自营' in address_fr:
                address='京东自营'
            else:
                beg_pos=address_fr.find('从')
                end_pos=address_fr.find('发货')
                if beg_pos==-1:
                    address='店铺发货'
                elif beg_pos!=-1 and end_pos!=-1:
                    address=address_fr[beg_pos+1:end_pos]
            item['address']=address
            item['shop_name']=shop_name
            item['shop_type']=shop_type
            item['shop_id']=shop_id
        yield item


    def _parse_list_items(self, response):
        brand=response.meta['brand']
        items_list = []
        if response.body:
            json_obj = json.loads(response.body)
            json_value = json.loads(json_obj['value'])
            warelist = json_value['wareList']['wareList']
            if warelist:
                for ware in warelist:
                    item=JdpaintItem()
                    item['task_date']=task_date
                    item['ware_id']=int(ware['wareId']) if ware['wareId'] is not None and str(ware['wareId']).strip() else -1
                    item['ware_name']=ware['wname']
                    title=str(item['ware_name']).strip()
                    if title.find('工具')!=-1:
                        continue
                    if title.find('滚筒')!=-1:
                        continue
                    if title.find('滚刷')!=-1:
                        continue
                    if title.find('链接')!=-1:
                        continue
                    if title.find('服务')!=-1:
                        continue
                    if title.find('寸')!=-1:
                        continue
                    num=1
                    if title.find('套装')==-1:
                        #volume=0
                        #units='套餐'
                        if re.findall(r'\*([0-9])',title):
                            n=re.findall(r'\*([0-9])',title)
                            num=int(str(n[0]).strip())
                        else:
                            num=1
                        if re.findall(r'([0-9.]+)kg',title):
                            m=re.findall(r'([0-9.]+)kg',title)
                            volume=float(m[0])*num
                            units='kg'
                        elif re.findall(r'([0-9.]+)KG',title):
                            m=re.findall(r'([0-9.]+)KG',title)
                            volume=float(m[0])*num
                            units='kg'
                        elif re.findall(r'([0-9.]+)L',title):
                            m=re.findall(r'([0-9.]+)L',title)
                            volume=float(m[0])*num
                            units='L'    
                        elif re.findall(r'([0-9.]+)升',title):
                            m=re.findall(r'([0-9.]+)升',title)
                            volume=float(m[0])*num
                            units='L'
                        elif re.findall(r'([0-9.]+)l',title):
                            m=re.findall(r'([0-9.]+)l',title)
                            volume=float(m[0])*num
                            units='L' 
                        else:
                            volume=0
                            units=''
                    else:
                        n=[]
                        if re.findall(r'\*([0-9])',title):
                            n=re.findall(r'\*([0-9])',title)
                            num=0
                        else:
                            num=1
                        if re.findall(r'([0-9.]+)kg',title):
                            m=re.findall(r'([0-9.]+)kg',title)
                            if len(m)==1 and num==1:
                                volume=float(m[0])*num
                            elif len(m)==1 and num==0 and len(n)==1:
                                volume=float(m[0])*int(str(n[0]).strip())
                            elif len(m)>1 and len(n)>1:
                                lm=len(m)
                                ln=len(n)
                                volume=0
                                if lm==ln:
                                    for i in range(0,lm):
                                        volume=volume+int(str(m[i]).strip())*int(str(n[i]).strip())
                                else:
                                    volume=-2
                            elif len(m)>1 and num==1:
                                volume=float(m[0])
                            else:
                                volume=None
                            units='kg'
                        elif re.findall(r'([0-9.]+)KG',title):
                            m=re.findall(r'([0-9.]+)KG',title)
                            #volume=float(m[0])*num
                            if len(m)==1 and num==1:
                                volume=float(m[0])*num
                            elif len(m)==1 and num==0 and len(n)==1:
                                volume=float(m[0])*int(str(n[0]).strip())
                            elif len(m)>1 and len(n)>1:
                                lm=len(m)
                                ln=len(n)
                                volume=0
                                if lm==ln:
                                    for i in range(0,lm):
                                        volume=volume+int(str(m[i]).strip())*int(str(n[i]).strip())
                                else:
                                    volume=-2
                            elif len(m)>1 and num==1:
                                volume=float(m[0])
                            else:
                                volume=None
                            units='kg'
                        elif re.findall(r'([0-9.]+)L',title):
                            m=re.findall(r'([0-9.]+)L',title)
                            #volume=float(m[0])*num
                            if len(m)==1 and num==1:
                                volume=float(m[0])*num
                            elif len(m)==1 and num==0 and len(n)==1:
                                volume=float(m[0])*int(str(n[0]).strip())
                            elif len(m)>1 and len(n)>1:
                                lm=len(m)
                                ln=len(n)
                                volume=0
                                if lm==ln:
                                    for i in range(0,lm):
                                        volume=volume+int(str(m[i]).strip())*int(str(n[i]).strip())
                                else:
                                    volume=-2
                            elif len(m)>1 and num==1:
                                volume=float(m[0])
                            else:
                                volume=None
                            units='L'    
                        elif re.findall(r'([0-9.]+)升',title):
                            m=re.findall(r'([0-9.]+)升',title)
                            #volume=float(m[0])*num
                            if len(m)==1 and num==1:
                                volume=float(m[0])*num
                            elif len(m)==1 and num==0 and len(n)==1:
                                volume=float(m[0])*int(str(n[0]).strip())
                            elif len(m)>1 and len(n)>1:
                                lm=len(m)
                                ln=len(n)
                                volume=0
                                if lm==ln:
                                    for i in range(0,lm):
                                        volume=volume+int(str(m[i]).strip())*int(str(n[i]).strip())
                                else:
                                    volume=-2
                            elif len(m)>1 and num==1:
                                volume=float(m[0])
                            else:
                                volume=None
                            units='L'
                        elif re.findall(r'([0-9.]+)l',title):
                            m=re.findall(r'([0-9.]+)l',title)
                            #volume=float(m[0])*num
                            if len(m)==1 and num==1:
                                volume=float(m[0])*num
                            elif len(m)==1 and num==0 and len(n)==1:
                                volume=float(m[0])*int(str(n[0]).strip())
                            elif len(m)>1 and len(n)>1:
                                lm=len(m)
                                ln=len(n)
                                volume=0
                                if lm==ln:
                                    for i in range(0,lm):
                                        volume=volume+int(str(m[i]).strip())*int(str(n[i]).strip())
                                else:
                                    volume=-2
                            elif len(m)>1 and num==1:
                                volume=float(m[0])
                            else:
                                volume=None
                            units='L' 
                        else:
                            volume=0
                            units=''

                    item['volume']=volume
                    item['units']=units
                    item['price']=float(ware['jdPrice']) if  ware['jdPrice'] is not None and str(ware['jdPrice']).strip() else -1
                    item['comment_count']=int(ware['totalCount']) if  ware['totalCount'] is not None  and str(ware['totalCount']).strip() else 0
                    item['brand_name']=brand
                    items_list.append(item)
            else:
                items_list=None
        return items_list

    
    
    
    