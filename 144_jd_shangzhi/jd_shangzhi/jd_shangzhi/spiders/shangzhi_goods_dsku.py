# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from dateutil.relativedelta import relativedelta
import web
from jd_shangzhi.items import JdShangGoodsdskuItem
import sys
import zipfile
import io
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")

replenish_history=0
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'close',
           'Host': 'sz.jd.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}


class ShangzhiGoodsDskuSpider(scrapy.Spider):
    name = "shangzhi_goods_dsku"
    allowed_domains = ["sz.jd.com"]

    def time_parse(self, t):
        t = int(t)
        today = datetime.date.today()
        oneday = datetime.timedelta(days=t)
        yesterday = today - oneday
        return yesterday.strftime("%Y-%m-%d")

    def time_month(self, dt):
        return (
            datetime.datetime.strptime(dt, "%Y-%m-%d") - relativedelta(months=1) + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d")

    def time_range(self, start_time, end_time):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        while start_time <= end_time:
            yield start_time.strftime("%Y-%m-%d")
            start_time = start_time + datetime.timedelta(days=1)

    def scan_need_request(self):
        if replenish_history == 1:
            return True
        else:
            sql_spider_front = "select * from hillinsight.t_spider_jdweizhi_spider where `dt`='%s' and `spider_name`='%s'" % (
            self.time_parse(1), 't_spider_jdweizhi_goods_details_sku')
            temp = db.query(sql_spider_front)
            if temp:
                i = temp[0]
                if i.get('flag') == '0':
                    return True
                else:
                    return False
            else:
                db.query('insert into hillinsight.t_spider_jdweizhi_spider(`id`,`dt`,`spider_name`,'
                         '`flag`) VALUE (NULL,"%s","%s","0")' % (self.time_parse(1), 't_spider_jdweizhi_goods_details_sku'))
                return True

    def start_requests(self):
        if not self.scan_need_request():
            return
        self.brand_list = []
        sql = '''select `shop_name`,`cookies`,`dt` from t_spiedr_JD_cookies where 
        (shop_name,dt) in (select `shop_name`,max(`dt`) from t_spiedr_JD_cookies group by `shop_name`)
        group by shop_name;'''
        for i in db.query(sql):
            cookies = str(i.get('cookies'))
            name = i.get('shop_name')
            cookies_tuple = name, cookies
            self.brand_list.append(cookies_tuple)
        start_date = self.time_parse(1)
        yester_day = self.time_parse(1)
        for j, i in enumerate(self.brand_list):
            cookies = json.loads(i[1])
            shom_name = i[0]
            # 交易概况  可以
            for dt in self.time_range(start_date, yester_day):
                # 商品明细 sku
                url="https://sz.jd.com/productDetail/getDownProList.ajax"
                yield scrapy.FormRequest(url,method='POST',headers=headers, cookies=cookies,
                                         formdata={
                                             'categoryType':'0',
                                             'channel':'99',
                                             'date':start_date,
                                             'endDate':start_date,
                                             'goodsId':'',
                                             'second':'999999',
                                             'skuId':'undefined',
                                             'spuId':'',
                                             'startDate':start_date,
                                             'third':'',
                                             'type':'1'
                                         },meta={'date': dt, 'cate': u'商品明细sku', 'Account': shom_name},
                                         dont_filter=True)

    def parse(self, response):
        data=response.body
        shop_name = response.meta['Account']
        data_zip=io.BytesIO()
        data_zip.write(data)
        zfile=zipfile.ZipFile(data_zip,'r',zipfile.ZIP_DEFLATED, allowZip64=False)
        for filename in zfile.namelist():
            data = zfile.read(filename)
        data = xlrd.open_workbook(file_contents=data)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            item=JdShangGoodsdskuItem()
            if i <= 1:
                continue
            temp=table.row_values(i)
            item['shop_name']= shop_name    #'店铺名'
            item['id_']=    temp[0]    #'商品ID'
            item['title'] = temp[1]  # '商品名称',
            item['huohao']=temp[2]
            item['visitors'] = temp[3]  # '访客数',
            item['views']=temp[4] # '浏览量'
            item['Focus_on']= temp[5]#'商品关注数',
            item['addCartItemCnt']= temp[6]# '加购商品件数',
            item['Purchase_one'] = temp[7]  # '加购人数',
            item['orderBuyerCnt'] = temp[8]  # '下单客户数',
            item['Orders_quantity']=  temp[9]# '下单单量',
            item['orderItemQty']=temp[10] #下单商品件数
            item['orderAmt'] = temp[11]  # '下单金额',
            item['orderRate']=  temp[12]# '下单转化率',
            item['UAworth']= temp[13]#'UV价值',
            item['comments'] = temp[14]  # '评价数',
            item['launch_time'] = temp[15]  # '上架时间',
            item['date']=response.meta['date']
            item['type']='sku'
            yield item

    
    
    
    
    
    
    