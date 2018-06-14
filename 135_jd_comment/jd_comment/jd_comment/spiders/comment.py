# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Selector
import time
import MySQLdb
from jd_comment.items import JdCommentItem


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        sql = ''' select * from hillinsight.jd_sku_data '''
        conn = MySQLdb.connect(host='10.15.1.24', user='writer', passwd='hh$writer', db='hillinsight', charset='utf8',
                               connect_timeout=5000, cursorclass=MySQLdb.cursors.DictCursor)
        cur=conn.cursor()
        cur.execute(sql)
        datas=cur.fetchall()
        cur.close()
        conn.close()
        for i in datas:
            code = i.get('sku')
            for j in range(1,4):
                header={
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Host':'club.jd.com',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                }
                url = 'http://club.jd.com/review/%s-1-1-%s.html' %(code,j)
                yield scrapy.Request(url,headers=header,meta={'item':{'sku':i.get('sku'),'shop_name':i.get('shop_name'),'code':code,'type_code':j,
                                                        'brand':i.get('brand'),'price':i.get('price'),'page':1}},dont_filter=True)

    def parse(self, response):
        page=response.meta['item']['page']
        if not 'page_num' in response.meta['item']:
            page_num=response.xpath('//li[@data-widget="tab-item" and @class="curr"]/a/em/text()').extract()[0].strip('(|)').strip('+')
            page_num=int(page_num)//30+bool(int(page_num)%30)
        else:
            page_num=response.meta['item']['page_num']
        html = response.body.decode('gb18030').encode('utf8')
        good_comment_rate=response.css('.rate strong::text').extract()[0]
        name = Selector(text=html).xpath('//*[@class="i-item"]//@data-nickname').extract()
        star = Selector(text=html).xpath('//*[@class="o-topic"]//span[1]/@class').extract()
        time_sk = Selector(text=html).xpath('//*[@class="mc"]/div/div[2]/div[1]/span[2]/a/text()').extract()
        comment_id= Selector(text=html).xpath('//div[@class="useful" and @id]/@id').extract()
        code_int = 0
        type_code=['','差评','中评','好评']
        comment_type=type_code[response.meta['item']['type_code']]
        yanse=response.xpath('//div[@class="dl-extra"]/dl[1]/dd/text()').extract()
        chicun=response.xpath('//div[@class="dl-extra"]/dl[2]/dd/text()').extract()
        for i in zip(name,star,time_sk,comment_id,yanse,chicun):
            item = JdCommentItem()
            item['sku']=response.meta['item']['sku']
            item['shop_name'] = response.meta['item']['shop_name']
            item['brand'] = response.meta['item']['brand']
            item['price'] = response.meta['item']['price']
            item['comment_id']=i[3]
            item['yanse'] = i[4].strip()
            item['chicun'] = i[5].strip()
            comment_xpath='//*[@id="comment-%s"]/div/div[2]/div[2]/dl/dd/text()'%code_int
            item['comments'] = ''.join(Selector(text=html).xpath(comment_xpath).extract()).replace('\n','').replace('\t','').replace('\r','')
            item['comment_type']=comment_type
            code_int+=1
            item['good_comment_rate']=good_comment_rate
            item['comment_time'] = i[2].replace('\n','').replace('\t','').replace('\r','')
            item['comments_name'] = i[0]
            item['score'] = ''.join(re.findall('\d', i[1]))
            item['dt'] =  time.strftime("%Y-%m-%d", time.localtime())
            item['agree'] =re.sub('[^0-9]+','',response.css('#agree::text').extract()[0])
            item['reply']=response.css('.btn-reply span::text').extract()[0]
            item['dt']=time.strftime('%Y-%m-%d', time.localtime())
            yield item
        if len(name)>=30 and page<=page_num-1:
            page+=1
            url = 'http://club.jd.com/review/%s-1-%s-%s.html' % (response.meta['item']['sku'],page,response.meta['item']['type_code'])
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'club.jd.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            yield scrapy.Request(url,headers=header,meta={'type_code':response.meta['item']['type_code'],
                                           'item':{'sku':response.meta['item']['sku'],'shop_name':response.meta['item']['shop_name'],
                                                   'type_code':response.meta['item']['type_code'],
                                                    'brand':response.meta['item']['brand'],'price':response.meta['item']['price'],'page':page}},
            dont_filter=True,callback=self.parse)


    